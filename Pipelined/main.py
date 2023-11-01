import decodings



instruction_memory = []
data_memory        = [0]*100


register_file = {
    '$0': 0,

    '$t0': 10,
    '$t1': '01001',
    '$t2': 43123,
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$t8': '11000',
    '$t9': '11001',

    '$s0': 12,
    '$s1': '10001',
    '$s2': '10010',
    '$s3': '10011',
    '$s4': '10100',
    '$s5': '10101',
    '$s6': '10110',
    '$s7': '10111',
}



file_path = "test_bin_dump.txt" 
with open(file_path, "r") as file:
    instruction_memory = file.readlines()

'''
clock cycle 1    : Instruction No 1 :-  (IF)   PC -> 101010101101010101101010101101010101
clock cycle 2    : Instruction No 1 :-  (ID)   instruction decoded as :-

                        Instruction[31:26] --- 10010 --- addi
                        Instruction[25:21] --- 10010 --- $s0 
                        Instruction[20:16] --- 10010 --- $s0
                        Instruction[15:0 ] --- 10010000000000000 --- 0

                        addi    $s0, $t0 , 0

clock cycle 1    : Instruction No 2 :-  (IF)   PC -> 101010101101010101101010101101010101

clock cycle 3    : Instruction No 1 :-  (Ex)  ALU performing addition 

                         Instruction No 2 :-  (ID)   instruction decoded as :-

                        Instruction[31:26] --- 10010 --- addi
                        Instruction[25:21] --- 10010 --- $s0 
                        Instruction[20:16] --- 10010 --- $s0
                        Instruction[15:0 ] --- 10010000000000000 --- 0

                        addi    $s0, $t0 , 0

                         Instruction No 3 :-  (IF)   PC -> 101010101101010101101010101101010101




clock cycle 4    : Instruction No 1 :-  (Mem) No memory access required  
clock cycle 5    : Instruction No 1 :-  (RegWrite)   

                        registers $s0 contains :-  123



'''


def IF(line):
    pass


def ID(line):
    pass


def Exe(line):
    pass


def Mem(line):
    pass


def WB(line):
    pass



clk = 1; instruction_number = 1
eof = len(instruction_memory)
branch_jump_flag = 0


line = instruction_memory[instruction_number - 1] 


IF(line)

ID(line)
IF(line)

Exe(line)


while instruction_number - 1 != eof :

    output = 0











