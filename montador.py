import os


#precisa ter um arquivo.asm ja pronto com as instruções

#O codigo tem que pegar instrucoes em binario e converter pra hexa e colocar num arquivo.txt para conseguir usar ele no computador de 8bits.
#Casp 1: só a instrução -> CLF
#Caso 2: A instrução e 1 registrador -> JMPR RB
#Caso 3: A instrução e 1 endereço -> JMP Addr, JMPCAEZ Addr
#Caso 4: A instrução e 2 Registradores -> ADD RA RB, SHR RA RB, SHL RA RB, NOT RA RB, AND RA RB, OR RA RB, XOR RA RB, CMP RA RB, LD RA RB, ST RA RB
#Caso 5: A instrução, 1 registrador e 1 endereço -> DATA RB, Addr

#Anotações:
#Vamos ter dois tipos de instruções aqui, um tipo de instrução vai ser gerado em um simbolo hexa unico, como todos os casos 1, 2 e 4
#o outro tipo vai gerar dois simbolos hexa, que seriam todos os casos 3 e 5.

#instrucoes em binario instrucoes = {'ADD':0b1000, 'SR':0b1001, 'SL':0b1010, 'NOT':0b1011, 'AND':0b1100, 'OR':0b1101, 'XOR':0b1110,'CMP':0b1111,'LD':0b0,
              #'ST':0b1,'DATA':0b10,'JMPR':0b11,'JMP':0b100,'JMPCAEZ':0b101,'CLF':0b110}

instrucoes = {
    'ADD': 0x08,
    'SR': 0x09,
    'SL': 0x0A,
    'NOT': 0x0B,
    'AND': 0x0C,
    'OR': 0x0D,
    'XOR': 0x0E,
    'CMP': 0x0F,
    'LD': 0x00,
    'ST': 0x01,
    'DATA': 0x02,
    'JMPR': 0x03,
    'JMP': 0x04,
    'JCAEZ': 0x05,
    'CLF': 0x06
}

registradores = {
    'R0': 0x00,
    'R1': 0x01,
    'R2': 0x02,
    'R3': 0x03
}

# Lista onde os códigos hexadecimais serão armazenados
hex_program = []

# Lê o arquivo de entrada
with open('program.asm', 'r') as f:
    linhas = f.read().upper().splitlines()

for linha in linhas:
    if not linha.strip():
        continue  # Ignora linhas em branco

    partes = linha.strip().split()
    instrucao = partes[0]

    if instrucao not in instrucoes:
        print(f"Instrução inválida: {instrucao}")
        continue

    opcode = instrucoes[instrucao]
    operandos = partes[1:]

    # Caso 1: Apenas a instrução (ex: CLF)
    if len(operandos) == 0:
        hex_program.append(f"{opcode:02X}")

    # Caso 2: Instrução + 1 registrador (ex: JMPR RB)
    elif len(operandos) == 1 and operandos[0] in registradores:
        reg = registradores[operandos[0]]
        byte = (opcode << 4) | reg
        hex_program.append(f"{byte:02X}")

    # Caso 3: Instrução + endereço (ex: JMP 0x20)
    elif len(operandos) == 1 and operandos[0].lower().startswith('0x'):
        endereco = int(operandos[0], 16)  # Espera endereço como hexa (ex: '0x20')
        hex_program.append(f"{opcode:02X}")
        hex_program.append(f"{endereco:02X}")

    # Caso 4: Instrução + 2 registradores (ex: ADD R0 R2)
    elif len(operandos) == 2 and operandos[0] in registradores and operandos[1] in registradores:
        r1 = registradores[operandos[0]]
        r2 = registradores[operandos[1]]
        byte = (opcode << 4) | (r1 << 2) | r2
        hex_program.append(f"{byte:02X}")

    # Caso 5: Instrução + registrador + endereço (ex: DATA R2, 0x20)
    elif instrucao == 'DATA' and len(operandos) == 2 and operandos[0] in registradores and operandos[1].lower().startswith('0x'):
        reg = registradores[operandos[0]]
        endereco = int(operandos[1], 16)
        byte = (opcode << 4) | reg
        hex_program.append(f"{byte:02X}")
        hex_program.append(f"{endereco:02X}")

    else:
        print(f"Formato de instrução inválido: {linha}")
        continue

# Geração do arquivo9
with open('program.txt', 'w') as f:
    f.write('v3.0 hex words plain\n')  # Cabeçalho
    for hex_code in hex_program:
        f.write(f"{hex_code}\n")
