;=================================================
;==== Add 1 to number labeled by input ===========
;=================================================

; load input arg into r0
LDWIC r0 input
; load value for halt flag 
LDWIC r10 halt

; halts to make sure there's no data dependencies
NOP
NOP

; add 1 to input and store in r1
ADDI r1 r0 1
; halt
HALT r10
NOP
NOP
NOP

input:
0x9
halt:
0x1
