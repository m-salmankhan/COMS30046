from enum import Enum

import alu
import control
import memory


class Instructions(Enum):
    BitWiseAnd = ("AND", alu.BitWiseAnd)
    BitWiseOr = ("OR", alu.BitWiseOr)
    BitWiseXOr = ("XOR", alu.BitWiseXOr)
    BitWiseNot = ("NOT", alu.BitWiseNot)
    ADDITION = ("ADD", alu.Add)
    ADDITION_IMMEDIATE = ("ADDI", alu.AddImmediate)
    SUBTRACT = ("SUB", alu.Subtract)
    SUBTRACT_IMMEDIATE = ("SUBI", alu.SubtractImmediate)
    LESSER_THAN = ("LT", alu.LesserThan)
    GREATER_THAN = ("GT", alu.GreaterThan)
    EQUAL_TO = ("EQ", alu.EqualTo)
    MULTIPLY = ("MUL", alu.Multiply)
    MULTIPLY_IMMEDIATE = ("MULI", alu.MultiplyImmediate)
    DIVISION = ("DIV", alu.Divide)
    LEFT_SHIFT = ("LSHIFT", alu.LeftShift)
    LEFT_SHIFT_IMMEDIATE = ("LSHIFTI", alu.LeftShiftImmediate)
    RIGHT_SHIFT = ("RSHIFT", alu.RightShift)
    RIGHT_SHIFT_IMMEDIATE = ("RSHIFTI", alu.RightShiftImmediate)
    JUMP_ABSOLUTE = ("JMP", control.JumpAbsolute)
    JUMP_RELATIVE = ("JMPA", control.JumpRelative)
    JUMP_ABSOLUTE_IMMEDIATE = ("JMPAI", control.JumpAbsoluteImmediate)
    JUMP_RELATIVE_IMMEDIATE = ("JMPI", control.JumpRelativeImmediate)
    BRANCH_ABSOLUTE_TRUE = ("BRAT", control.BranchAbsoluteTrue)
    BRANCH_RELATIVE_TRUE = ("BRT", control.BranchRelativeTrue)
    BRANCH_RELATIVE_TRUE_IMMEDIATE = ("BRT", control.BranchRelativeTrueImmediate)
    BRANCH_ABSOLUTE_TRUE_IMMEDIATE = ("BRATI", control.BranchAbsoluteTrueImmediate)
    LOAD_WORD = ("LDW", memory.LoadWord)
    LOAD_WORD_IMMEDIATE = ("LDWI", memory.LoadWordImmediate)
    LOAD_WORD_CONSTANT = ("LDWC", memory.LoadWordConstant)
    LOAD_WORD_CONSTANT_IMMEDIATE = ("LDWIC", memory.LoadWordConstantImmediate)
    STORE_WORD_CONSTANT = ("STWC", None)
    STORE_WORD_CONSTANT_IMMEDIATE = ("STWCI", memory.StoreWord)
    STORE_WORD = ("STW", memory.StoreWord)
    STORE_WORD_IMMEDIATE = ("STWI", memory.StoreWordImmediate)
    HALT = ("HALT", control.Halt)
    NO_OP = ("NOP", control.NoOp)


"""
MEMORY:
	- LDW dest base offset (reg[dest] = [mem+offset])
	- LDW dest base #IMMEDIATE (reg[dest] = [mem+{offset}])
	- LDWC dest x (dest = MEM[x])
	- LDIC dest #IMMEDIATE (dest = {immediate})
	- STW dest x (MEM[dest] = x)

	
CONTROL:
	- JMPA x (PC = reg[x])
	- JMP x (PC = PC + reg[x]
	- JMPI #IMMEDIATE (PC = PC + {immediate}
	- JMPAI #IMMEDIATE (PC = {immediate}
	
	- BRAT x y (if reg[x]then  PC = reg[y])
	- BRATI x #IMMEDIATE (if x PC = {immediate}
	- BRT x y (if reg[x] then PC=PC+reg[y])
	- BRTI x #IMMEDIATE (if reg[x] then PC=PC+{immediate})
	
	- HALT
"""