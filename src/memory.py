from abc import ABC, abstractmethod
from collections import deque
from typing import List, Callable, Deque

import base_instruction
import registers
import writeback


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


class Memory:
    # available size in bytes
    __size = 32000

    # data types that can be stored in memory
    __type = None | base_instruction.BaseInstruction | int

    # singleton instance
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Memory, cls).__new__(cls)

        return cls.__instance

    def __init__(self, register_file: registers.RegisterFile, write_back: writeback.WriteBack):
        if not hasattr(self, "_initialised"):
            self._initialised = True

            self.__memory: List[Memory.__type] = [None] * Memory.__size

            self.__register_file = register_file
            self.__write_back = write_back

            self.__action_buffer: Deque[MemoryAction] = deque()
            self.__instruction: None | BaseMemoryInstruction = None

    # Get address in memory
    def get(self, address: int) -> __type:
        return self.__memory[address]

    # Set address in memory
    def set(self, address: int, val: __type):
        self.__memory[address] = val

    def give_instruction(self, instruction: BaseMemoryInstruction):
        self.__instruction = instruction

    def add_memory_action(self, action: MemoryAction):
        self.__action_buffer.append(action)

    def execute(self):
        if self.__instruction is None:
            return

        print(f"execute: {self.__instruction}")

        memory_action = self.__instruction.execute(self.__register_file, self)
        self.__instruction = None
        self.add_memory_action(memory_action)

    def exec_memory_actions(self):
        for _ in range(len(self.__action_buffer)):
            action = self.__action_buffer.popleft()

            address = action.address
            data = action.data
            reg = action.register

            # if loading data from memory to register
            if reg is not None:
                print(f"memory: Queue {registers.Registers(reg).name} <- {self.get(address)}")

                write_back_action = writeback.WriteBackAction(reg=reg, data=self.get(address))
                self.__write_back.prepare_write(write_back_action)

            # if storing data from register to memory
            else:
                print(f"memory: MEM[{address}] <- {data}")
                self.set(address, data)


# REG[dest] = MEM[REG[base] + REG[offset]]
class LoadWord(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, base: registers.Registers, offset: registers.Registers):
        self.__dest = dest
        self.__base = base
        self.__offset = offset

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        address = register_file.get_register_value(self.__base) + register_file.get_register_value(self.__offset)
        return MemoryAction(address=address, register=self.__dest)


# REG[dest] = MEM[REG[base] + offset]
class LoadWordImmediate(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, base: registers.Registers, offset: registers.Registers):
        self.__dest = dest
        self.__base = base
        self.__offset = offset

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        address = register_file.get_register_value(self.__base) + self.__offset
        return MemoryAction(address=address, register=self.__dest)


# REG[dest] = MEM[REG[address]]
class LoadWordConstant(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, address: registers.Registers):
        self.__dest = dest
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        return MemoryAction(address=register_file.get_register_value(self.__address), register=self.__dest)


# REG[dest] = MEM[address]
class LoadWordConstantImmediate(BaseMemoryInstruction):
    def __init__(self, dest: registers.Registers, address: registers.Registers):
        self.__dest = dest
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        address = self.__address
        return MemoryAction(address=address, register=self.__dest)


# MEM[REG[address]] = REG[source]
class StoreWord(BaseMemoryInstruction):
    def __init__(self, address: registers.Registers, source: registers.Registers):
        self.__source = source
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        return MemoryAction(address=register_file.get_register_value(self.__address),
                            data=register_file.get_register_value(self.__source))


# MEM[address] = REG[source]
class StoreWordImmediate(BaseMemoryInstruction):
    def __init__(self, address: registers.Registers, data: int):
        self.__data = data
        self.__address = address

    def execute(self, register_file: registers.RegisterFile, memory: Memory):
        return MemoryAction(address=register_file.get_register_value(self.__address),
                            data=self.__data)
