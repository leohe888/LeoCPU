import pin

# 取指微程序
FETCH = [
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.IR_IN | pin.PC_INC,
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.DST_IN | pin.PC_INC,
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.SRC_IN | pin.PC_INC,
]

MOV = (0 << pin.ADDR2_SHITF) | pin.ADDR2
ADD = (1 << pin.ADDR2_SHITF) | pin.ADDR2
SUB = (2 << pin.ADDR2_SHITF) | pin.ADDR2
CMP = (3 << pin.ADDR2_SHITF) | pin.ADDR2
AND = (4 << pin.ADDR2_SHITF) | pin.ADDR2
OR = (5 << pin.ADDR2_SHITF) | pin.ADDR2
XOR = (6 << pin.ADDR2_SHITF) | pin.ADDR2

INC = (0 << pin.ADDR1_SHITF) | pin.ADDR1
DEC = (1 << pin.ADDR1_SHITF) | pin.ADDR1

NOT = (2 << pin.ADDR1_SHITF) | pin.ADDR1

JMP = (3 << pin.ADDR1_SHITF) | pin.ADDR1

JO = (4 << pin.ADDR1_SHITF) | pin.ADDR1
JNO = (5 << pin.ADDR1_SHITF) | pin.ADDR1
JZ  = (6 << pin.ADDR1_SHITF) | pin.ADDR1
JNZ = (7 << pin.ADDR1_SHITF) | pin.ADDR1
JP = (8 << pin.ADDR1_SHITF) | pin.ADDR1
JNP = (9 << pin.ADDR1_SHITF) | pin.ADDR1

PUSH = (10 << pin.ADDR1_SHITF) | pin.ADDR1
POP = (11 << pin.ADDR1_SHITF) | pin.ADDR1

NOP = 0
HLT = 0x3f

INSTRUCTIONS = {
    2: {
        MOV: {
            # MOV REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_W | pin.SRC_OUT,
            ],
            # MOV REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_W | pin.SRC_R
            ],
            # MOV REG, [MEM]
            (pin.AM_REG, pin.AM_DIR): [
                pin.SRC_OUT | pin.MAR_IN,
                pin.DST_W | pin.RAM_OUT
            ],
            # MOV REG, [REG]
            (pin.AM_REG, pin.AM_RAM): [
                pin.SRC_R | pin.MAR_IN,
                pin.DST_W | pin.RAM_OUT
            ],
            # MOV [MEM], IMM
            (pin.AM_DIR, pin.AM_INS): [
                pin.DST_OUT | pin.MAR_IN,
                pin.RAM_IN | pin.SRC_OUT
            ],
            # MOV [MEM], REG
            (pin.AM_DIR, pin.AM_REG): [
                pin.DST_OUT | pin.MAR_IN,
                pin.RAM_IN | pin.SRC_R
            ],
            # MOV [MEM], [MEM]
            (pin.AM_DIR, pin.AM_DIR): [
                pin.SRC_OUT | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_OUT | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ],
            # MOV [MEM], [REG]
            (pin.AM_DIR, pin.AM_RAM): [
                pin.SRC_R | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_OUT | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ],
            # MOV [REG], IMM
            (pin.AM_RAM, pin.AM_INS): [
                pin.DST_R | pin.MAR_IN,
                pin.RAM_IN | pin.SRC_OUT
            ],
            # MOV [REG], REG
            (pin.AM_RAM, pin.AM_REG): [
                pin.DST_R | pin.MAR_IN,
                pin.RAM_IN | pin.SRC_R
            ],
            # MOV [REG], [MEM]
            (pin.AM_RAM, pin.AM_DIR): [
                pin.SRC_OUT | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_R | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ],
            # MOV [REG], [REG]
            (pin.AM_RAM, pin.AM_RAM): [
                pin.SRC_R | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_R | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ]
        },
        ADD: {
            # ADD REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_ADD | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            # ADD REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_ADD | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        SUB: {
            # SUB REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_SUB | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            # SUB REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_SUB | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        CMP: {
            # CMP REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_SUB | pin.ALU_PSW    # 只更新 PSW
            ],
            # CMP REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_SUB | pin.ALU_PSW    # 只更新 PSW
            ],
        },
        AND: {
            # AND REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_AND | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            # AND REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_AND | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        OR: {
            # OR REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_OR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            # OR REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_OR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        XOR: {
            # XOR REG, IMM
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_XOR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            # XOR REG, REG
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_XOR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        }
    },
    1: {
        INC: {
            # INC REG
            pin.AM_REG: [
                pin.DST_R | pin.A_IN,
                pin.OP_INC | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ]
        },
        DEC: {
            # DEC REG
            pin.AM_REG: [
                pin.DST_R | pin.A_IN,
                pin.OP_DEC | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ]
        },
        NOT: {
            # NOT REG
            pin.AM_REG: [
                pin.DST_R | pin.A_IN,
                pin.OP_NOT | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ]
        },
        JMP: {
            # JMP IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        JO: {
            # JO IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        JNO: {
            # JNO IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        JZ: {
            # JZ IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        JNZ: {
            # JNZ IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        JP: {
            # JP IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        JNP: {
            # JNP IMM
            pin.AM_INS: [
                pin.DST_OUT | pin.PC_IN,
            ]
        },
        PUSH: {
            # PUSH INS
            pin.AM_INS: [
                pin.SP_OUT | pin.A_IN,
                pin.OP_DEC | pin.SP_IN | pin.ALU_OUT,
                pin.SP_OUT | pin.MAR_IN,
                pin.SS_OUT | pin.MSR_IN,
                pin.DST_OUT | pin.RAM_IN,
                pin.CS_OUT | pin.MSR_IN,
            ],
            # PUSH REG
            pin.AM_REG: [
                pin.SP_OUT | pin.A_IN,
                pin.OP_DEC | pin.SP_IN | pin.ALU_OUT,
                pin.SP_OUT | pin.MAR_IN,
                pin.SS_OUT | pin.MSR_IN,
                pin.DST_R | pin.RAM_IN,
                pin.CS_OUT | pin.MSR_IN,
            ],
        },
        POP: {
            # POP REG
            pin.AM_REG: [
                pin.SP_OUT | pin.MAR_IN,
                pin.SS_OUT | pin.MSR_IN,
                pin.DST_W | pin.RAM_OUT,
                pin.SP_OUT | pin.A_IN,
                pin.OP_INC | pin.SP_IN | pin.ALU_OUT,
                pin.CS_OUT | pin.MSR_IN,
            ]
        }
    },
    0: {
        NOP: [
            pin.CYC,
        ],
        HLT: [
            pin.HLT,
        ]
    }
}
