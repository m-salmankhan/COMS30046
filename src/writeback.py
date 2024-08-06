from collections import deque
from typing import Deque

import registers


class WriteBackAction:
    def __init__(self, reg: registers.Registers, data: int):
        self.reg = reg
        self.data = data


class WriteBack:
    # singleton instance
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(WriteBack, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if not hasattr(self, "_initialised"):
            self._initialised = True
            self.__register_file = registers.RegisterFile()
            self.__action_buffer: Deque[WriteBackAction] = deque()

    def prepare_write(self, action: WriteBackAction):
        self.__action_buffer.append(action)

    def is_available(self) -> bool:
        return len(self.__action_buffer) == 0

    def write(self):
        if len(self.__action_buffer) == 0:
            return

        action = self.__action_buffer.popleft()
        print(f"write-back: Writing {registers.Registers(action.reg).name} <- {action.data}")
        self.__register_file.set_register_value(action.reg, action.data)
