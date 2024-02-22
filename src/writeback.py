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
            self.__action_buffer = None

    def prepare_write(self, action: WriteBackAction):
        self.__action_buffer = action

    class WriteResults:
        def __init__(self, register_file: registers.RegisterFile, register: registers.Registers, data: int):
            self.__register_file = register_file
            self.__register = register
            self.__data = data

        def apply(self):
            self.__register_file.set_register_value(self.__register, self.__data)

    def write(self):
        if self.__action_buffer is not None:
            results = self.WriteResults(self.__register_file, self.__action_buffer.reg, self.__action_buffer.data)
            self.__action_buffer = None
            return results

        else:
            pass
            # print("Nothing to write to registers")
