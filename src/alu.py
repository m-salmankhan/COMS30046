from abc import ABC, abstractmethod
from math import floor
from typing import List

import registers
import writeback
import base_instruction
import clock
import memory


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new

class LogicalNot(BaseALUInstruction):
    def __init__(self, dest: registers.Registers, op1: registers.Registers):
        self.__dest = dest
        self.__op1 = op1

    def execute(self, register_file: registers.RegisterFile):
        return writeback.WriteBackAction(
            self.__dest,
            not register_file.get_register_value(self.__op1)
        )

    def get_execution_cycles(self) -> int:
        return 1

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers | None:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


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

    def get_dest(self) -> registers.Registers:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__op1, self.__op2]

    def update_source_registers(self, rat: List[int]):
        self.__op1 = registers.PhysicalRegisters(rat[self.__op1])
        self.__op2 = registers.PhysicalRegisters(rat[self.__op2])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = new


class ALU:
    def __init__(self, register_file: registers.RegisterFile, write_back: writeback.WriteBack, clock: clock.Clock,
                 memory: memory.Memory):
        self.__register_file = register_file
        self.__clock = clock
        self.__write_back = write_back
        self.__instruction: None | BaseALUInstruction = None
        self.__memory = memory

        # used to keep track of which clock cycle the instruction that's executing should finish at.
        self.__finish_at: None | int = 0

    def give_instruction(self, instruction: BaseALUInstruction):
        self.__instruction = instruction

    def get_instruction(self) -> BaseALUInstruction | None:
        return self.__instruction

    # whether the ALU is available for being given a new instruction (i.e. has it finished executing the last one).
    def is_available(self) -> bool:
        return self.__instruction is None

    # returns whether instruction was executed
    def execute(self) -> bool:
        if self.__instruction is None:
            return False


        print(f"ALU execute: {self.__instruction}")

        # hasn't started "executing" yet.
        if self.__finish_at is None:
            self.__finish_at = self.__clock.get_time() + self.__instruction.get_execution_cycles()

        # only execute when the timer runs out, to simulate it taking however many cycles to execute
        # we also need to make sure that the memory unit is free (even though there's no dependence between them)
        # to ensure in-order execution
        if self.__clock.get_time() + 1 >= self.__finish_at:
            write_back_action = self.__instruction.execute(self.__register_file)
            # stall if memory unit busy
            if not self.__memory.is_mem_busy():
                print(f"\t forward through MEM: {registers.PhysicalRegisters(write_back_action.reg).name} <- {write_back_action.data}")
                self.__memory.pass_to_wb(write_back_action)
                self.__finish_at = None
                self.__instruction = None
                return True
            else:
                print(f"\t Stalling waiting for memory")

        return False
