def fetch_instruction(instruction_memory,pc):
    return instruction_memory[pc]


def binary_neg_decimal(decimal_value):
    if decimal_value & 0x8000: 
        decimal_value = -((1 << 16) - decimal_value)
    return decimal_value


def decode_instruction(instruction,reg_memory):
    op=instruction[0:6]
    opcodes = {
    "000000":"r_type" ,
    "100011":"lw" ,
    "101011":"sw",
    "001000":"addi",
    "000101":"bne",
    "000100":"beq",
    "011100":"mul",
    "001001":"li",
    "000011":"jal",
    "000010":"j"}

    reg={
        "00001":"$at", #temporary reg for pseudo code
        "00101":"$a1",
        "00000":"$0",
        "01000":"$t0" ,
        "01001":"$t1",
        "01010":"$t2",
        "01011":"$t3",
        "01100":"$t4",
        "01101": "$t5",
        "01110": "$t6",
        "01111": "$t7",
        "11000": "$t8",
        "11001": "$t9",
        "10000": "$s0",
        "10001": "$s1",
        "10010": "$s2",
        "10011": "$s3",
        "10100": "$s4",
        "10101": "$s5",
        "10110": "$s6",
        "10111": "$s7"
    }



    for e in opcodes:
        if(e==op):
            str=opcodes[op]
            if(str=="r_type"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                rd=instruction[16:21]
                shamt=instruction[21:26]
                funct=instruction[26:32]
                rs=reg[rs]
                rt=reg[rt]
                rd=reg[rd]
                shamt=int(shamt,2)
                funct=int(funct,2)
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                rd1=reg_memory[rd]
                l=[rs1,rt1,rd1,shamt,funct,rs,rt,rd]
                return l

            elif(str=="lw"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[op,rs1,rt1,imm,rs,rt]
                return l

            elif(str=="addi"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[op,rs1,rt1,imm,rs,rt]
                return l

            elif(str=="beq"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[op,rs1,rt1,imm,rs,rt]
                return l

            elif(str=="bne"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[op,rs1,rt1,imm,rs,rt]
                return l

            elif(str=="sw"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[op,rs1,rt1,imm,rs,rt]
                return l

            elif(str=="li"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                imm=instruction[16:32]
                rs=reg[rs]
                rt=reg[rt]
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                imm=int(imm,2)
                l=[op,rs1,rt1,imm,rs,rt]
                return l

            elif(str=="mul"):
                rs=instruction[6:11]
                rt=instruction[11:16]
                rd=instruction[16:21]
                shamt=instruction[21:26]
                funct=instruction[26:32]
                rs=reg[rs]
                rt=reg[rt]
                rd=reg[rd]
                shamt=int(shamt,2)
                funct=int(funct,2)
                rs1=reg_memory[rs]
                rt1=reg_memory[rt]
                rd1=reg_memory[rd]
                l=[rs1,rt1,rd1,shamt,funct,rs,rt,rd]
                return l

            




def execute_instruction(l,pc):
    wb=0 #Control Lines-Write back
    wm=0 #Control Lines-Write Memory
    rm=0 #Control Lines-Read Memory
    m=[]
        
    if(len(l)==8): #r_type format
        funct=l[4]
        if(funct==33): #move
            wb=1
            wm=0
            rm=0
            l[2]=l[1]
            m=[wb,wm,rm,l[2],l[7]]
            return m

        elif(funct==32): #add
            wb=1
            wm=0
            rm=0
            l[2]=l[0]+l[1]
            m=[wb,wm,rm,l[2],l[7]]
            return m

        elif(funct==0): #sll
            wb=1
            wm=0
            rm=0
            l[2]=l[1]*((2**l[3])//4)
            m=[wb,wm,rm,l[2],l[7]]
            return m

        elif(funct==34): #sub
            wb=1
            wm=0
            rm=0
            l[2]=l[1]-l[0]
            m=[wb,wm,rm,l[2],l[7]]
            return m
            
        elif(funct==42):#slt
            wb=1
            wm=0
            rm=0
            if(l[0]<l[1]):
                l[2]=1
            else:
                l[2]=0
            m=[wb,wm,rm,l[2],l[7]]
            return m
        
        elif(funct==2):#mul
            wb=1
            wm=0
            rm=0
            l[2]=l[0]*l[1]
            m=[wb,wm,rm,l[2],l[7]]
            return m


    elif(len(l)==6): #i-type format
        op=l[0]
        imm=l[3]
        if(op=='001000'):#addi
            wb=1
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
                if(imm<-3):
                    imm=imm//4 
            if(imm>3):
                imm=imm//4
            l[2]=l[1]+imm
            m=[wb,wm,rm,l[2],l[5]]
            return m

        elif(op=='100011'): #lw
            wb=1
            rm=1
            wm=0
            imm=imm//4
            x=imm+l[1]
            m=[wb,wm,rm,x,l[2],l[5]]
            return m

        elif(op=='101011'): #sw
            wm=1
            wb=0
            rm=0
            imm=imm//4
            x=l[1]+imm
            m=[wb,wm,rm,x,l[2],l[5]]
            return m

        elif(op=='001001'):#li
            wb=1
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
                if(imm<-3):
                    imm=imm//4 
            if(imm>3):
                imm=imm//4
            l[2]=l[1]+imm
            m=[wb,wm,rm,l[2],l[5]]
            return m
        
        elif(op=='000101'):#bne
            wb=0
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
            if(l[2]!=l[1]):
                pc=pc+imm
                m=[wb,wm,rm,pc]
                return m
            else:
                m=[wb,wm,rm,pc]
                return m

        elif(op=='000100'):#beq
            wb=0
            wm=0
            rm=0
            if(imm>1000):
                imm=binary_neg_decimal(imm)
            if(l[2]==l[1]):
                pc+=imm
                m=[wb,wm,rm,pc]
                return m
            else:
                m=[wb,wm,rm,pc]
                return m

        



def memory_access(wm,rm,data_memory,x,rt1):
    if(rm==1):
        return data_memory[x]

    if(wm==1):
        data_memory[x]=rt1
        return data_memory




def write_back(reg_memory,rd1,rd):
    if(rd=='$s0'):
        rd1=abs(rd1)
    reg_memory[rd]=rd1
    return reg_memory


def main():
    # binary code for sorting
    # instruction_memory=["00000000000000001011100000100000",
    # "00000001011000001010100000100000",
    # "00000001010000000111100000100000",
    # "00100001010011000000000110010000",
    # "10001101010110010000000000000000",
    # "10101101100110010000000000000000",
    # "00100001100011000000000000000100",
    # "00100001010010100000000000000100",
    # "00100010111101110000000000000001",
    # "00010110111010011111111111111010",
    # "00000000000000001011100000100000",
    # "00000000000000000110000000100000",
    # "00000001111000000101000000100000",
    # "00100001010011000000000110010000",
    # "00000000000010010010100010000000",
    # "00000000101011000010100000100000",
    # "00010010111010010000000000010100",
    # "00000000000000001011000000100000",
    # "00000000000101101000000010000000",
    # "00000001100100001000000000100000",
    # "00100010000100000000000000001000",
    # "00000000101100000000100000101010",
    # "00010100001000000000000000001011",
    # "00100000000000010000000000001000",
    # "00000010000000011000000000100010",
    # "10001110000011010000000000000000",
    # "10001110000011100000000000000100",
    # "00000001110011010000100000101010",
    # "00010000001000000000000000000010",
    # "10101110000011100000000000000000",
    # "10101110000011010000000000000100",
    # "00100010110101100000000000000001",
    # "00000010110010010000100000101010",
    # "00010100001000001111111111110000",
    # "00100010111101110000000000000001",
    # "00000010111010010000100000101010",
    # "00010100001000001111111111101011",
    # "00000000000000001010000000100000",
    # "10001101100100110000000000000000",
    # "10101110101100110000000000000000",
    # "00100001100011000000000000000100",
    # "00100010101101010000000000000100",
    # "00100010100101000000000000000001",
    # "00010110100010011111111111111010"]

    #binary code forfactorial
    instruction_memory=["00100000000011100000000000000000", 
    "00100001010011110000000000000000",
    "00100001011110000000000000000000",
    "10001101010011000000000000000000",
    "00100001110011100000000000000001",
    "00100000000011010000000000000001",
    "00010001100000000000000000000110",
    "01110001101011000110100000000010",
    "00100001100011001111111111111111",
    "00010101100000001111111111111101",
    "10101101011011010000000000000000",
    "00100001010010100000000000000100",
    "00100001011010110000000000000100",
    "00100001100011000000000000000001",
    "10101101011011000000000000000000",
    "00010101110010011111111111110011",
    "00100001111010100000000000000000",
    "00100011000010110000000000000000"]

    n=len(instruction_memory)
    a=int(input("Enter number of integers:"))
    b=int(input("Enter base address of input:"))
    c=int(input("Enter base address of output:"))
    clock=0

    reg_memory={
            "$0":0,
            "$at":0,
            "$a1":0,
            "$s0":0,
            "$s1":0,
            "$s2":0,
            "$s3":0,
            "$s4":0,
            "$s5":0,
            "$s6":0,
            "$s7":0,
            "$t0":0,
            "$t1":a,
            "$t2":b,
            "$t3":c,
            "$t4":0,
            "$t5":0,
            "$t6":0,
            "$t7":0,
            "$t8":0,
            "$t9":0}

    pc=0
    data_memory=[0]*200
    for i in range(b,b+a):
            e=int(input("Enter the number:"))
            data_memory[i]=e
    print("\n")
    while(pc<n):
        instruction=fetch_instruction(instruction_memory,pc)
        l=[]
        m=[]
        l=decode_instruction(instruction,reg_memory)
        m=execute_instruction(l,pc)
        if(m[0]==1 and m[1]==0 and m[2]==0):
            reg_memory=write_back(reg_memory,m[3],m[4])

        elif(m[0]==1 and m[2]==1 and m[1]==0):#lw
            x=memory_access(m[1],m[2],data_memory,m[3],m[4])
            reg_memory=write_back(reg_memory,x,m[5])

        elif(m[1]==1 and m[0]==0 and m[2]==0):
            data_memory=memory_access(m[1],m[2],data_memory,m[3],m[4])

        if(m[0]==0 and m[1]==0 and m[2]==0):
            pc=m[3]        
        pc+=1
        clock+=5
        
        
    x=reg_memory["$t3"]
    y=reg_memory["$t1"]
    for i in range(x,x+y):
        print(data_memory[i],end=" ")
    print("\n")
    print(f"Clock Cycles:{clock}")
   
main()