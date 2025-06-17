; vector_swap.asm
; Programa para inverter um vetor de 7 inteiros in-place.

START:
    ; Carregar o endereço do vetor em R0
    JMP R0, VECTOR_START  ; R0 aponta para o início do vetor

    ; Inicializando os índices do vetor (início e fim)
    MOV R1, #0           ; R1 = índice inicial
    MOV R2, #6           ; R2 = índice final (6, pois temos 7 elementos)

LOOP:
    ; Carregar os valores de R1 e R2 para trocar os elementos
    MOV R3, [R0 + R1]    ; R3 = vetor[R1]
    MOV R4, [R0 + R2]    ; R4 = vetor[R2]

    ; Trocar os valores
    MOV [R0 + R1], R4    ; vetor[R1] = R4
    MOV [R0 + R2], R3    ; vetor[R2] = R3

    ; Atualizar os índices
    INC R1               ; R1++
    DEC R2               ; R2--

    ; Verificar se os índices se cruzaram
    CMP R1, R2           ; R1 == R2?
    JNE LOOP              ; Se não, continua o loop

    ; Fim do programa
    HALT

VECTOR_START:
    .DATA
    ; Vetor de 7 inteiros
    .WORD 10, 20, 30, 40, 50, 60, 70  ; Inicialização do vetor
