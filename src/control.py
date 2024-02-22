from abc import abstractmethod
from typing import Tuple, Callable

import alu
import memory
import registers
import base_instruction


class BaseControlInstruction(base_instruction.BaseInstruction):
    @abstractmethod
    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[None | int, None | int]:
        pass


class JumpRelative(base_instruction.BaseInstruction):
    def __init__(self, location: registers.Registers):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        return register_file.get_register_value(self.__loc) + pc_value, None


class JumpAbsolute(BaseControlInstruction):
    def __init__(self, location: registers.Registers):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        return register_file.get_register_value(self.__loc), None


class JumpRelativeImmediate(BaseControlInstruction):
    def __init__(self, location: int):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        return self.__loc + pc_value, None


class JumpAbsoluteImmediate(BaseControlInstruction):
    def __init__(self, location: int):
        self.__loc = location

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        return self.__loc, None


class BranchRelativeTrue(BaseControlInstruction):
    def __init__(self, location: registers.Registers, condition: registers.Registers):
        self.__loc = location
        self.__cond = condition

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        if register_file.get_register_value(self.__cond):
            return register_file.get_register_value(self.__loc) + pc_value, None


class BranchRelativeTrueImmediate(BaseControlInstruction):
    def __init__(self, location: int, condition: registers.Registers):
        self.__loc = location
        self.__cond = condition

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        if register_file.get_register_value(self.__cond):
            return self.__loc + pc_value, None


class BranchAbsoluteTrue(BaseControlInstruction):
    def __init__(self, location: registers.Registers, cond: registers.Registers):
        self.__loc = location
        self.__cond = cond

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        if register_file.get_register_value(self.__cond):
            return register_file.get_register_value(self.__loc) + pc_value, None


class BranchAbsoluteTrueImmediate(BaseControlInstruction):
    def __init__(self, location: int, cond: registers.Registers):
        self.__loc = location
        self.__cond = cond

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[int, None]:
        if register_file.get_register_value(self.__cond):
            return self.__loc + pc_value, None


class Halt(BaseControlInstruction):
    def __init__(self, status: registers.Registers):
        self.__status = status

    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[None, int]:
        return None, register_file.get_register_value(self.__status)


class NoOp(BaseControlInstruction):
    def execute(self, register_file: registers.RegisterFile, pc_value: int) -> Tuple[None, None]:
        return None, None


class Control:
    def __init__(self, alu: alu.ALU, mem: memory.Memory, register_file: registers.RegisterFile):
        self.__register_file = register_file
        self.__ALU = alu
        self.__memory = mem

        self.__program_counter: int = 0
        self.__instruction_register: base_instruction.BaseInstruction | None = None
        self.halt_status: int = 0

        # instruction to be executed in "execute" stage
        self.__instruction: BaseControlInstruction | None = None

    class DecodeResults:
        def __init__(self, callback: Callable):
            self.apply = callback

    class FetchResults:
        def __init__(self, parent: "Control", new_pc: int, new_ir: base_instruction.BaseInstruction):
            self.__new_pc = new_pc
            self.__new_ir = new_ir
            self.__parent = parent

        def apply(self):
            self.__parent.update_ir(self.__new_ir)
            self.__parent.update_pc(self.__new_pc)

    def instruction_fetch(self) -> FetchResults | None:
        if self.halt_status == 1:
            print("HALTED")
            return

        addr = self.__program_counter
        instruction = self.__memory.get(addr)

        return self.FetchResults(self, addr + 1, instruction)

    def decode(self) -> None | DecodeResults:
        instruction = self.__instruction_register

        if instruction is None:
            return

        if not isinstance(instruction, base_instruction.BaseInstruction):
            raise Exception("Encountered data (not instruction) within PC address")

        if isinstance(instruction, alu.BaseALUInstruction):
            return self.DecodeResults(lambda: self.__ALU.give_instruction(instruction))
        elif isinstance(instruction, memory.BaseMemoryInstruction):
            return self.DecodeResults(lambda: self.__memory.give_instruction(instruction))
        elif isinstance(instruction, BaseControlInstruction):
            return self.DecodeResults(lambda: self.give_instruction(instruction))
        else:
            raise Exception(f"No unit exists to execute instructions of type {type(instruction)}.")

    def update_pc(self, new_val: int):
        self.__program_counter = new_val

    def update_ir(self, inst: base_instruction.BaseInstruction):
        self.__instruction_register = inst

    def give_instruction(self, instruction: BaseControlInstruction):
        self.__instruction = instruction

    class ExecuteResults:
        def __init__(self, parent: "Control", new_pc: int | None, new_halt: int | None):
            self.__pc = new_pc
            self.__halt = new_halt
            self.__parent = parent

        def apply(self):
            if self.__pc is not None:
                self.__parent.update_pc(self.__pc)
            if self.__halt is not None:
                self.__parent.halt_status = self.__halt

    def execute(self) -> ExecuteResults | None:
        if self.__instruction is None:
            return
        new_pc, new_halt = self.__instruction.execute(self.__register_file, self.__program_counter)
        self.__instruction = None
        return self.ExecuteResults(self, new_pc, new_halt)
