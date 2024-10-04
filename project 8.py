import os
from numpy import char

# 获取用户输入的 a 文件目录和文件名
a_dir = input("请输入 a 文件的目录: ")
a_dir_parts = a_dir.split("\\")
temp_file_name = a_dir_parts[-1]
a_file_name =temp_file_name+".vm"
b_file_name = temp_file_name+".asm"

def commandtype(command):
    if(command[0]=='pop'):
        return 'c_pop'
    if(command[0]=='push'):
        return 'c_push'
    if(command[0]=='add' or command[0]=='sub' or command[0]=='neg' or command[0]=='eq' or command[0]=='lt' or command[0]=='gt'
    or command[0]=='and' or command[0]=='or' or command[0]=='not'):
        return 'c_ari'
    if(command[0]=='label'):
        return 'c_label'
    if(command[0]=='if-goto'):
        return 'c_ifgoto'
    if(command[0]=='goto'):
        return 'c_goto'
    if(command[0]=='function'):
        return 'c_function'
    if(command[0]=='return'):
        return 'c_return'
    if(command[0]=='call'):
        return 'c_call'
def arg1(command):
    if(command[0]=="sub" or command[0]=="add"):
        return 'c_ari'
    if(command[0]=='pop' or command[0]=="push"):
        return command[1]
    if(command[0]=="label"):
        return command[1]
    if(command[0]=="if-goto"):
        return command[1]
    if(command[0]=="goto"):
        return command[1]
    if(command[0]=="function"):
        return command[1]
    if(command[0]=="call"):
        return command[1]
def arg2(command):
    return command[2]

def writeArithmetic(command,n):
    c = []
    if(command=='sub'):
        c.append('@SP')
        c.append('A=M-1')
        c.append('D=M')
        c.append('A=A-1')
        c.append('M=M-D')
        c.append('@SP')
        c.append('M=M-1')
    if(command=='add'):
        c.append('@SP')
        c.append('A=M-1')
        c.append('D=M')
        c.append('A=A-1')
        c.append('M=D+M')
        c.append('@SP')
        c.append('M=M-1')
    if(command=='neg'):
        c.append('@SP')
        c.append('A=M-1')
        c.append('M=-M')
    if(command=='lt'or command=='gt'or command=='eq'):
        y=str(n)
        c.append('@SP')
        c.append('A=M-1')
        c.append('D=M')
        c.append('A=A-1')
        c.append('M=M-D')
        c.append('D=M')
        if(command=='lt'):
            c.append('@loop'+y+'1')
            c.append('D;JLT')
            c.append('@loop'+y+'2')
            c.append('D;JGE')
            c.append('(loop'+y+'1)')
            c.append('D=-1')
            c.append('@loop'+y+'3')
            c.append('0;JMP')
            c.append('(loop' + y + '2)')
            c.append('D=0')
        if(command=='gt'):
            c.append('@loop' + y + '1')
            c.append('D;JGT')
            c.append('@loop' + y + '2')
            c.append('D;JLE')
            c.append('(loop' + y + '1)')
            c.append('D=-1')
            c.append('@loop' + y + '3')
            c.append('0;JMP')
            c.append('(loop' + y + '2)')
            c.append('D=0')
        if(command=='eq'):
            c.append('@loop' + y + '1')
            c.append('D;JEQ')
            c.append('@loop' + y + '2')
            c.append('D;JNE')
            c.append('(loop' + y + '1)')
            c.append('D=-1')
            c.append('@loop' + y + '3')
            c.append('0;JMP')
            c.append('(loop' + y + '2)')
            c.append('D=0')
        c.append('(loop' + y + '3)')
        c.append('@SP')
        c.append('A=M-1')
        c.append('A=A-1')
        c.append('M=D')
        c.append('@SP')
        c.append('M=M-1')
    if(command=='and'or command=='or'):
        c.append('@SP')
        c.append('A=M-1')
        c.append('D=M')
        c.append('A=A-1')
        if(command=='and'):
            c.append('M=D&M')
        if(command=='or'):
            c.append('M=D|M')
        c.append('@SP')
        c.append('M=M-1')
    if(command=='not'):
        c.append('@SP')
        c.append('A=M-1')
        c.append('M=!M')

    return c
def writePushPOP(command,x,y):
    if(x=='pointer'): x='3'
    c=[]
    if(command!='c_cir'):
        if(command=='pop'):
            if (x == 'temp'):
                c.append('@5')
                c.append('D=A')
            if (x == 'this'):
                c.append('@3')
                c.append('D=M')
            if (x == 'that'):
                c.append('@4')
                c.append('D=M')
            if (x == 'local'):
                c.append('@1')
                c.append('D=M')
            if (x == 'argument'):
                c.append('@2')
                c.append('D=M')
            if (x != 'this' and x != 'that' and x != 'local' and x != 'argument' and x != 'temp'):
                c.append('@' + x)
                c.append('D=A')
            c.append('@'+y)
            c.append('D=D+A')
            c.append('@v')
            c.append('M=D')
            c.append('@SP')
            c.append('A=M-1')
            c.append('D=M')
            c.append('@v')
            c.append('A=M')
            c.append('M=D')
            c.append('@SP')
            c.append('M=M-1')
        if(command=='push'):
            if(x!='constant'):
                if (x == 'temp'):
                    c.append('@5')
                    c.append('D=A')
                if (x == 'this'):
                    c.append('@3')
                    c.append('D=M')
                if (x == 'that'):
                    c.append('@4')
                    c.append('D=M')
                if (x == 'local'):
                    c.append('@1')
                    c.append('D=M')
                if (x == 'argument'):
                    c.append('@2')
                    c.append('D=M')
                if (x != 'this' and x != 'that' and x != 'local' and x != 'argument' and x!='temp'):
                    c.append('@' + x)
                    c.append('D=A')
                c.append('@'+y)
                c.append('D=D+A')
                c.append('A=D')
                c.append('D=M')
                c.append('@SP')
                c.append('A=M')
                c.append('M=D')
            if(x=='constant'):
                c.append('@' + y)
                c.append('D=A')
                c.append('@SP')
                c.append('A=M')
                c.append('M=D')
            c.append('@SP')
            c.append('M=M+1')
    return c

def writeLabel(x,label):
    c = []
    if x not in label:
        c.append('('+x+')')
        label.append(x)
    return c

def writeIf(x):
    c=[]
    c.append("@SP")
    c.append('A=M-1')
    c.append('D=M')
    c.append('@SP')
    c.append('M=M-1')   #删除用于判断的变量
    c.append('@'+x)
    c.append('D;JNE')
    return c

def writeGoto(x):
    c=[]
    c.append("@"+x)
    c.append('0;JMP')
    return c

def writeFunction(x,y):
    c=[]
    c.append('('+x+')')
    n=int(y)
    for i in range(0,n):
        c.append('@SP')
        c.append('A=M')
        c.append('M=0')
        c.append('@SP')
        c.append('M=M+1')
    return c

def writeReturn():
    c=[]
    # FRAME=LCL
    c.append('@LCL')
    c.append('D=M')
    c.append('@FRAME')
    c.append('M=D')
    # RET=*(FRAME-5)
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('A=D')
    c.append('D=M')
    c.append('@RET')
    c.append('M=D')
    # *ARG=pop()
    c.append('@SP')
    c.append('A=M-1')
    c.append('D=M')
    c.append('@ARG')
    c.append('A=M')
    c.append('M=D')
    # SP=ARG+1
    c.append('@ARG')
    c.append('D=M')
    c.append('@SP')
    c.append('M=D+1')
    # THAT=*(FRAME-1)
    c.append('@FRAME')
    c.append('D=M-1')
    c.append('A=D')
    c.append('D=M')
    c.append('@THAT')
    c.append('M=D')
    # THIS=*(FRAME-2)
    c.append('@FRAME')
    c.append('D=M-1')
    c.append('D=D-1')
    c.append('A=D')
    c.append('D=M')
    c.append('@THIS')
    c.append('M=D')
    # ARG=*(FRAME-3)
    c.append('@FRAME')
    c.append('D=M-1')
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('A=D')
    c.append('D=M')
    c.append('@ARG')
    c.append('M=D')
    # LCL=*(FRAME-4)
    c.append('@FRAME')
    c.append('D=M-1')
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('D=D-1')
    c.append('A=D')
    c.append('D=M')
    c.append('@LCL')
    c.append('M=D')
    # GOTO RET
    c.append('@RET')
    c.append('A=M')
    c.append('0;JMP')
    return c

def writeCall(f,n,n1):   # return f_n  n1是ARG个数
    c=[]
    #push return-address
    c.append('@return_'+f+'_'+str(n))
    c.append('D=A')
    c.append('@SP')
    c.append('A=M')
    c.append('M=D')
    c.append('@SP')
    c.append('M=M+1')
    #push LCL
    c.append('@LCL')
    c.append('D=M')
    c.append('@SP')
    c.append('A=M')
    c.append('M=D')
    c.append('@SP')
    c.append('M=M+1')
    #push ARG
    c.append('@ARG')
    c.append('D=M')
    c.append('@SP')
    c.append('A=M')
    c.append('M=D')
    c.append('@SP')
    c.append('M=M+1')
    #push THIS
    c.append('@THIS')
    c.append('D=M')
    c.append('@SP')
    c.append('A=M')
    c.append('M=D')
    c.append('@SP')
    c.append('M=M+1')
    #push THAT
    c.append('@THAT')
    c.append('D=M')
    c.append('@SP')
    c.append('A=M')
    c.append('M=D')
    c.append('@SP')
    c.append('M=M+1')
    #arg=sp-n-5
    c.append('@SP')
    c.append('D=M')
    for i in range(0,int(n1)+5):
        c.append('D=D-1')
    c.append('@ARG')
    c.append('M=D')
    c.append('@SP')
    c.append('D=M')
    c.append('@LCL')
    c.append('M=D')
    c.append('@'+f)
    c.append('0;JMP')
    c.append('(return_'+f+'_'+str(n)+")")
    return c





# 拼接完整的文件路径
a_file_path = os.path.join(a_dir, a_file_name)
b_file_path = os.path.join(a_dir, b_file_name)
n=0
label = []
r_n={}
# 检查文件是否存在
if os.path.isfile(a_file_path):
    print(f"a 文件的绝对路径是: {os.path.abspath(a_file_path)}")
    # 打开 a 文件并读取其内容
    with open(a_file_path, 'r', encoding='utf-8') as file_a, open(b_file_path, 'a', encoding='utf-8') as file_b:
        c=[]
        c.append('@SP')
        c.append('M=0')
        for i in range(0,256):
            c.append('M=M+1')
        for item in c:
            file_b.write(f"{item}\n")
        c=writeCall('Sys.init',0,'0')
        for item in c:
            file_b.write(f"{item}\n")

        for line in file_a:
            processed_line = line.strip().split()

            if processed_line:
                if processed_line[0]!='//':
                    type=commandtype(processed_line)
                    if type=='c_ari':
                        c=writeArithmetic(processed_line[0],n)
                        if processed_line[0]=='eq' or processed_line[0]=='lt' or processed_line[0]=='gt':
                            n=n+1
                        for item in c:
                            file_b.write(f"{item}\n") # 将每个元素写入文件并加上换行符
                    if type=="c_pop" or type=="c_push":
                        c=writePushPOP(processed_line[0],arg1(processed_line),arg2(processed_line))
                        for item in c:
                            file_b.write(f"{item}\n")
                    if type=='c_label':
                        c=writeLabel(arg1(processed_line),label)
                        for item in c:
                            file_b.write(f"{item}\n")
                    if type=="c_ifgoto":
                        c = writeIf(arg1(processed_line))
                        for item in c:
                            file_b.write(f"{item}\n")
                    if type=="c_goto":
                        c=writeGoto(arg1(processed_line))
                        for item in c:
                            file_b.write(f"{item}\n")
                    if type=="c_function":
                        c=writeFunction(arg1(processed_line),arg2(processed_line))
                        for item in c:
                            file_b.write(f"{item}\n")
                    if type=="c_return":
                        c=writeReturn()
                        for item in c:
                            file_b.write(f"{item}\n")
                    if type=="c_call":
                        if arg1(processed_line) not in r_n:
                            r_n[arg1(processed_line)]=1
                        else:
                            r_n[arg1(processed_line)]+=1
                        c=writeCall(arg1(processed_line),r_n[arg1(processed_line)],arg2(processed_line))
                        for item in c:
                            file_b.write(f"{item}\n")






    file_a.close()
    file_b.close()





else:
    print("文件不存在或不是有效的文件，请检查路径。")