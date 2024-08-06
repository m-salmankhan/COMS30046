from abc import ABC, abstractmethod
from math import floor

import registers
import writeback
import base_instruction
import clock

class BaseALUInstruction(base_instruction.BaseInstruction, ABC):
    @abstractmethod
    def execute(self, register_file: registers.RegisterFile) -> None | writeback.WriteBackAction:
        pass

    @abstractmethod
    def get_execution_cycles(self) -> int:
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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


class BitWiseNot(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers):
        self.__dest = dest
        self.__op1 = op1

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            ~register_file.get_register_value(self.__op1)
        )

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


class Multiply(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers, op2: registers.Registers):
        self.__dest = dest
        self.__op1 = op1
        self.__op2 = op2

    def execute(self, register_file: registers.RegisterFile):
        val1 = register_file.get_register_value(self.__op1)
        val2 = register_file.get_register_value(self.__op2)
        return writeback.WriteBackAction(
            self.__dest,
            val1 * val2
        )

    def get_execution_cycles(self) -> int:
        return 10


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

    def get_execution_cycles(self) -> int:
        return 10


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 1


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

    def get_execution_cycles(self) -> int:
        return 10


class ALU:
    def __init__(self, register_file: registers.RegisterFile, write_back: writeback.WriteBack, clock: clock.Clock):
        self.__register_file = register_file
        self.__clock = clock
        self.__write_back = write_back
        self.__instruction: None | BaseALUInstruction = None

        # used to keep track of which clock cycle the instruction that's executing should finish at.
        self.__finish_at: None | int = 0

    def give_instruction(self, instruction: BaseALUInstruction):
        self.__instruction = instruction

    # whether the ALU is available for being given a new instruction (i.e. has it finished executing the last one).
    def is_available(self) -> bool:
        return self.__instruction is None

    # returns whether instruction was executed
    def execute(self) -> bool:
        if self.__instruction is None:
            return False
        print(f"execute: {self.__instruction}")

        # hasn't started "executing" yet.
        if self.__finish_at is None:
            self.__finish_at = self.__clock.get_time() + self.__instruction.get_execution_cycles()

        # only execute when the timer runs out, to simulate it taking however many cycles to execute
        if self.__clock.get_time() + 1 >= self.__finish_at:
            write_back_action = self.__instruction.execute(self.__register_file)
            self.__finish_at = None
            self.__instruction = None
            self.__write_back.prepare_write(write_back_action)
            return True
        else:
            return False
