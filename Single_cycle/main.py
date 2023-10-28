import decodings


instruction_memory = []

register_file = {
    '$0': 0,

    '$t0': '01000',
    '$t1': '01001',
    '$t2': 43123,
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$t8': '11000',
    '$t9': '11001',

    '$s0': '10000',
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
Output we trying for :-

clock cycle 1    : Instruction No 1 :-  (IF)   PC -> 101010101101010101101010101101010101
clock cycle 2    : Instruction No 1 :-  (ID)   instruction decoded as :-

                        Instruction[31:26] --- 10010 --- addi
                        Instruction[25:21] --- 10010 --- $s0 
                        Instruction[20:16] --- 10010 --- $s0
                        Instruction[15:0 ] --- 10010000000000000 --- 0

                        addi    $s0, $t0 , 0

clock cycle 3    : Instruction No 1 :-  (Ex)  ALU performing addition 

                        register $t0 contains  :- 123
                        immediate value        :- 0

                        ALU executing...
                        Output computed as     :- 123 + 0 = 123


clock cycle 4    : Instruction No 1 :-  (Mem) No memory access required  
clock cycle 5    : Instruction No 1 :-  (RegWrite)   

                        registers $s0 contains :-  123
                        
'''

begining_space = "                        "
clk = 1

instruction_number = 1
eof = len(instruction_memory)

while instruction_number - 1 != eof :
    line = instruction_memory[instruction_number - 1] 
    line = line.strip()
    
    # IF Phase
    print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (IF)   PC -> {line}')
    clk += 1



    # ID Phase
    print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (ID)   instruction decoded as :-\n')

    opcode = line[:6]
    opcode_decoded = decodings.opcode_decodings[opcode]
    print(begining_space + f'Instruction[31:26] --- {opcode} --- {opcode_decoded}')


    if opcode_decoded in decodings.i_type :
        rs = line[6:11]
        rt = line[11:16]
        imm = line[16:]
        rs_decoded = decodings.register_decoding[rs]        
        rt_decoded = decodings.register_decoding[rt]
        print(begining_space + f'Instruction[25:21] --- {rs} --- {rs_decoded} ')
        print(begining_space + f'Instruction[20:16] --- {rt} --- {rt_decoded} ')
        print(begining_space + f'Instruction[15:0 ] --- {imm} --- {int(imm)}\n')

        print(begining_space + f'{opcode_decoded}    {rt_decoded}, {rs_decoded}, {int(imm)}\n')

    clk+=1


    # ALU phase
    print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing addition\n')

    print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
    print(begining_space + f'immediate value        :- {int(imm)}')
    print(begining_space + 'ALU executing...')

    # ALU addition
    output = int(imm) + register_file[rs_decoded]

    print(begining_space + f'Output computed as     :-  + {register_file[rs_decoded]} + {int(imm)} = {output}\n\n')
    clk+=1




    # Mem Access phase
    print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No memory access required ')
    clk+=1



    # MemWriteBack phase
    print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (WriteBack) Writing ALU output back to RegFile  \n')

    register_file[rt_decoded] = output

    print(begining_space + f'registers {rt_decoded} contains :-  {output}\n')
    clk+=1

    instruction_number += 1



# for instruction_number, line in enumerate(instruction_memory):
#     line = line.strip()
#     instruction_number += 1


#     # IF Phase
#     print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (IF)   PC -> {line}')
#     clk += 1



#     # ID Phase
#     print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (ID)   instruction decoded as :-\n')

#     opcode = line[:6]
#     opcode_decoded = decodings.opcode_decodings[opcode]
#     print(begining_space + f'Instruction[31:26] --- {opcode} --- {opcode_decoded}')


#     if opcode_decoded in decodings.i_type :
#         rs = line[6:11]
#         rt = line[11:16]
#         imm = line[16:]
#         rs_decoded = decodings.register_decoding[rs]        
#         rt_decoded = decodings.register_decoding[rt]
#         print(begining_space + f'Instruction[25:21] --- {rs} --- {rs_decoded} ')
#         print(begining_space + f'Instruction[20:16] --- {rt} --- {rt_decoded} ')
#         print(begining_space + f'Instruction[15:0 ] --- {imm} --- {int(imm)}\n')

#         print(begining_space + f'{opcode_decoded}    {rt_decoded}, {rs_decoded}, {int(imm)}\n')

#     clk+=1

#     # ALU phase
#     print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing addition\n')

#     print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
#     print(begining_space + f'immediate value        :- {int(imm)}')
#     print(begining_space + 'ALU executing...')
#     print(begining_space + 'Output computed and stored in register ' + str(rs_decoded))

#     # ALU addition
#     output = int(imm) + register_file[rs_decoded]


#     # Mem Access phase
#     print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No memory access required  \n')



#     # MemWriteBack phase
#     print(begining_space + f'registers {rt_decoded} contains :-  {output}\n')
