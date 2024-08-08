from abc import ABCMeta, abstractmethod
from typing import List

from src import registers


class BaseInstruction(metaclass=ABCMeta):
    @abstractmethod
    def get_dest(self) -> registers.Registers | None:
        pass

    @abstractmethod
    def get_sources(self) -> List[registers.Registers]:
        pass

    @abstractmethod
    def update_source_registers(self, rat: List[int]):
        pass

    @abstractmethod
    def update_dest(self, new: registers.PhysicalRegisters):
        pass
