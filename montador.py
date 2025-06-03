import os


#precisa ter um arquivo.asm ja pronto com as instruções
with open('program.asm', 'r') as f:
  content = f.read()
p = content.upper().split('\n')


memory = 256 * ['00']

instrucoes = {'ADD':0b1000, 'SR':0b1001, 'SL':0b1010, 'NOT':0b1011, 'AND':0b1100, 'OR':0b1101, 'XOR':0b1110,'CMP':0b1111,'LD':0b0,
              'ST':0b1,'DATA':0b10,'JMPR':0b11,'JMP':0b100,'JMPCAEZ':0b101,'CLF':0b110} 
registradores = {'R0':0b0, 'R1':0b1, 'R2':0b10,'R3':0b11}



memory[0] = '7c'
memory[1] = '7a'
memory [2] = '7b'
memory[3] = '7d'
for i, linha in enumerate(p):
  if not linha.strip():
    continue
  partes = linha.strip()

  instrucao = partes[0]

  if instrucao not in instrucoes
hexadecimal = hex(int(binario, 2))






with open('program.txt', 'w') as f:
  f.write('v3.0 hex words plain')
  f.write(memory[0])
  f.write('\n')
  f.write(memory[1])


#aqui e o codigo do chat
# Dicionários de instruções e registradores
instrucoes = {
    'ADD': 0b1000, 'SR': 0b1001, 'SL': 0b1010, 'NOT': 0b1011,
    'AND': 0b1100, 'OR': 0b1101, 'XOR': 0b1110, 'CMP': 0b1111,
    'LD': 0b0, 'ST': 0b1, 'DATA': 0b10, 'JMPR': 0b11, 'JMP': 0b100,
    'JMPCAEZ': 0b101, 'CLF': 0b110
}

registradores = {
    'R0': 0b00, 'R1': 0b01, 'R2': 0b10, 'R3': 0b11
}

# Inicializar a memória (256 posições de memória com valor inicial '00')
memory = ['00'] * 256

# Ler o arquivo .asm
with open('program.asm', 'r') as f:
    content = f.read()

# Dividir o conteúdo em linhas
p = content.upper().split('\n')

# Processar cada linha
for i, linha in enumerate(p):
    # Ignorar linhas vazias
    if not linha.strip():
        continue

    # Separar a linha em instrução e operandos
    partes = linha.split()

    # Obter a instrução
    instrucao = partes[0]

    # Verificar se a instrução é válida
    if instrucao not in instrucoes:
        print(f"Instrução desconhecida: {instrucao}")
        continue

    # Pegar o código binário da instrução
    codigo_binario = instrucoes[instrucao]

    # Verificar se há operandos
    if len(partes) > 1:
        operandos = partes[1:]
    else:
        operandos = []

    # Caso de instrução + registradores (2 operandos)
    if len(operandos) == 2:
        # Verificar se ambos os operandos são registradores
        if operandos[0] in registradores and operandos[1] in registradores:
            # Combinar o código binário da instrução com os registradores
            # A ideia é combinar o código binário da instrução com os valores dos registradores.
            # Vamos fazer um shift de 2 bits para cada registrador e combinar.
            r1 = registradores[operandos[0]]  # Registrador 1
            r2 = registradores[operandos[1]]  # Registrador 2
            
            # A instrução (4 bits) será seguida pelos dois registradores (2 bits cada)
            codigo_binario = (codigo_binario << 4) | (r1 << 2) | r2  # Shift de 2 bits para os registradores
            
        else:
            print(f"Erro: Operandos não são registradores válidos: {operandos}")
            continue

    # Caso de instrução sem operandos ou outro tipo de operação
    elif len(operandos) == 1:
        # Pode ser que seja um valor imediato ou algum tipo de instrução com apenas um operando.
        pass

    # Converter o código binário para hexadecimal
    hex_valor = hex(codigo_binario)[2:].upper()  # Remove o prefixo '0x' e converte para maiúsculas

    # Preencher com 2 dígitos hexadecimais se necessário
    hex_valor = hex_valor.zfill(2)

    # Armazenar o valor hexadecimal na memória
    memory[i] = hex_valor

# Exibir a memória em formato hexadecimal
for i in range(len(memory)):
    print(f"Endereço {i:03}: {memory[i]}")
