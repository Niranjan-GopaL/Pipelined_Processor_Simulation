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


'''Output we trying for :-

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

''' For Branch Insteruction output we'll try to do :-



'''


  
# To do 

#  [*]-> addi instruction
#  [*]-> sub instruction
#  []-> lw  instruction
#  []-> sw  instruction
#  []-> beq  instruction ( Do later )               
#  []-> j  instruction
#  []-> sw  instruction




begining_space = "                        "
clk = 1


instruction_number = 1
eof = len(instruction_memory)

while instruction_number - 1 != eof :
    output = 0

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

    if opcode_decoded in decodings.load_store_encoding :
        rs = line[6:11]
        rt = line[11:16]
        imm = line[16:]
        rs_decoded = decodings.register_decoding[rs]        
        rt_decoded = decodings.register_decoding[rt]
        print(begining_space + f'Instruction[25:21] --- {rs} --- {rs_decoded} ')
        print(begining_space + f'Instruction[20:16] --- {rt} --- {rt_decoded} ')
        print(begining_space + f'Instruction[15:0 ] --- {imm} --- {int(imm)}\n')

        print(begining_space + f'{opcode_decoded}    {rt_decoded}, {int(imm)}({rs_decoded}), \n')


    elif opcode_decoded in decodings.r_type:
        rs = line[6:11]
        rt = line[11:16]
        rd = line[16:21]
        shamt = line[21:26]
        func = line[26:]

        rs_decoded    = decodings.register_decoding[rs]        
        rt_decoded    = decodings.register_decoding[rt]
        rd_decoded    = decodings.register_decoding[rd]
        func_decoded  = decodings.func_encoding[func]

        print(begining_space + f'Instruction[25:21] --- {rs} --- {rs_decoded} ')
        print(begining_space + f'Instruction[20:16] --- {rt} --- {rt_decoded} ')
        print(begining_space + f'Instruction[15:11] --- {rd} --- {rd_decoded} ')

        print(begining_space + f'Instruction[10:6 ] --- {shamt} --- 0 ')
        print(begining_space + f'Instruction[5 :0  ] --- {func} --- {func_decoded} ')

        print(begining_space + f'{func_decoded}    {rd_decoded}, {rs_decoded}, {rt_decoded}\n')


    clk+=1


    # ALU phase
    if opcode_decoded in decodings.i_type or opcode_decoded in decodings.load_store_encoding :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing addition\n')

        print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
        print(begining_space + f'immediate value        :- {int(imm)}')
        print(begining_space + 'ALU executing...')

        # ALU addition
        output = int(imm) + register_file[rs_decoded]

        print(begining_space + f'Output computed as     :-  + {register_file[rs_decoded]} + {int(imm)} = {output}\n\n')

    if opcode_decoded in decodings.r_type :
        opertaion = { 'sub': "subrtation", 'add': "addition", 'mul': "multiplication"}

        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing {opertaion[func_decoded]}\n')
        print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
        print(begining_space + f'register {rt_decoded} contains  :- {register_file[rt_decoded]}')

        print(begining_space + 'ALU executing...')


        rs_value = register_file[rs_decoded]
        rt_value = register_file[rt_decoded]

        # ALU operation
        if func_decoded == 'sub':
            output = rs_value - rt_value
            operation_character = '-'

        elif func_decoded == 'add':
            output = rs_value + rt_value
            operation_character = '+'

        elif func_decoded == 'mul':
            output = rs_value * rt_value
            operation_character = '*'

        print(begining_space + f'Output computed as     :-  + {register_file[rs_decoded]} {operation_character} {register_file[rt_decoded]} = {output}\n\n')


    clk+=1






    # Mem Access phase
    if   opcode_decoded == 'sw' :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) Data Memory needs to written onto  ')

        # Do data memory stuff ...

    elif opcode_decoded == 'lw' :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No memory access required ')

        # Do data memory stuff ...
        
    else:
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No memory access required ')

    clk+=1



    # MemWriteBack phase
    if opcode_decoded != 'lw' :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (WriteBack) Writing ALU output back to RegFile  \n')
        if opcode_decoded in decodings.i_type :
            register_file[rt_decoded] = output
            print(begining_space + f'registers {rt_decoded} contains :-  {output}\n')
        else:
            register_file[rd_decoded] = output
            print(begining_space + f'registers {rd_decoded} contains :-  {output}\n')
    else:
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No Writing back to register file required ')




    clk+=1
    instruction_number += 1
