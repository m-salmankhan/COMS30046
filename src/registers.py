from enum import IntEnum, verify, UNIQUE


@verify(UNIQUE)
class Registers(IntEnum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    R8 = 8
    R9 = 9
    R10 = 10
    R11 = 11
    R12 = 12
    R13 = 13


class RegisterFile:
    __registers = None

    def __new__(cls, ):
        if cls.__registers is None:
            cls.__registers = super(RegisterFile, cls).__new__(cls)
        return cls.__registers

    def __init__(self):
        self.__registers = [0] * len(Registers)

    def print_register_file(self, time: int | None = None):
        if time is not None:
            print(f"Register file at t={time}")
        else:
            print("Register File")

        for (idx, val) in enumerate(self.__registers):
            name = Registers(idx).name
            print(f"{name} \t {val}")

    def get_register_value(self, register: Registers) -> int:
        print(f"getting register {Registers(register).name} at index {register}")
        return self.__registers[register]

    def set_register_value(self, register: Registers, new_val: int):
        self.__registers[register] = new_val

    @property
    def r0(self):
        return self.__registers[Registers.R0]

    @r0.setter
    def r0(self, new_val):
        self.__registers[Registers.R0] = new_val

    @property
    def r1(self):
        return self.__registers[Registers.R1]

    @r1.setter
    def r1(self, new_val):
        self.__registers[Registers.R1] = new_val

    @property
    def r2(self):
        return self.__registers[Registers.R2]

    @r2.setter
    def r2(self, new_val):
        self.__registers[Registers.R2] = new_val

    @property
    def r3(self):
        return self.__registers[Registers.R3]

    @r3.setter
    def r3(self, new_val):
        self.__registers[Registers.R3] = new_val

    @property
    def r4(self):
        return self.__registers[Registers.R4]

    @r4.setter
    def r4(self, new_val):
        self.__registers[Registers.R4] = new_val

    @property
    def r5(self):
        return self.__registers[Registers.R5]

    @r5.setter
    def r5(self, new_val):
        self.__registers[Registers.R5] = new_val

    @property
    def r6(self):
        return self.__registers[Registers.R6]

    @r6.setter
    def r6(self, new_val):
        self.__registers[Registers.R6] = new_val

    @property
    def r7(self):
        return self.__registers[Registers.R7]

    @r7.setter
    def r7(self, new_val):
        self.__registers[Registers.R7] = new_val

    @property
    def r8(self):
        return self.__registers[Registers.R8]

    @r8.setter
    def r8(self, new_val):
        self.__registers[Registers.R8] = new_val

    @property
    def r9(self):
        return self.__registers[Registers.R9]

    @r9.setter
    def r9(self, new_val):
        self.__registers[Registers.R9] = new_val

    @property
    def r10(self):
        return self.__registers[Registers.R10]

    @r10.setter
    def r10(self, new_val):
        self.__registers[Registers.R10] = new_val

    @property
    def r11(self):
        return self.__registers[Registers.R11]

    @r11.setter
    def r11(self, new_val):
        self.__registers[Registers.R11] = new_val

    @property
    def r12(self):
        return self.__registers[Registers.R12]

    @r12.setter
    def r12(self, new_val):
        self.__registers[Registers.R12] = new_val
