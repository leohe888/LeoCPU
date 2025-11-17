MOV SS, 1
MOV SP, 0X20
JMP START

show:
    MOV D, 255
    IRET

start:
    MOV C, 0

increase:
    INC C
    MOV D, C
    INT show
    JMP increase

    HLT
