import os
a,b,c=(i for i in input().split())
os.chdir('C:/Users/lll13/Downloads/nand2tetris/nand2tetris/projects/{}/{}'.format(a,b))
file=open("{}.asm".format(c),'r')
r=file.readlines()
file.close()
asm1=[]
asm=[]
for i in range(0,len(r)):
    print(r[i])
    if (r[i][0]=="/" or r[i][0]=="\n"):
        continue
    else:
        asm1.append(r[i])
for i in range(0,len(asm1)):
    asm.append(asm1[i][0:len(asm1[i])-1])
print(asm)
instr=[]

def A(x):
    a=int(x[1:])
    t=bin(a)[2:]
    c='0'*(16-len(t))+t
    return c


def C(x):
    if '=' not in x:
        x = '=' + x
    if ';' not in x:
        x = x + ';'
    a, c = x.split('=')
    b, jump = c.split(';')
    instra = ''
    instrjump = ''
    if 'A' in a:
        instra = "1" + instra
    else:
        instra = '0' + instra
    if 'D' in a:
        instra = instra + '1'
    else:
        instra = instra + '0'
    if 'M' in a:
        instra = instra + '1'
    else:
        instra = instra + '0'
    if jump == 'JGT':
        instrjump = '001'
    if jump == 'JEQ':
        instrjump = '010'
    if jump == 'JGE':
        instrjump = '011'
    if jump == 'JLT':
        instrjump ='100'
    if jump == 'JNE':
        instrjump ='101'
    if jump == 'JLE':
        instrjump ='110'
    if jump == 'JMP':
        instrjump ='111'
    if jump=='':
        instrjump='000'
    comp = ''
    if b == "0":
        comp = comp + "0101010"
    elif b == '1':
        comp = comp + "0111111"
    elif b == '-1':
        comp = comp + '0111010'
    elif b == 'D':
        comp = comp + '0001100'
    elif b == 'A':
        comp = comp + '0110000'
    elif b == 'M':
        comp = comp + '1110000'
    elif b == '!D':
        comp = comp + '0001101'
    elif b == '!A':
        comp = comp + '0110001'
    elif b == '!M':
        comp = comp + '1110001'
    elif b == '-D':
        comp = comp + '0001111'
    elif b == '-A':
        comp = comp + '0110011'
    elif b == '-M':
        comp = comp + '1110011'
    elif b == "D+1":
        comp = comp + '0011111'
    elif b == 'A+1':
        comp = comp + '0110111'
    elif b == 'M+1':
        comp = comp + '1110111'
    elif b == 'D-1':
        comp = comp + '0001110'
    elif b == 'A-1':
        comp = comp + '0110010'
    elif b == 'M-1':
        comp = comp + '1110010'
    elif b == 'D+A':
        comp = comp + '0000010'
    elif b == 'D+M':
        comp = comp + '1000010'
    elif b == 'D-A':
        comp = comp + '0010011'
    elif b == 'D-M':
        comp = comp + '1010011'
    elif b == 'A-D':
        comp = comp + '0000111'
    elif b == 'M-D':
        comp = comp + '1000111'
    elif b == 'D&A':
        comp = comp + '0000000'
    elif b == 'D&M':
        comp = comp + '1000000'
    elif b == 'D|A':
        comp = comp + '0010101'
    else:
        comp = comp + '1010101'
    print(instrjump)
    return '111' + comp + instra + instrjump






for i in range(0,len(asm)):
    if asm[i][0]=="@":
        instruction=A(asm[i])
    else:
        instruction=C(asm[i])
    instr.append(instruction)
file=open('{}.hark'.format(c),'w+')
for i in range(0,len(instr)):
    file.write("{}\n".format(instr[i]))






