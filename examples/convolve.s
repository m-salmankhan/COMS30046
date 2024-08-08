; Initialize the base addresses
LDIC R1 matrix  ; Load base address of matrix into R1
LDIC R2 kernel  ; Load base address of kernel into R2
LDIC R3 output  ; Load base address of output into R3

; Convolution operation
LDIC R4 0x05     ; Load matrix size (5) into R4
LDIC R5 0x02     ; Load kernel size (2) into R5
LDIC R6 0x01     ; Load constant 1 into R6
LDIC R7 0x00     ; Initialize sum register (R7)

; Loop through each element of the matrix for convolution
LDIC R8 0x00     ; Initialize row index (i) to 0

outer_loop:
    LT R9 R8 R4     ; if i >= 5, exit loop
    BRTI R9 end     ; if R9 is true, jump to end

    LDIC R10 0x00   ; Initialize column index (j) to 0

    inner_loop:
        LT R11 R10 R4    ; if j >= 5, exit inner loop
        BRTI R11 next_row ; if R11 is true, jump to next_row

        ; Initialize sum for current element
        LDIC R7 0x00

        ; Convolution operation for current element
        LDIC R12 0x00  ; Initialize k index to 0

        conv_loop:
            LT R13 R12 R5   ; if k >= 2, exit loop
            BRTI R13 store_result ; if R13 is true, jump to store_result

            LDIC R14 0x00      ; Initialize l index to 0

            conv_inner_loop:
                LT R15 R14 R5  ; if l >= 2, exit inner loop
                BRTI R15 conv_next_k ; if R15 is true, jump to conv_next_k

                ; Calculate the address of matrix element (i + k, j + l)
                ADD R16 R8 R12   ; i + k
                MUL R16 R16 R4   ; (i + k) * 5
                ADD R16 R16 R10  ; (i + k) * 5 + j
                ADD R17 R16 R14  ; (i + k) * 5 + j + l

                LDW R18 R1 R17  ; Load matrix element into R18
                LDW R19 R2 R14  ; Load kernel element into R19

                MUL R20 R18 R19 ; Multiply matrix and kernel elements
                ADD R7 R7 R20   ; Add to sum

                ADDI R14 R14 0x01 ; l++
                JMP conv_inner_loop

            conv_next_k:
                ADDI R12 R12 0x01 ; k++
                JMP conv_loop

        store_result:
            ; Store the sum in the output matrix
            ADD R21 R8 R4   ; i * 5
            ADD R21 R21 R10 ; i * 5 + j
            STW R3 R21 R7   ; Store sum in output

            ADDI R10 R10 0x01 ; j++
            JMP inner_loop

    next_row:
        ADDI R8 R8 0x01 ; i++
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
