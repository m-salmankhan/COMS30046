import os
from pathlib import Path
from typing import List

import base_instruction
import instructions
import registers


class Assembler:

    # if input path is specified, text is loaded from file. Otherwise, it can be passed as a string.
    # if both are provided, it will ignore the string and use the file.
    def __init__(self, input_file: None | str = None, input_str: None | str = None):
        self.__labels = {}

        self.__input_path = Path(input_file) if input_file is not None else None
        self.__input_str = input_str

        if input_str is None and input_file is None:
            raise ValueError("Either an input string or an asm file must be provided.")

    def assemble(self) -> List[base_instruction.BaseInstruction | int]:
        assembled = []

        if self.__input_path is not None:
            with open(self.__input_path, "r") as fh:
                lines = fh.readlines()
        else:
            lines = self.__input_str.split(os.linesep)

        # remove comments
        lines = [x.split(";")[0] for x in lines]

        # remove empty lines
        lines = [x.strip() for x in lines if x.strip() != ""]

        # extract PC values for labels
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            colon_count = line.count(":")

            if colon_count > 1:
                raise Exception(
                    "Unrecognised syntax: multiple colons found. There can be only one label defined per line.")

            if colon_count == 1:
                [left, right] = line.split(":")

                if left in self.__labels:
                    raise Exception("Labels cannot be reused.")

                self.__labels[left] = idx

                if len(right) == 0:
                    del lines[idx]
                    idx -= 1
                else:
                    lines[idx] = right

            idx += 1

        # replace references to labels with extracted PC values
        labels_names = self.__labels.keys()
        for (idx, line) in enumerate(lines):
            for label_name in labels_names:
                a = label_name in line
                if a:
                    lines[idx] = line.replace(label_name, hex(self.__labels[label_name]))

        # convert to Instructions
        for (idx, line) in enumerate(lines):
            instruction = self.__parse_inst(lines, idx)

            assembled.append(instruction)

        return assembled

    def __parse_operands(self, instruction_name, segments: List[str], lines: List[str], line_num: int, num_regs: int,
                         num_immediate=0) -> List[registers.ArchRegisters | int]:

        num_operands = num_regs + num_immediate
        line = lines[line_num]

        if len(segments) - 1 > num_operands:
            raise Exception(
                f"{instruction_name} expects {num_operands} operands, but only {len(segments) - 1} given in \n\t {line}")
        try:
            reg_operands = [self.__parse_register(reg, lines, line_num) for reg in segments[1:num_regs + 1]]

            immediate_operands = [int(op, 16) for op in segments[num_regs + 1:num_regs + 1 + num_immediate]]
            return reg_operands + immediate_operands
        except IndexError:
            raise Exception(
                f"{instruction_name} expects {num_operands} operands, but only {len(segments) - 1} given in \n\t {line}")
        except ValueError:
            reg = " ".join(segments[num_regs + 1:num_regs + 1 + num_immediate])
            raise Exception(f"Error interpreting immediate values: {reg} in line \n\t {line}")

    def __parse_inst(self, lines: List[str], line_num: int) -> base_instruction.BaseInstruction | int:
        segments = lines[line_num].upper().split(" ")
        instruction = segments[0]

        if instruction == instructions.Instructions.BitWiseAnd.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.BitWiseAnd.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.BitWiseXOr.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.BitWiseXOr.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.BitWiseOr.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.BitWiseOr.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.BitWiseNot.value[0]:
            [dest, op1] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2)
            return instructions.Instructions.BitWiseNot.value[1](dest, op1)

        if instruction == instructions.Instructions.LogicalNot.value[0]:
            [dest, op1] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2)
            return instructions.Instructions.LogicalNot.value[1](dest, op1)

        if instruction == instructions.Instructions.ADDITION.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.ADDITION.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.ADDITION_IMMEDIATE.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2,
                                                     num_immediate=1)
            return instructions.Instructions.ADDITION_IMMEDIATE.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.SUBTRACT.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.SUBTRACT.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.SUBTRACT_IMMEDIATE.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2,
                                                     num_immediate=1)
            return instructions.Instructions.SUBTRACT_IMMEDIATE.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.MULTIPLY.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.MULTIPLY.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.MULTIPLY_IMMEDIATE.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2,
                                                     num_immediate=1)
            return instructions.Instructions.MULTIPLY_IMMEDIATE.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.GREATER_THAN.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.GREATER_THAN.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.LESSER_THAN.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.LESSER_THAN.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.EQUAL_TO.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.EQUAL_TO.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.LEFT_SHIFT.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.LEFT_SHIFT.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.LEFT_SHIFT_IMMEDIATE.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2,
                                                     num_immediate=1)
            return instructions.Instructions.LEFT_SHIFT_IMMEDIATE.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.RIGHT_SHIFT.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.RIGHT_SHIFT.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.RIGHT_SHIFT_IMMEDIATE.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2,
                                                     num_immediate=1)
            return instructions.Instructions.RIGHT_SHIFT_IMMEDIATE.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.DIVISION.value[0]:
            [dest, op1, op2] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.DIVISION.value[1](dest, op1, op2)

        if instruction == instructions.Instructions.JUMP_ABSOLUTE.value[0]:
            [addr] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=1)
            return instructions.Instructions.JUMP_ABSOLUTE.value[1](addr)

        if instruction == instructions.Instructions.JUMP_ABSOLUTE_IMMEDIATE.value[0]:
            [addr] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=0, num_immediate=1)
            return instructions.Instructions.JUMP_ABSOLUTE_IMMEDIATE.value[1](addr)

        if instruction == instructions.Instructions.BRANCH_ABSOLUTE_TRUE.value[0]:
            [cond, address] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2)
            return instructions.Instructions.BRANCH_ABSOLUTE_TRUE.value[1](cond, address)

        if instruction == instructions.Instructions.BRANCH_ABSOLUTE_TRUE_IMMEDIATE.value[0]:
            [cond, address] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=1, num_immediate=1)
            return instructions.Instructions.BRANCH_ABSOLUTE_TRUE_IMMEDIATE.value[1](cond, address)

        if instruction == instructions.Instructions.LOAD_WORD.value[0]:
            [dest, base, offset] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.LOAD_WORD.value[1](dest, base, offset)

        if instruction == instructions.Instructions.LOAD_WORD_IMMEDIATE.value[0]:
            [dest, base, offset] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2,
                                                         num_immediate=1)
            return instructions.Instructions.LOAD_WORD_IMMEDIATE.value[1](dest, base, offset)

        if instruction == instructions.Instructions.LOAD_WORD_CONSTANT.value[0]:
            [dest, addr] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2)
            return instructions.Instructions.LOAD_WORD_CONSTANT.value[1](dest, addr)

        if instruction == instructions.Instructions.LOAD_WORD_CONSTANT_IMMEDIATE.value[0]:
            [dest, addr] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=1, num_immediate=1)
            return instructions.Instructions.LOAD_WORD_CONSTANT_IMMEDIATE.value[1](dest, addr)

        if instruction == instructions.Instructions.STORE_WORD.value[0]:
            [addr, source] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=3)
            return instructions.Instructions.STORE_WORD.value[1](addr, source)

        if instruction == instructions.Instructions.STORE_WORD_IMMEDIATE.value[0]:
            [addr, source] = self.__parse_operands(instruction, segments, lines, line_num, num_regs=2, num_immediate=1)
            return instructions.Instructions.STORE_WORD_IMMEDIATE.value[1](addr, source)

        if instruction == instructions.Instructions.HALT.value[0]:
            return instructions.Instructions.HALT.value[1]()

        if instruction == instructions.Instructions.NO_OP.value[0]:
            return instructions.Instructions.NO_OP.value[1]()

        try:
            return int(segments[0], 16)
        except ValueError:
            raise Exception(f"Unrecognised Instruction \"{instruction}\" on line {line_num}:\n\t {lines[line_num]}")

    def __parse_register(self, name: str, lines: List[str], line_num: int) -> registers.ArchRegisters:
        try:
            return registers.ArchRegisters[name]
        except KeyError:
            raise Exception(f"Unrecognised Register {name} in \n\t{lines[line_num]}")

    def get_label(self, key):
        return self.__labels[key]