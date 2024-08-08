import copy
from abc import abstractmethod
from typing import Tuple, Callable, List

import alu
import memory
import registers
import base_instruction
import clock


class BaseControlInstruction(base_instruction.BaseInstruction):
    @abstractmethod
    def execute(self, register_file: registers.RegisterFile) -> Tuple[None | int, None | int]:
        pass


class JumpAbsolute(BaseControlInstruction):
    def __init__(self, location: registers.Registers):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile) -> Tuple[int, None]:
        return register_file.get_register_value(self.__loc), None

    def get_dest(self) -> registers.Registers:
        return None

    def get_sources(self) -> List[registers.Registers]:
        return [self.__loc]

    def update_source_registers(self, rat: List[int]):
        physical = rat[self.__loc]
        self.__loc = registers.PhysicalRegisters(physical)

    def update_dest(self, new: registers.PhysicalRegisters):
        pass


class JumpAbsoluteImmediate(BaseControlInstruction):
    def __init__(self, location: int):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile) -> Tuple[int, None]:
        return self.__loc, None

    def get_dest(self) -> registers.Registers:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return []

    def update_source_registers(self, rat: List[int]):
        pass


class BranchAbsoluteTrue(BaseControlInstruction):
    def __init__(self, cond: registers.Registers, location: registers.Registers):
        self.__loc = location
        self.__cond = cond

    def execute(self, register_file: registers.RegisterFile) -> Tuple[None | int, None]:
        if register_file.get_register_value(self.__cond):
            return register_file.get_register_value(self.__loc), None
        return None, None

    def get_dest(self) -> registers.Registers:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return [self.__loc, self.__cond]

    def update_source_registers(self, rat: List[int]):
        self.__loc = registers.PhysicalRegisters(rat[self.__loc])
        self.__cond = registers.PhysicalRegisters(rat[self.__cond])


class BranchAbsoluteTrueImmediate(BaseControlInstruction):
    def __init__(self, cond: registers.Registers, location: int):
        self.__loc = location
        self.__cond = cond

    def execute(self, register_file: registers.RegisterFile) -> Tuple[None | int, None]:
        if register_file.get_register_value(self.__cond):
            return self.__loc, None
        return None, None

    def get_dest(self) -> registers.Registers:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return [self.__cond]

    def update_source_registers(self, rat: List[int]):
        self.__cond = registers.PhysicalRegisters(rat[self.__cond])


class Halt(BaseControlInstruction):
    def execute(self, register_file: registers.RegisterFile) -> Tuple[None, int]:
        return None, 1

    def get_dest(self) -> registers.Registers:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return []

    def update_source_registers(self, rat: List[int]):
        pass


class NoOp(BaseControlInstruction):
    def execute(self, register_file: registers.RegisterFile) -> Tuple[None, None]:
        return None, None

    def get_dest(self) -> registers.Registers:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return []

    def update_source_registers(self, rat: List[int]):
        pass


class Control:
    def __init__(self, alu: alu.ALU, mem: memory.Memory, register_file: registers.RegisterFile, clock: clock.Clock,
                 writeback):
        self.__register_file = register_file
        self.__ALU = alu
        self.__memory = mem
        self.__clock = clock
        self.__writeback = writeback

        self.__program_counter: int = 0
        self.__instruction_register: base_instruction.BaseInstruction | None = None
        self.halt_status: int = 0

        # instruction to be executed in "execute" stage
        self.__instruction: BaseControlInstruction | None = None

    def instruction_fetch(self) -> None:
        if self.halt_status == 1:
            print("HALTED")
            return

        print(f"fetch: {self.__program_counter}")

        current_addr = self.__program_counter
        instruction = self.__memory.get(current_addr)

        # only fetch and increment PC if the last instruction has already been decoded
        if self.is_ir_available():
            self.update_ir(instruction)
            self.update_pc(current_addr + 1)

    def decode(self) -> None:
        instruction = self.__instruction_register

        if instruction is None:
            return

        print(f"decoding: {instruction}")

        if not isinstance(instruction, base_instruction.BaseInstruction):
            raise Exception("Encountered data (not instruction) within PC address")

        dest = instruction.get_dest()
        sources = instruction.get_sources()

        source_is_renamed = (len(sources) > 0 and isinstance(sources[0], registers.PhysicalRegisters))
        dest_is_renamed = dest is not None and isinstance(dest, registers.PhysicalRegisters)

        # Renaming time!
        # Just make sure we don't accidentally rename twice because it waited the first time.
        if not (source_is_renamed or dest_is_renamed):
            instruction = copy.deepcopy(instruction)
            # look up the physical registers in the RAT and replace them
            instruction.update_source_registers(self.__register_file.get_rat())
            # lets rename the registers
            if dest is not None:
                print(f"\tRemapping {registers.ArchRegisters(dest).name}, for {instruction}")
                new_dest = self.__register_file.alias_register(dest)
                instruction.update_dest(new_dest)
            self.__instruction_register = instruction

        waiting_for_results = False
        sources = self.__instruction_register.get_sources()
        for source in sources:
            res = self.__writeback.forward_result(source)
            if res is not None or self.__memory.wil_change_reg(source):
                print(f"\t waiting for {registers.PhysicalRegisters(source).name} to be valid")
                waiting_for_results = True


        occupied_units = sum([0 if available else 1 for available in
                              [self.is_available(), self.__memory.is_available(), self.__ALU.is_available()]])

        if occupied_units == 0 and not waiting_for_results:
        # if occupied_units == 0:
            sources = self.__instruction_register.get_sources()
            for source in sources:
                res = self.__writeback.forward_result(source)
                if res is not None or self.__memory.wil_change_reg(source):
                    print(f"\t waiting for {registers.PhysicalRegisters(source).name} to be valid")
                    wait = True

            if isinstance(instruction, alu.BaseALUInstruction):
                self.__ALU.give_instruction(instruction)
                self.__instruction_register = None
            elif isinstance(instruction, memory.BaseMemoryInstruction):
                self.__memory.give_instruction(instruction)
                self.__instruction_register = None
            elif isinstance(instruction, BaseControlInstruction):
                self.give_instruction(instruction)
                self.__instruction_register = None
            else:
                raise Exception(f"No unit exists to execute instructions of type {type(instruction)}.")
        else:
            print("Unit occupied, blocking")

    def update_pc(self, new_val: int):
        self.__program_counter = new_val

    def update_ir(self, inst: base_instruction.BaseInstruction | None):
        self.__instruction_register = inst

    # has the last instruction been dispatched to the relevant unit already?
    def is_ir_available(self) -> bool:
        return self.__instruction_register is None

    def give_instruction(self, instruction: BaseControlInstruction):
        self.__instruction = instruction

    # is the Control unit available to execute a new instruction?
    def is_available(self):
        return self.__instruction is None

    def execute(self) -> Tuple[bool, bool, bool]:
        if self.__instruction is None:
            return False, False, False

        print(f"CU execute: {self.__instruction}")
        # wait for memory to be available
        if not self.__memory.is_mem_busy():
            new_pc, new_halt = self.__instruction.execute(self.__register_file)
            self.__instruction = None

            if new_pc is not None:
                self.update_pc(new_pc)
            if new_halt is not None:
                self.halt_status = new_halt

            return True, (new_pc is not None), (new_halt is not None)
        return False, False, False
