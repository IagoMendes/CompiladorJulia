SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss 
res RESB 1

section .text
global _start

print : ; subrotina print
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer
MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
XOR ESI , ESI

print_dec : ; empilha todos os digitos
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0 '
PUSH EDX
INC ESI ; contador de digitos
CMP EAX, 0
JZ print_next ; quando acabar pula
JMP print_dec

print_next :
CMP ESI , 0
JZ print_exit ; quando acabar de imprimir
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [res] , ECX
MOV ECX, res
MOV EDX, 1
INT 0x80
JMP print_next

print_exit :
POP EBP
RET

; subrotinas if / while
binop_je :
JE binop_true
JMP binop_false

binop_jg :
JG binop_true
JMP binop_false

binop_jl :
JL binop_true
JMP binop_false

binop_false :
MOV EBX, False
JMP binop_exit

binop_true :
MOV EBX, True

binop_exit :
RET

_start :
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

PUSH DWORD 0
NOP
PUSH DWORD 0
NOP
PUSH DWORD 0
NOP
NOP
MOV EBX, 2
MOV [EBP-4], EBX
NOP
MOV EBX, 5
MOV [EBP-8], EBX
NOP
MOV EBX, 1
MOV [EBP-12], EBX
NOP
NOP
loop_24: ;
MOV EBX, [EBP - 4]
PUSH EBX
MOV EBX, [EBP - 8]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
POP EAX
CMP EAX, EBX
CALL binop_jl
CMP EBX, False ;
JE exit_24 ;
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, [EBP - 4]
POP EAX
IMUL EBX
MOV EBX, EAX
MOV [EBP-12], EBX
NOP
MOV EBX, [EBP - 4]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-4], EBX
NOP
JMP loop_24 ;
exit_24: ;
NOP
MOV EBX, [EBP - 12]
PUSH EBX
CALL print
POP EBX
NOP
NOP
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, 120
POP EAX
CMP EAX, EBX
CALL binop_jg
CMP EBX, False
JE exit_44
MOV EBX, [EBP - 12]
PUSH EBX
CALL print
POP EBX
NOP
exit_44: ;
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, 120
POP EAX
CMP EAX, EBX
CALL binop_jg
CMP EBX, False
JNE exit_else_44
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, 120
POP EAX
CMP EAX, EBX
CALL binop_je
CMP EBX, False
JE exit_52
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, 2
POP EAX
ADD EAX, EBX
MOV EBX, EAX
PUSH EBX
CALL print
POP EBX
NOP
exit_52: ;
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, 120
POP EAX
CMP EAX, EBX
CALL binop_je
CMP EBX, False
JNE exit_else_52
MOV EBX, [EBP - 12]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
PUSH EBX
CALL print
POP EBX
NOP
exit_else_52: ;
exit_else_44: ;
; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
