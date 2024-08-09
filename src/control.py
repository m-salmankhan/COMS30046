import copy
from abc import abstractmethod
from typing import Tuple, Callable, List

import alu
import memory
import registers
import base_instruction
import clock
from src import flags


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

        self.__waiting_for_results = False

        # instruction to be executed in "execute" stage
        self.__instruction: BaseControlInstruction | None = None

    # rewrites arch registers and physical and checks for data hazards. If found, it stalls.
    # returns Tuple [is instruction a branch?, Did we change the PC early?]
    def check_hazards(self) -> Tuple[bool, bool]:
        instruction = self.__instruction_register
        if instruction is None or not isinstance(instruction, base_instruction.BaseInstruction):
            return False, False

        is_new_branch = False
        if isinstance(instruction, BranchAbsoluteTrue) or isinstance(instruction, BranchAbsoluteTrueImmediate) or isinstance(instruction, JumpAbsolute) or isinstance(instruction, JumpAbsoluteImmediate):
            is_new_branch = True

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
            self.__instruction_register = instruction
        else:
            # we've already renamed it so must already have counted it as a branch
            is_new_branch = False
        # if any of the source registers are being written to, we need to wait for them
        """
        Conditions we wait:
            - a functional unit is executing an instruction that writes to a register that's used here
            - the memory unit is about to push an action into the MEM/WB pipeline register that writes to this register
            
            - Result forwarding is off AND:
                - the wb unit already has an action in its pipeline register that writes to this
                - the memory unit is about to forward a result from EX to WB (in this case, the value is known)
        """
        self.__waiting_for_results = False
        sources = self.__instruction_register.get_sources()

        # if we aren't renaming registers, we also need to wait for the destination
        if not flags.rename_registers and dest is not None:
            sources.append(dest)

        for source in sources:
            alu_writing = self.__ALU.get_instruction().get_dest() == source if self.__ALU.get_instruction() is not None else False
            cu_writing = self.__instruction.get_dest() == source if self.__instruction is not None else False
            mem_writing = self.__memory.get_instruction().get_dest() == source if self.__memory.get_instruction() is not None else False

            function_units_writing = alu_writing or cu_writing or mem_writing

            # forwarded results from mem and wb units
            wb_res = self.__writeback.forward_result(source)
            mem_res = self.__memory.forward_result(source)
            forwarded_result = wb_res if wb_res is not None else mem_res

            # If result is still being written to in EX stage
            if function_units_writing:
                print(f"Hazard Check: waiting for {registers.PhysicalRegisters(source).name} to be written to. Still executing")
                self.__waiting_for_results = True
            # if a memory action is about to cause a write to this register
            elif self.__memory.wil_change_reg(source):
                print(f"Hazard Check: waiting for {registers.PhysicalRegisters(source).name} to be written to. Memory result executing.")
                self.__waiting_for_results = True
            # it's in the EX/MEM or MEM/WB reg
            elif forwarded_result is not None:
                if not flags.forward_results:
                    print(f"Hazard Check: waiting for {registers.PhysicalRegisters(source).name} to be written to. Not Writtenback yet")
                    self.__waiting_for_results = True
            else:
                continue

        # if it's a JMP (unconditional branch) change PC here
        if isinstance(instruction, JumpAbsolute) or isinstance(instruction, JumpAbsoluteImmediate):
            new_pc, _ = instruction.execute(self.__register_file)
            self.update_pc(new_pc)
            return is_new_branch, new_pc != self.__program_counter

        return is_new_branch, False


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

    def decode(self):
        instruction = self.__instruction_register

        if instruction is None:
            return

        print(f"decoding: {instruction}")

        if not isinstance(instruction, base_instruction.BaseInstruction):
            raise Exception("Encountered data (not instruction) within PC address")

        dest = instruction.get_dest()
        dest_is_renamed = dest is not None and isinstance(dest, registers.PhysicalRegisters)

        # TODO: handle rename failed: e.g. if there weren't enough physical registers
        # lets rename the registers
        if flags.rename_registers and dest is not None and not dest_is_renamed:
            print(f"\t Remapping {registers.ArchRegisters(dest).name}, for {instruction}")
            new_dest = self.__register_file.alias_register(dest)
            instruction.update_dest(new_dest)
        self.__instruction_register = instruction

        occupied_units = sum([0 if available else 1 for available in
                              [self.is_available(), self.__memory.is_available(), self.__ALU.is_available()]])

        if self.__waiting_for_results:
            print("\t Waiting for results, can't decode.")

        if occupied_units == 0 and not self.__waiting_for_results:

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

    # return Tuple [did CU execute ins?, was PC changed?, was HALT encountered?]
    def execute(self) -> Tuple[bool, bool, bool]:
        if self.__instruction is None:
            return False, False, False

        print(f"CU execute: {self.__instruction}")

        if isinstance(self.__instruction, JumpAbsoluteImmediate) or isinstance(self.__instruction, JumpAbsolute):
            print(f"\t JMP already evaluated at Decode Stage, doing nothing")
            self.__instruction = None
            return True, False, False

        # wait for memory to be available
        if not self.__memory.is_mem_busy():
            new_pc, new_halt = self.__instruction.execute(self.__register_file)

            if new_pc is not None and new_pc != self.__program_counter:
                print(f"\t PC value changed.")
                self.update_pc(new_pc)
            if new_halt is not None:
                self.halt_status = new_halt

            self.__instruction = None

            return True, (new_pc is not None), (new_halt is not None)

        return False, False, False
