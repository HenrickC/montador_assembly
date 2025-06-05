

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

import os

# Nome: Carlos Henrick Cavalcante Gomes
# Matricula: 22400691


#Ainda falta os casos de IO OUT ADRR, ETC.

#funcoes
def parse_endereco(valor):
    valor = valor.lower()
    if valor.startswith('0x'):
        return int(valor, 16)
    elif valor.startswith('0b'):
        return int(valor, 2)
    else:
        return int(valor)  # Decimal puro

# Dicionário de instruções
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
    'CLF': 0x06
}

# Condições de salto (usadas com opcode base 0x5)
condicoes = {
    'JZ':  0x1,
    'JC':  0x2,
    'JA':  0x4,
    'JE':  0x8,
    'JCA':  0x2 | 0x4,
    'JCE':  0x2 | 0x8,
    'JCZ':  0x2 | 0x1,
    'JAE':  0x4 | 0x8,
    'JAZ':  0x4 | 0x1,
    'JEZ':  0x8 | 0x1,
    'JCAE': 0x2 | 0x4 | 0x8,
    'JCAZ': 0x2 | 0x4 | 0x1,
    'JCEZ': 0x2 | 0x8 | 0x1,
    'JAEZ': 0x4 | 0x8 | 0x1,
    'JCAEZ': 0x2 | 0x4 | 0x8 | 0x1
}

registradores = {
    'R0': 0x00,
    'R1': 0x01,
    'R2': 0x02,
    'R3': 0x03
}

hex_program = []

# Leitura do programa
with open('program.asm', 'r') as f:
    linhas = f.read().splitlines()

for linha in linhas:
    if not linha.strip():
        continue  # ignora linhas em branco

    # Remove vírgulas e divide corretamente
    linha = linha.split(';')[0].strip()  # Remove comentários e espaços
    linha = linha.strip().replace(',', ' ')
    linha = ' '.join(linha.strip().split())  # remove espaços duplicados
    linha = linha.upper()                  # força maiúsculas
    partes = linha.split()
    if not partes:
        continue  # ignora linha vazia após remoção de comentários, etc.
    instrucao = partes[0].upper()
    operandos = [op.upper() for op in partes[1:]]

    # Instruções de salto condicional personalizadas (2 bytes: opcode + endereço)
    if instrucao in condicoes and len(operandos) == 1 and operandos[0].startswith('0X'):
        endereco = parse_endereco(operandos[0])
        cond_byte = (0x05 << 4) | condicoes[instrucao]
        hex_program.append(f"{cond_byte:02X}")
        hex_program.append(f"{endereco:02X}")

    # Caso 1: Instrução sem operando (ex: CLF)
    elif instrucao in instrucoes and len(operandos) == 0:
        hex_program.append(f"{instrucoes[instrucao]:02X}")

    # Caso 2: Instrução + 1 registrador (ex: JMPR R1)
    elif instrucao in instrucoes and len(operandos) == 1 and operandos[0] in registradores:
        reg = registradores[operandos[0]]
        byte = (instrucoes[instrucao] << 4) | reg
        hex_program.append(f"{byte:02X}")

    # Caso 3: Instrução + 1 endereço (ex: JMP 0x20)
    elif instrucao in instrucoes and len(operandos) == 1 and operandos[0].startswith('0X'):
        endereco = parse_endereco(operandos[0])
        hex_program.append(f"{instrucoes[instrucao]:02X}")
        hex_program.append(f"{endereco:02X}")

    # Caso 4: Instrução + 2 registradores (ex: ADD R0 R2)
    elif instrucao in instrucoes and len(operandos) == 2 and operandos[0] in registradores and operandos[1] in registradores:
        r1 = registradores[operandos[0]]
        r2 = registradores[operandos[1]]
        byte = (instrucoes[instrucao] << 4) | (r1 << 2) | r2
        hex_program.append(f"{byte:02X}")

    # Caso 5: DATA + registrador + endereço (ex: DATA R2, 0x20)
    elif instrucao == 'DATA' and len(operandos) == 2 and operandos[0] in registradores:
        reg = registradores[operandos[0].upper()]
        try:
            endereco = parse_endereco(operandos[1])
        except ValueError:
            print(f"Endereço inválido: {operandos[1]}")
            continue
        byte = (instrucoes[instrucao] << 4) | reg
        hex_program.append(f"{byte:02X}")
        hex_program.append(f"{endereco:02X}")

    else:
        print(f"Instrução inválida ou mal formatada: {linha}")

# Escreve a saída
with open('program.txt', 'w') as f:
    f.write('v3.0 hex words plain\n')
    for hex_code in hex_program:
        f.write(f"{hex_code}\n")
