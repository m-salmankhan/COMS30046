# COMS30046 Coursework --- Advanced Computer Architecture

Building a pipelined, superscalar processor simulator.

## To run:

```bash

python main.py [/path/to/assembly/file/] -s [speed]

```
The speed is a delay after each `tick()`, to give you time to read the output. Default: 0

## To-do: 
- Make more complex programs to use as benchmarks:
  - Gaussian blur with CONV2D - has nested loops so good to test branch prediction. Also has real data dependencies that would benefit from result forwarding. Also really important for AI inference, so is a nice "real-life" benchmark
  - Sorting algorithm
- Simulate a source of entropy to add RNG instruction for encryption algorithms
- Properly document ISA
- Fix output mechanism
  - Instead of printing new lines to terminal, make it replace what was on screen.
- Add OOO
- Make superscalar T_T

## ISA

### Registers
14 General Purpose Registers, named R0 to R13.

### Instructions (incomplete)


| Instruction   | Pseudo-format               |
| --------------|-----------------------------|
|`AND dest x y` | `REG[dest] = REG[x] ∧ REG[y]`|
|`OR dest x y`  | `REG[dest] = REG[x]  REG[y]`|

