from typing import List

import alu
import registers
import clock
import control
import memory
import writeback
from src.base_instruction import BaseInstruction

class Processor:
    def __init__(self, clock_speed: int, preload: List[BaseInstruction | int]):
        self.register_file = registers.RegisterFile()
        self.write_back = writeback.WriteBack()
        self.clock = clock.Clock(clock_speed)

        self.memory_unit = memory.Memory(self.register_file, self.write_back)
        self.alu = alu.ALU(self.register_file, self.write_back)
        self.control_unit = control.Control(self.alu, self.memory_unit, self.register_file)

        # load instructions and data to memory
        self.preload_memory(preload)

    def preload_memory(self, data: List[BaseInstruction | int]):
        for (idx, item) in enumerate(data):
            self.memory_unit.set(idx, item)

    def run(self):
        while True:
            # write-back stage
            self.write_back.write()

            # memory stage
            self.memory_unit.exec_memory_actions()

            # execute stage
            pc_changed, halted = self.control_unit.execute()
            self.alu.execute()
            self.memory_unit.execute()

            # if there has been a branch or HALT instruction, throw away the fetched instruction
            # so that it isn't decoded on the next cycle
            if pc_changed or halted:
                self.control_unit.update_ir(None)
                continue
            # the decoded result would be the instruction in the IR which now needs to be abandoned
            else:
                self.control_unit.decode()
                self.control_unit.instruction_fetch()

            # tick
            self.clock.tick()

            # Print Register File
            self.register_file.print_register_file(self.clock.get_time())
