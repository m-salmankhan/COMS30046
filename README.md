# COMS30046 Coursework --- Advanced Computer Architecture

Building a pipelined, superscalar processor simulator.

## ISA

### Registers
14 General Purpose Registers, named R0 to R13.

### Instructions

#### Bitwise AND

| Instruction   | Pseudo-format                |
| --------------|------------------------------|
|`AND dest x y` | `REG[dest] = REG[x] ∧ REG[y]`|
|`OR dest x y`  | `REG[dest] = REG[x] ∧ REG[y]`|

