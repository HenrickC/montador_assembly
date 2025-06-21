; vector_swap.asm
; Inverte um vetor de 7 elementos (endereçado manualmente)

; Inicialização dos registradores
DATA R0 0x20     ; R0 = endereço base do vetor (ex: posição 0x20 na RAM)
DATA R1 0x00     ; R1 = índice inicial (i)
DATA R2 0x06     ; R2 = índice final   (j)

; Início do loop - endereço 0x06

; R3 = R0 + R1
ADD R3 R0
ADD R3 R1
LD R4 R3         ; R4 = vetor[i]

; R5 = R0 + R2
ADD R5 R0
ADD R5 R2
LD R6 R5         ; R6 = vetor[j]

; Troca os valores
ST R3 R6         ; vetor[i] = R6
ST R5 R4         ; vetor[j] = R4

; i++
DATA R7 0x01
ADD R1 R7

; j--
DATA R7 0xFF     ; -1 em 2's complemento
ADD R2 R7

; Verifica se i < j
CMP R1 R2
JAE 0x06         ; Se R1 < R2, continua o loop (salta para 0x06)

; Loop infinito simulando HALT
JMP 0x1C         ; Salto para o endereço dos dados para loop infinito

; Vetor começa no endereço 0x20 (usado acima como base do vetor)
; vetor = [10, 20, 30, 40, 50, 60, 70]
DATA R0 0x0A     ; 0x20
DATA R0 0x14     ; 0x21
DATA R0 0x1E     ; 0x22
DATA R0 0x28     ; 0x23
DATA R0 0x32     ; 0x24
DATA R0 0x3C     ; 0x25
DATA R0 0x46     ; 0x26
