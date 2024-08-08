; -----------------------------------------
; calculate factorial(input)
; --------------------------------------

_start:
; Load input (n) into r0
LDWIC r0 input
; decrement r0 (we pre-initialise the start so it isn't needed)
SUBI r0 r0 0x1 ; REG[r0] <- REG[r0] - 1

; Set r1 to 1 (initial value of accumulator)
ADDI r1 r1 0x0 ; REG[r1] <- 0
ADDI r2 r2 0x1 ; REG[r2] <- 1

; 0 1 1 2 3 5
; r1: 0 1
; r2: 1


loop:
; r3 = r1+r2
ADD r3 r1 r2 ; REG[r1] <- REG[r1] + REG[r2]

; move r2 into r1
SUB r1 r1 r1 ; make r1 0 (r1 = r1-r1)
ADD r1 r1 r2 ; REG[r2] <- REG[r1] + REG[r2] ; r1 = r1 + r2 (=0+r2)

; move r3 into r2
SUB r2 r2 r2 ; make r2 0 (r2 = r2-r2)
ADD r2 r2 r3 ; REG[r2] <- REG[r2] + REG[r3] ; r2 = r2 + r3 (=0+r3)

; decrement r0
SUBI r0 r0 0x1 ; REG[r0] <- REG[r0] - 1

GT r3 r0 r13 ; REG[r3] <- REG[r0] > r13 (=0)

BRATI r3 loop ; if REG[r3] then goto loop

; reset r0 to 0
SUB r0 r0 r0

ADD r0 r0 r2

_end:
HALT



input:
0xFFF
