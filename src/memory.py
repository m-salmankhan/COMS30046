from abc import ABC, abstractmethod
from collections import deque
from typing import List, Callable, Deque

import base_instruction
import registers
import writeback
import clock


class MemoryAction:
    def __init__(self, address: int, data: int | None = None, register: None | registers.Registers = None):
        # memory address to load (or store) from (or to)
        self.address = address

        # One of the two of these should be set. Not both.
        # source register for loads
        self.register = register
        # data to store
        self.data = data


class BaseMemoryInstruction(base_instruction.BaseInstruction, ABC):
    @abstractmethod
    def execute(self, register_file: registers.RegisterFile, memory: "Memory") -> None | MemoryAction:
        pass

    @abstractmethod
    def get_execution_cycles(self) -> int:
        return 1


class Memory:
    # available size in bytes
    __size = 32000

    # data types that can be stored in memory
    __type = None | base_instruction.BaseInstruction | int

    def __init__(self, register_file: registers.RegisterFile, write_back: writeback.WriteBack, clock: clock.Clock):
        self._initialised = True

        self.__memory: List[Memory.__type] = [None] * Memory.__size

        self.__register_file = register_file
        self.__write_back = write_back
        self.__clock = clock
        self.__finish_at = None

        self.__action_buffer: Deque[MemoryAction] = deque()
        self.__instruction: None | BaseMemoryInstruction = None
        self.__wb_res: None | writeback.WriteBackAction = None

    # Get address in memory
    def get(self, address: int) -> __type:
        return self.__memory[address]

    # Set address in memory
    def set(self, address: int, val: __type):
        self.__memory[address] = val

    def give_instruction(self, instruction: BaseMemoryInstruction):
        self.__instruction = instruction

    def is_available(self) -> bool:
        return self.__instruction is None

    def add_memory_action(self, action: MemoryAction):
        self.__action_buffer.append(action)

    # returns whether instruction was executed
    def execute(self) -> bool:
        if self.__instruction is None:
            return False

        print(f"MEM execute: {self.__instruction}")

        # wait if the memory unit is busy executing in the mem stage
        if not self.is_mem_busy():
            memory_action = self.__instruction.execute(self.__register_file, self)
            self.__instruction = None
            self.add_memory_action(memory_action)
            return True
        else:
            return False

    def is_mem_busy(self) -> bool:
        return len(self.__action_buffer) > 0

    def exec_memory_actions(self):
        # if self.__wb_res is not None:
        #     if self.__write_back.is_available():
        #         self.__write_back.prepare_write(self.__wb_res)
        #         self.__wb_res = None
        #     return

        if len(self.__action_buffer) == 0:
            return

        # hasn't started "executing" yet.
        if self.__finish_at is None:
            self.__finish_at = self.__clock.get_time() + 100

        action = self.__action_buffer.popleft()
        print(f"Memory: data={action.data}, address={action.address}, reg={action.register}")
        self.__action_buffer.appendleft(action)

        # only execute when the timer runs out, to simulate it taking however many cycles to execute
        # also wait for WB unit to be available
        if self.__clock.get_time() + 1 >= self.__finish_at and self.__write_back.is_available():
            action = self.__action_buffer.popleft()
            address = action.address
            data = action.data
            reg = action.register

            # if loading data from memory to register
            if reg is not None:
                print(f"\tQueue {registers.PhysicalRegisters(reg).name} <- {self.get(address)}")

                write_back_action = writeback.WriteBackAction(reg=reg, data=self.get(address))
                self.__write_back.prepare_write(write_back_action)
            # if storing data from register to memory
            else:
                print(f"\tMEM[{address}] <- {data}")
                self.set(address, data)
            self.__finish_at = None
        else:
            print("\tin progress...")

    # is the value of this register going to be changed?
    def wil_change_reg(self, register: registers.PhysicalRegisters) -> bool:
        for action in self.__action_buffer:
            if action.register == register:
                return True
        return False


# REG[dest] = MEM[REG[base] + REG[offset]]
class LoadWord(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, base: registers.Registers, offset: registers.Registers):
        self.__dest = dest
        self.__base = base
        self.__offset = offset

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        address = register_file.get_register_value(self.__base) + register_file.get_register_value(self.__offset)
        return MemoryAction(address=address, register=self.__dest)

    def get_execution_cycles(self) -> int:
        return 100

    def get_dest(self) -> registers.Registers | None:
        return self.__dest

    def get_sources(self) -> List[registers.Registers]:
        return [self.__base, self.__offset]

    def update_source_registers(self, rat: List[int]):
        self.__base = registers.PhysicalRegisters(rat[self.__base])
        self.__offset = registers.PhysicalRegisters(rat[self.__offset])

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = registers.PhysicalRegisters(new)


# REG[dest] = MEM[REG[base] + offset]
class LoadWordImmediate(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, base: registers.Registers, offset: registers.Registers):
        self.__dest = dest
        self.__base = base
        self.__offset = offset

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        address = register_file.get_register_value(self.__base) + self.__offset
        return MemoryAction(address=address, register=self.__dest)

    def get_execution_cycles(self) -> int:
        return 100

    def get_dest(self) -> registers.Registers | None:
        return self.__dest

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = registers.PhysicalRegisters(new)

    def get_sources(self) -> List[registers.Registers]:
        return [self.__base, self.__offset]

    def update_source_registers(self, rat: List[int]):
        self.__dest = registers.PhysicalRegisters(rat[self.__dest])
        self.__base = registers.PhysicalRegisters(rat[self.__base])
        self.__offset = registers.PhysicalRegisters(rat[self.__offset])


# REG[dest] = MEM[REG[address]]
class LoadWordConstant(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, address: registers.Registers):
        self.__dest = dest
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        return MemoryAction(address=register_file.get_register_value(self.__address), register=self.__dest)

    def get_execution_cycles(self) -> int:
        return 100

    def get_dest(self) -> registers.Registers | None:
        return self.__dest

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = registers.PhysicalRegisters(new)

    def get_sources(self) -> List[registers.Registers]:
        return [self.__address]

    def update_source_registers(self, rat: List[int]):
        self.__dest = registers.PhysicalRegisters(rat[self.__dest])
        self.__address = registers.PhysicalRegisters(rat[self.__address])


# REG[dest] = MEM[address]
class LoadWordConstantImmediate(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, address: int):
        self.__dest = dest
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        address = self.__address
        return MemoryAction(address=address, register=self.__dest)

    def get_execution_cycles(self) -> int:
        return 100

    def get_dest(self) -> registers.Registers | None:
        return self.__dest

    def update_dest(self, new: registers.PhysicalRegisters):
        self.__dest = registers.PhysicalRegisters(new)

    def get_sources(self) -> List[registers.Registers]:
        return []

    def update_source_registers(self, rat: List[int]):
        self.__dest = registers.PhysicalRegisters(rat[self.__dest])


# MEM[REG[address]] = REG[source]
class StoreWord(BaseMemoryInstruction):
    def __init__(self, address: registers.Registers, source: registers.Registers):
        self.__source = source
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        return MemoryAction(address=register_file.get_register_value(self.__address),
                            data=register_file.get_register_value(self.__source))

    def get_execution_cycles(self) -> int:
        return 100

    def get_dest(self) -> registers.Registers | None:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return [self.__source, self.__address]

    def update_source_registers(self, rat: List[int]):
        self.__source = registers.PhysicalRegisters(rat[self.__source])
        self.__address = registers.PhysicalRegisters(rat[self.__address])


# MEM[address] = REG[source]
class StoreWordImmediate(BaseMemoryInstruction):
    def __init__(self, address: registers.Registers, data: int):
        self.__data = data
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        return MemoryAction(address=register_file.get_register_value(self.__address),
                            data=self.__data)

    def get_execution_cycles(self) -> int:
        return 100

    def get_dest(self) -> registers.Registers | None:
        return None

    def update_dest(self, new: registers.PhysicalRegisters):
        pass

    def get_sources(self) -> List[registers.Registers]:
        return [self.__data, self.__address]

    def update_source_registers(self, rat: List[int]):
        self.__data = registers.PhysicalRegisters(rat[self.__data])
        self.__address = registers.PhysicalRegisters(rat[self.__address])
