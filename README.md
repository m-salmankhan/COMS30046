# COMS30046 Coursework --- Advanced Computer Architecture

Building a pipelined, superscalar processor simulator.

## To run:

```bash

python main.py [/path/to/assembly/file/] -s [speed]

```
The speed is a delay after each `tick()`, to give you time to read the output. Default: 0

## To-do: 
- Make more complex programs to use as benchmarks
- Simulate a source of entropy to add RNG instruction for encryption algorithms
- Properly document ISA
- Fix output mechanism
  - Instead of printing new lines to terminal, make it replace what was on screen.
- Make superscalar T_T

## ISA

### Registers
14 General Purpose Registers, named R0 to R13.

### Instructions (incomplete)


| Instruction   | Pseudo-format               |
| --------------|-----------------------------|
|`AND dest x y` | `REG[dest] = REG[x] ∧ REG[y]`|
|`OR dest x y`  | `REG[dest] = REG[x]  REG[y]`|

