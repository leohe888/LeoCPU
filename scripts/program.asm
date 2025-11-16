; MOV C, 5
; MOV D, C
; MOV D, [5]
; MOV A, 6
; MOV D, [A]

; MOV [0x2f], 5

; MOV [0x2e], 18
; MOV [0x2f], [0x2e]

; MOV [0X18], 0XFE
; MOV C, 0X18
; MOV [0x2f], C

; MOV C, 0X18
; MOV D, 0X33
; MOV [C], D

; MOV [0X30], 0XDD
; MOV C, 0X18
; MOV [C], [0X30]

MOV [0X30], 0XEE
MOV D, 0X30
MOV C, 0X18
MOV [C], [D]

HLT