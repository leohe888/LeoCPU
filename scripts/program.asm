MOV SS, 1
MOV SP, 0X20
JMP START

show:
    MOV D, 255
    RET

start:
    MOV C, 0

increase:
    INC C
    MOV D, C
    call show
    JMP increase

    HLT
