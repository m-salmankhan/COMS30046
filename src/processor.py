"""
Start processor with program and data already loaded in memory
Clock time = 0

Fetch Next Instruction & Increment PC (modifies PC and IR)

Tick()

Fetch Next Instruction & Increment PC (modifies PC and IR)

Decode Instruction (i.e. look at instruction and call ALU.give_instruction() or Memory.give_instruction() etc. i.e.
                    Decide which unit needs to execute it)
                    (modifies unit's individual registers, only one at a time, though)

Tick()

Fetch Next Instruction & Increment PC (modifies PC and IR)

Decode (modifies unit's individual registers, only one at a time, though)

Execute Instruction (call Unit.Execute for each unit)
                     Only one of the units should have an instruction in them at each time(?) fact-check this
                     (modifies either MemoryActionBuffer and WriteBackActionBuffer)


Tick()

Fetch Next Instruction & Increment PC (modifies PC and IR)

Decode (modifies unit's individual registers, only one at a time, though)

Execute Instruction (modifies either MemoryActionBuffer and WriteBackActionBuffer)

Run Memory actions (action dispatched to the memory unit during the execution stage) (Modifies WriteBackActionBuffer)

Tick()

Fetch Next Instruction & Increment PC (modifies PC and IR)

Decode (modifies unit's individual registers, only one at a time, though)

Execute Instruction (modifies either MemoryActionBuffer and WriteBackActionBuffer)

Run Memory actions (Modifies WriteBackActionBuffer)

Run WriteBack actions (action dispatched to WriteBack during execution or memory stages)

"""
import alu
import registers
import clock
import control
import memory
import writeback


class Processor:
    def __init__(self, clock_speed: int):
        self.register_file = registers.RegisterFile()
        self.write_back = writeback.WriteBack()
        self.clock = clock.Clock(clock_speed)

        self.memory_unit = memory.Memory(self.register_file, self.write_back)
        self.alu = alu.ALU(self.register_file, self.write_back)
        self.control_unit = control.Control(self.alu, self.memory_unit, self.register_file)

    def run(self):
        while True:
            # fetch
            fetch_results = self.control_unit.instruction_fetch()

            # decode
            decode_results = self.control_unit.decode()

            # execute -- only one of these should have any instructions to execute each cycle
            control_execute_results = self.control_unit.execute()
            alu_execute_results = self.alu.execute()
            memory_execute_results = self.memory_unit.execute()

            # memory
            memory_results = self.memory_unit.exec_memory_actions()

            # write-back
            write_back_results = self.write_back.write()

            # Apply results
            # only apply decoded changes if the instruction that finished executing wasn't a branch
            # if it's a branch, the decoded instruction needs to be discarded.
            if control_execute_results is None or control_execute_results.pc is None:
                if fetch_results is not None:
                    fetch_results.apply()

                if decode_results is not None:
                    decode_results.apply()
            else:
                # clean decode unit of instruction that it was about to decode
                self.control_unit.update_ir(None)

            if control_execute_results is not None:
                control_execute_results.apply()

            if alu_execute_results is not None:
                alu_execute_results.apply()

            if memory_execute_results is not None:
                memory_execute_results.apply()

            if memory_results is not None:
                memory_results.apply()

            if write_back_results is not None:
                write_back_results.apply()

            # tick
            self.clock.tick()


            # Print Register File
            self.register_file.print_register_file(self.clock.get_time())
