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



instrucoes = {
    "CLF": 0x00,
    "JMPR": 0x10,
    "JMP": 0x20,
    "JMPCAEZ": 0x21,
    "ADD": 0x30,
    "SHR": 0x31,
    "SHL": 0x32,
    "NOT": 0x33,
    "AND": 0x34,
    "OR": 0x35,
    "XOR": 0x36,
    "CMP": 0x37,
    "LD": 0x38,
    "ST": 0x39,
    "DATA": 0x40
}

registradores = {
    "RA": 0x0,
    "RB": 0x1,
    "RC": 0x2,
    "RD": 0x3
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
        byte = opcode | reg  # Combina opcode com registrador (últimos bits)
        hex_program.append(f"{byte:02X}")

    # Caso 3: Instrução + endereço (ex: JMP 05)
    elif len(operandos) == 1:
        endereco = int(operandos[0], 16)  # espera endereço como hexa (ex: '0A')
        hex_program.append(f"{opcode:02X}")
        hex_program.append(f"{endereco:02X}")

    # Caso 4: Instrução + 2 registradores (ex: ADD RA RB)
    elif len(operandos) == 2 and operandos[0] in registradores and operandos[1] in registradores:
        r1 = registradores[operandos[0]]
        r2 = registradores[operandos[1]]
        byte = opcode | (r1 << 2) | r2
        hex_program.append(f"{byte:02X}")

    # Caso 5: Instrução + registrador + endereço (ex: DATA RB, 0F)
    elif len(operandos) == 2 and operandos[0] in registradores:
        reg = registradores[operandos[0]]
        endereco = int(operandos[1], 16)
        byte = opcode | reg
        hex_program.append(f"{byte:02X}")
        hex_program.append(f"{endereco:02X}")

    else:
        print(f"Formato de instrução inválido: {linha}")
        continue



#Geração do arquivo 
with open('program.txt', 'w') as f:
    f.write('v3.0 hex words plain')
    for hex_code in hex_program:
        f.write(f"{hex_code}\n")
