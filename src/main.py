import argparse
import processor
from assembler import Assembler


def main(input_file: str, speed: int):
    # First parse the input file and load the program and data into memory
    assembler = Assembler(input_file)
    # Then run the processor
    a = processor.Processor(speed, assembler.assemble())
    a.run()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Run the simulator on a given assembly file")
    arg_parser.add_argument("input_file", type=str,
                            help="The assembly file you wish to execute in the simulator")

    arg_parser.add_argument("--speed", "-s", type=int, default=0,
                            help="The delay between ticks of the clock. A bigger number slows down the simulation.")

    args = arg_parser.parse_args()
    main(input_file=args.input_file, speed=args.speed)
