from typing import List

import alu
import registers
import clock
import control
import memory
import writeback
from src import flags
from src.base_instruction import BaseInstruction


class Processor:
    def __init__(self, clock_speed: int, preload: List[BaseInstruction | int]):
        self.register_file = registers.RegisterFile()
        self.write_back = writeback.WriteBack()
        self.clock = clock.Clock(clock_speed)

        self.memory_unit = memory.Memory(self.register_file, self.write_back, self.clock)
        self.alu = alu.ALU(self.register_file, self.write_back, self.clock, self.memory_unit)
        self.control_unit = control.Control(self.alu, self.memory_unit, self.register_file, self.clock, self.write_back)

        # load instructions and data to memory
        self.preload_memory(preload)

    def preload_memory(self, data: List[BaseInstruction | int]):
        for (idx, item) in enumerate(data):
            self.memory_unit.set(idx, item)

    def run(self):
        halted = False
        inst_count = 0
        should_continue_after_halt = False

        num_mispredicts = 0
        num_branches = 0

        while (not halted) or should_continue_after_halt:
            # check hazards
            is_branch, was_jmp = self.control_unit.check_hazards()
            if is_branch:
                num_branches += 1

            # write-back stage
            self.write_back.write()

            # tick after every pipeline stage to simulate un-pipelined execution
            if not flags.pipeline:
                self.clock.tick()

            # memory stage
            self.memory_unit.exec_memory_actions()

            if not flags.pipeline:
                self.clock.tick()

            # only memory and wb can happen after a halt has been executed
            if not halted:
                # execute stage
                executed_cu, pc_changed, halted = self.control_unit.execute()
                executed_alu = self.alu.execute()
                executed_mem = self.memory_unit.execute()

                if not flags.pipeline:
                    self.clock.tick()

                inst_count = inst_count + executed_cu + executed_alu + executed_mem

                # if there has been a branch or HALT instruction, throw away the fetched instruction
                # so that it isn't decoded on the next cycle
                if pc_changed or halted:
                    # the decoded result would be the instruction in the IR which now needs to be abandoned
                    self.control_unit.update_ir(None)
                    self.control_unit.decode()

                    # if the PC was changed in the EX stage, it means that a Branch instruction changed the PC
                    # since we predict that conditions are always false (i.e. no branch will happen), we mispredicted
                    num_mispredicts += 1 if pc_changed else 0
                    continue

                else:
                    self.control_unit.decode()
                    if not flags.pipeline:
                        self.clock.tick()

                    # if there was a JMP that changed the PC, we still need to wait a cycle
                    # the fetch stage shouldn't see the PC update until next cycle
                    if not was_jmp:
                        self.control_unit.instruction_fetch()

            # tick -- this one happens in both pipelined and unpipelined
            self.clock.tick()

            # Print Register File
            print("----------------------")
            self.register_file.print_register_file(self.clock.get_time())
            print("----------------------")
            print("")

            # after a halt, we should let things further on from the execute stage (i.e. memory and writeback) finish
            # what they started
            should_continue_after_halt = (
                    (not self.memory_unit.is_available())
                    or self.memory_unit.is_mem_busy()
                    or (not self.write_back.is_available())
            )

        print(f"Executed {inst_count} instructions in {self.clock.get_time()} cycles")
        print(f"Cycles per Instruction: {self.clock.get_time() / inst_count}")
        if num_branches != 0:
            print(f"Branch mispredicts: {num_mispredicts}/{num_branches} ({100 - 100*num_mispredicts/num_branches}% correct)")
