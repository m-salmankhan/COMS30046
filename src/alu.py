from abc import ABC, abstractmethod
from math import floor

import registers
import writeback
import base_instruction


class BaseALUInstruction(base_instruction.BaseInstruction, ABC):
    @abstractmethod
    def execute(self, register_file: registers.RegisterFile) -> None | writeback.WriteBackAction:
        pass


class BitWiseAnd(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) & register_file.get_register_value(self.__op2)
        )


class BitWiseOr(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) | register_file.get_register_value(self.__op2)
        )


class BitWiseXOr(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) ^ register_file.get_register_value(self.__op2)
        )


class BitWiseNot(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers):
        self.__dest = dest
        self.__op1 = op1

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            ~register_file.get_register_value(self.__op1)
        )


class Add(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) + register_file.get_register_value(self.__op2)
        )


class AddImmediate(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: int):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) + self.__op2
        )


class Subtract(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) - register_file.get_register_value(self.__op2)
        )


class SubtractImmediate(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: int):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) - self.__op2
        )


class LesserThan(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) < register_file.get_register_value(self.__op2)
        )


class GreaterThan(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) > register_file.get_register_value(self.__op2)
        )


class EqualTo(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) == register_file.get_register_value(self.__op2)
        )


class Multiply(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) * register_file.get_register_value(self.__op2)
        )


class MultiplyImmediate(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: int):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) * self.__op2
        )


class LeftShift(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) << register_file.get_register_value(self.__op2)
        )


class LeftShiftImmediate(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: int):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) << self.__op2
        )


class RightShift(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) >> register_file.get_register_value(self.__op2)
        )


class RightShiftImmediate(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: int):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            register_file.get_register_value(self.__op1) >> self.__op2
        )


class Divide(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            floor(register_file.get_register_value(self.__op1) / register_file.get_register_value(self.__op2))
        )


class ALU:
    def __init__(self, register_file: registers.RegisterFile, write_back: writeback.WriteBack):
        self.__register_file = register_file

        self.__write_back = write_back
        self.__instruction: None | BaseALUInstruction = None

    def give_instruction(self, instruction: BaseALUInstruction):
        self.__instruction = instruction

    class ExecuteResults:
        def __init__(self, writeback: writeback.WriteBack, wb_action: writeback.WriteBackAction | None):
            self.__wb_action = wb_action
            self.__wb = writeback

        def apply(self):
            if self.__wb_action is not None:
                self.__wb.prepare_write(self.__wb_action)

    def execute(self):
        if self.__instruction is None:
            return

        write_back_action = self.__instruction.execute(self.__register_file)
        self.__instruction = None
        return self.ExecuteResults(self.__write_back, write_back_action)
