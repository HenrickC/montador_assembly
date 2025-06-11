
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

#Estudo de Caso:
#O codigo tem que ler as instrucoes do arquivo .asm, converter pra hexa e colocar num arquivo.txt.
#Caso 1: só a instrução -> CLF
#Caso 2: A instrução e 1 registrador -> JMPR RB
#Caso 3: A instrução e 1 endereço -> JMP Addr, JMPCAEZ Addr
#Caso 4: A instrução e 2 Registradores -> ADD RA RB, SHR RA RB, SHL RA RB, NOT RA RB, AND RA RB, OR RA RB, XOR RA RB, CMP RA RB, LD RA RB, ST RA RB
#Caso 5: A instrução, 1 registrador e 1 endereço -> DATA RB, Addr

#Vamos ter dois tipos de instruções aqui, um tipo de instrução vai ser gerado em um simbolo hexa unico, como todos os casos 1, 2 e 4
#o outro tipo vai gerar dois simbolos hexa, que seriam todos os casos 3 e 5.


#instrucoes em binario instrucoes = {'ADD':0b1000, 'SR':0b1001, 'SL':0b1010, 'NOT':0b1011, 'AND':0b1100, 'OR':0b1101, 'XOR':0b1110,'CMP':0b1111,'LD':0b0,
              #'ST':0b1,'DATA':0b10,'JMPR':0b11,'JMP':0b100,'JMPCAEZ':0b101,'CLF':0b110}
#funcoes

"""Para que possamos distinguir a forma em que um endereço pode ser representado no arquivo .asm, é necessária uma função para conver
tê-lo em valor inteiro, e é exatamente isto que parse_endereco faz. As condicionais verificam como o endereço foi posto no arquivo
e o convertem."""
def parse_endereco(valor):
    valor = valor.lower()
    if valor.startswith('0x'):
        return int(valor, 16) #16 pois 0x significa que estamos convertendo um valor que está em hexadecimal para inteiro.
    elif valor.startswith('0b'):
        return int(valor, 2) #2 pois 0b significa um número em binário, e esta é a sintaxe necessária para que convertê-lo para
                            #inteiro.
    else:
        return int(valor)  # Se ele não entrou em nenhum dos casos, significa que ele já está em decimal, o que torna
                            #a conversão pra inteiro desnecessária.

            
"""Depois de conseguirmos o valor inteiro, é necessário saber qual seria seu valor em binário, para isso, temos a função to_byte
que converte este valor para binário, e, até mesmo se este for negativo."""
def to_byte(valor):
    #Converte para byte de 8 bits com sinal (dois complementos).
    if not -128 <= valor <= 255:#Confere se o número é inteiro
        raise ValueError(f"Valor fora do intervalo permitido: {valor}")#Se não for, ocorre um erro
    return valor & 0xFF # o valor em binário é retornado.


# Dicionário de instruções, guardadas em hexadecimal
instrucoes = {
    'ADD': 0x08,
    'SHR': 0x09,
    'SHL': 0x0A,
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
    'CLF': 0x06,
    'IN': 0x07,
    'OUT': 0x07
}


# Instruções especiais, o JCAEZ, por ter uma variedade de possibilidades de JC até JCAEZ, acredito que colocar todas estas
#condições em um único dicionário tornaria o código mais legível.
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
#O uso de | faz uma especie de intersecção entre os valores no formato binário, e assim, todos estes se encaixam formando um 
#unico valor.
"""exemplo:
"""


#Dicionário contendo o valor dos registradores em hexadecimal.
registradores = {
    'R0': 0x00,
    'R1': 0x01,
    'R2': 0x02,
    'R3': 0x03
}

#Vetor que guardará as instruções em hexadecimal e será responsavel por imprimí-las no arquivo .txt
hex_program = []

# Leitura do programa
with open('teste.asm', 'r') as f: ##Abre o programa, no modo read(ler).
    linhas = f.read().splitlines() #Lê o arquivo como uma string única, e depois, a partir da leitura dos \n, quebra ele em linhas.

for linha in linhas: # percorre linha por linha em linhas
    if not linha.strip(): # Se a linha não estiver vazia depois de excluir os espaços com strip, continue
        continue  

    # Remove vírgulas e divide corretamente
    linha = linha.split(';')[0].strip()  # Remove comentários marcados por ; e espaços
    linha = linha.strip().replace(',', ' ')  #as virgulas encontradas serão substituidas por espaço.
    linha = ' '.join(linha.strip().split())  # remove espaços duplicados
    linha = linha.upper() # transforma tudo em maíusculas
    partes = linha.split()"""Divide a linha em um vetor,
    sendo partes[0] e os seguintes sendo seus argumentos"""
    if not partes:
        continue  # ignora linha vazia após remoção de comentários, etc.
    instrucao = partes[0].upper() #atribui a instrução para uma variavel
    operandos = [op.upper() for op in partes[1:]]"""Operandos são guardados em um vetor em específico,
    já que, de partes[1] até o ultimo elemento do vetor partes seriam os argumentos."""

    # Instruções de salto condicional personalizadas (2 bytes: opcode + endereço)
    if instrucao in condicoes and len(operandos) == 1:
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
        hex_program.append(f"{to_byte(endereco):02X}")


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
        hex_program.append(f"{to_byte(endereco):02X}")
    #Caso 6: I/O
    elif instrucao in ['IN', 'OUT'] and len(operandos) == 2:
        tipo_dado = operandos[0]
        registrador = operandos[1]

        if tipo_dado not in ['DATA', 'ADDR'] or registrador not in registradores:
            print(f"Instrução I/O mal formatada: {linha}")
            continue

        bit_io   = 0 if instrucao == 'IN' else 1       # Bit 3
        bit_tipo = 0 if tipo_dado == 'DATA' else 1     # Bit 2
        reg_bits = registradores[registrador]          # Bits 1-0

        byte = (0b0111 << 4) | (bit_io << 3) | (bit_tipo << 2) | reg_bits
        hex_program.append(f"{byte:02X}")

    else:
        print(f"Instrução inválida ou mal formatada: {linha}")

# Escreve a saída
with open('teste.txt', 'w') as f:
    f.write('v3.0 hex words plain\n')
    for hex_code in hex_program:
        f.write(f"{hex_code}\n")
