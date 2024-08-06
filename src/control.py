from abc import abstractmethod
from typing import Tuple, Callable

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


class JumpAbsoluteImmediate(BaseControlInstruction):
    def __init__(self, location: int):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile) -> Tuple[int, None]:
        return self.__loc, None


class BranchAbsoluteTrue(BaseControlInstruction):
    def __init__(self, cond: registers.Registers, location: registers.Registers):
        self.__loc = location
        self.__cond = cond

    def execute(self, register_file: registers.RegisterFile) -> Tuple[None | int, None]:
        if register_file.get_register_value(self.__cond):
            return register_file.get_register_value(self.__loc), None
        return None, None


class BranchAbsoluteTrueImmediate(BaseControlInstruction):
    def __init__(self, cond: registers.Registers, location: int):
        self.__loc = location
        self.__cond = cond

    def execute(self, register_file: registers.RegisterFile) -> Tuple[None | int, None]:
        if register_file.get_register_value(self.__cond):
            return self.__loc, None
        return None, None


class Halt(BaseControlInstruction):
    def execute(self, register_file: registers.RegisterFile) -> Tuple[None, int]:
        return None, 1


class NoOp(BaseControlInstruction):
    def execute(self, register_file: registers.RegisterFile) -> Tuple[None, None]:
        return None, None


class Control:
    def __init__(self, alu: alu.ALU, mem: memory.Memory, register_file: registers.RegisterFile, clock: clock.Clock):
        self.__register_file = register_file
        self.__ALU = alu
        self.__memory = mem
        self.__clock = clock

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
            self.update_pc(current_addr+1)

    def decode(self) -> None:
        instruction = self.__instruction_register

        if instruction is None:
            return

        print(f"decoding: {instruction}")

        if not isinstance(instruction, base_instruction.BaseInstruction):
            raise Exception("Encountered data (not instruction) within PC address")

        occupied_units = sum([1 if occupied else 0 for occupied in [self.is_available(), self.__memory.is_available(), self.__ALU.is_available()]])
        if occupied_units != 0:
            if isinstance(instruction, alu.BaseALUInstruction):
                if self.__ALU.is_available():
                    self.__ALU.give_instruction(instruction)
                    self.__instruction_register = None
            elif isinstance(instruction, memory.BaseMemoryInstruction):
                if self.__memory.is_available():
                    self.__memory.give_instruction(instruction)
                    self.__instruction_register = None
            elif isinstance(instruction, BaseControlInstruction):
                if self.is_available():
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

    # has the last instruction been dispatched to the relavent unit already?
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

        print(f"execute: {self.__instruction}")

        # all CU unit only take 1 cycle, don't bother waiting
        new_pc, new_halt = self.__instruction.execute(self.__register_file)
        self.__instruction = None

        if new_pc is not None:
            self.update_pc(new_pc)
        if new_halt is not None:
            self.halt_status = new_halt

        return True, (new_pc is not None), (new_halt is not None)
