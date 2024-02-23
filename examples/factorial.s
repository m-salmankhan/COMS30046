; -----------------------------------------
; calculate factorial(input)
; --------------------------------------

; Load input into r0
; TODO: add a MOV instruction
LDWIC r0 input
; Set r1 to 1 (initial value of accumulator)
NOP
NOP
NOP
NOP
NOP
ADDI r1 r1 0x1 ; REG[r1] <- 1
NOP
NOP
NOP
NOP
NOP

loop:
MUL r1 r1 r0 ; REG[r1] <- REG[r1] * REG[r0]
NOP
NOP
NOP
NOP
NOP
SUBI r0 r0 0x1 ; REG[r0] <- REG[r0] - 1
NOP
NOP
NOP
NOP
NOP
GT r3 r0 r13 ; REG[r3] <- REG[r0] > r13 (=0)
NOP
NOP
NOP
NOP
NOP
BRATI r3 loop ; if REG[r3] then goto loop
HALT
NOP
NOP
NOP
input:
0xA
