; NONE OF THIS WORKS >,>
; Initialize the base addresses
LDWIC R0 matrix   ; Load base address of matrix into R0
LDWIC R1 kernel   ; Load base address of kernel into R1
LDWIC R2 output   ; Load base address of output into R2

; Convolution operation
LDWIC R3 0x05     ; Load matrix size (5) into R3
LDWIC R4 0x02     ; Load kernel size (2) into R4
LDWIC R5 0x00     ; Initialize sum register (R5)

; Initialize row index (i) to 0
LDWIC R6 0x00

; Loop through each row of the matrix for convolution
outer_loop:
    ; if i >= 5, exit loop
    LT R7 R6 R3
    BRATI R7 end

    ; Initialize column index (j) to 0
    LDWIC R8 0x00

    ; Iterate through each column
    inner_loop:
        ; if j >= 5, exit inner loop
        LT R9 R8 R3
        BRATI R9 next_row ; if R9 is true, jump to next_row

        ; Initialize sum for current element
        LDWIC R5 0x00

        ; Convolution operation for current element
        LDWIC R10 0x00  ; Initialize k index to 0

        conv_loop:
            LT R11 R10 R4   ; if k 0< 2, exit loop
            BRATI R11 store_result ; if R11 is true, jump to store_result

            LDWIC R12 0x00      ; Initialize l index to 0

            conv_inner_loop:
                LT R13 R12 R4  ; if l >= 2, exit inner loop
                BRATI R13 conv_next_k ; if R13 is true, jump to conv_next_k

                ; Calculate the address of matrix element (i + k, j + l)
                ADD R7 R6 R10   ; i + k
                MUL R7 R7 R3    ; (i + k) * 5
                ADD R7 R7 R8    ; (i + k) * 5 + j
                ADD R7 R7 R12   ; (i + k) * 5 + j + l

                LDW R9 R0 R7    ; Load matrix element into R9
                ADD R11 R10 R12 ; Calculate kernel offset
                LDW R13 R1 R11  ; Load kernel element into R13

                MUL R11 R9 R13  ; Multiply matrix and kernel elements
                ADD R5 R5 R11   ; Add to sum

                ADDI R12 R12 0x01 ; l++
                JMP conv_inner_loop

            conv_next_k:
                ADDI R10 R10 0x01 ; k++
                JMP conv_loop

        store_result:
            ; Store the sum in the output matrix
            MUL R7 R6 R3    ; i * 5
            ADD R7 R7 R8    ; i * 5 + j
            STW R2 R7 R5    ; Store sum in output

            ADDI R8 R8 0x01 ; j++
            JMP inner_loop

    next_row:
        ADDI R6 R6 0x01 ; i++
        JMP outer_loop

end:
    HALT

; Define the base addresses for matrix, kernel, and output
matrix:
0x01
0x02
0x03
0x04
0x05
0x06
0x07
0x08
0x09
0x0A
0x0B
0x0C
0x0D
0x0E
0x0F
0x10
0x11
0x12
0x13
0x14
0x15
0x16
0x17
0x18
0x19

kernel:
0x01
0x02
0x03
0x04

output:
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
0x00
