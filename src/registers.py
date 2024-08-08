from collections import deque
from enum import IntEnum, verify, UNIQUE
from typing import Deque, List


@verify(UNIQUE)
class ArchRegisters(IntEnum):
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


@verify(UNIQUE)
class PhysicalRegisters(IntEnum):
    P0 = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    P5 = 5
    P6 = 6
    P7 = 7
    P8 = 8
    P9 = 9
    P10 = 10
    P11 = 11
    P12 = 12
    P13 = 13
    P14 = 14
    P15 = 15
    P16 = 16
    P17 = 17
    P18 = 18
    P19 = 19
    P20 = 20
    P21 = 21
    P22 = 22
    P23 = 23
    P24 = 24
    P25 = 25
    P26 = 26
    P27 = 27
    P28 = 28
    P29 = 29
    P30 = 30
    P31 = 31
    P32 = 32
    P33 = 33
    P34 = 34
    P35 = 35
    P36 = 36
    P37 = 37
    P38 = 38
    P39 = 39
    P40 = 40
    P41 = 41
    P42 = 42
    P43 = 43
    P44 = 44
    P45 = 45
    P46 = 46
    P47 = 47
    P48 = 48
    P49 = 49
    P50 = 50
    P51 = 51
    P52 = 52
    P53 = 53
    P54 = 54
    P55 = 55
    P56 = 56


Registers = ArchRegisters | PhysicalRegisters


class RegisterFile:
    __registers = None
    __rat = []  # idx is arch reg, value is physical
    __available_reg: Deque[int] = deque()

    def __new__(cls, ):
        if cls.__registers is None:
            cls.__registers = super(RegisterFile, cls).__new__(cls)
        return cls.__registers

    def __init__(self):
        self.__registers = [0] * len(PhysicalRegisters)
        self.__rat = list(range(len(ArchRegisters)))
        self.__available_reg = deque(range(len(ArchRegisters), len(PhysicalRegisters)))

    def alias_register(self, arch: ArchRegisters) -> PhysicalRegisters:
        # free the physical reg that is currently there
        self.__available_reg.append(self.__rat[arch])
        reg = self.__available_reg.popleft()
        # alias it to a new one
        self.__rat[arch] = reg
        return PhysicalRegisters(reg)

    def get_rat(self) -> List[int]:
        return self.__rat

    def print_physica_register_file(self, time: int | None = None):
        if time is not None:
            print(f"Register file at t={time}")
        else:
            print("Register File")

        for (idx, val) in enumerate(self.__registers):
            name = PhysicalRegisters(idx).name
            print(f"{name} \t {val}")

    def print_register_file(self, time: int | None = None):
        if time is not None:
            print(f"Register file at t={time}")
        else:
            print("Register File")

        for idx in ArchRegisters:
            name = ArchRegisters(idx).name
            phys = self.__rat[idx]
            val = self.__registers[phys]
            print(f"{name} (P{phys}) \t {val}")

    def get_register_value(self, register: ArchRegisters) -> int:
        print(f"\t getting register {PhysicalRegisters(register).name} at index {register}")
        return self.__registers[register]

    def set_register_value(self, register: PhysicalRegisters, new_val: int):
        self.__registers[register] = new_val
