import os
import pin
import assembly as ASM

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'micro.bin')

micro = [pin.HLT for _ in range(0x10000)]   # 微程序控制器的 ROM 要存放的内容

def compile_addr2(addr, ir, psw, index):
    global micro

    op = ir & 0xf0
    amd = (ir >> 2) & 3 # 目的操作数的寻址方式
    ams = ir & 3        # 源操作数的寻址方式

    INST = ASM.INSTRUCTIONS[2]
    if op not in INST:
        micro[addr] = pin.CYC
        return
    am = (amd, ams)
    if am not in INST[op]:
        micro[addr] = pin.CYC
        return
    EXEC = INST[op][am]
    if index < len(EXEC):
        micro[addr] = EXEC[index]
    else:
        micro[addr] = pin.CYC

def compile_addr1(addr, ir, psw, index):
    pass

def compile_addr0(addr, ir, psw, index):
    global micro

    op = ir

    INST = ASM.INSTRUCTIONS[2]
    if op not in INST:
        micro[addr] = pin.CYC
        return
    EXEC = INST[op]
    if index < len(EXEC):
        micro[addr] = EXEC[index]
    else:
        micro[addr] = pin.CYC

# 遍历 ROM 的每一个地址，地址位宽为 16 位，第 0 位到第 3 位为微指令周期数，第 4 位到第 7 位为 PSW，第 8 位到第 15 位为 IR。
for addr in range(0x10000):
    ir = addr >> 8
    psw = (addr >> 4) & 0xf
    cyc = addr & 0xf

    if cyc < len(ASM.FETCH):
        micro[addr] = ASM.FETCH[cyc]
        continue

    addr2 = ir & (1 << 7)
    addr1 = ir & (1 << 6)

    index = cyc- len(ASM.FETCH)

    if addr2:   # 二地址指令
        compile_addr2(addr, ir, psw, index)
    elif addr1: # 一地址指令
        compile_addr1(addr, ir, psw, index)
    else:       # 零地址指令
        compile_addr0(addr, ir, psw, index)

with open(filename, 'wb') as file:
    for var in micro:
        value = var.to_bytes(4, 'little')
        file.write(value)

print("Compile micro instruction finish!!!")