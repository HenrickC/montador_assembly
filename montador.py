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

hexadecimal = hex(int(binario, 2))






with open('program.txt', 'w') as f:
  f.write('v3.0 hex words plain')
  f.write(memory[0])
  f.write('\n')
  f.write(memory[1])
