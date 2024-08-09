;=================================================================
;==== lots of ADDs with no branches or loads or stores ===========
;==== it has real data dependencies                    ===========
;=================================================================
ADDI r0 r0 1
ADDI r1 r0 1
ADDI r2 r1 1
ADDI r3 r2 1
ADDI r4 r3 1
ADDI r5 r4 1
ADDI r6 r5 1
HALT