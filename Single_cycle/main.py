import decodings



# register_file = {
#     '$0': 0,

#     '$t0': 10,
#     '$t1': '01001',
#     '$t2': 43,
#     '$t3': '01011',
#     '$t4': '01100',
#     '$t5': '01101',
#     '$t6': '01110',
#     '$t7': '01111',
#     '$t8': '11000',
#     '$t9': '11001',

#     '$s0': 12,
#     '$s1': '10001',
#     '$s2': '10010',
#     '$s3': 333333,
#     '$s4': 444444,
#     '$s5': '10101',
#     '$s6': '10110',
#     '$s7': '10111',
# }




instruction_memory = []
data_memory        = [0]*100

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

''' load
clock cycle 4    : Instruction No 1 :-  (Mem) Memory access initiation ...

                        Memory[ rs + imm ]  
                        Memory[ 4324 + 12 ] =  value_in_mem

clock cycle 5    : Instruction No 1 :-  (RegWrite) Writing back to register   

                        registers $s0 =  Memory[ 4336 ] = value_in_mem 
'''

''' store
clock cycle 4    : Instruction No 1 :-  (Mem) Memory access initiation ...

                        registers $rt = ...

                        Memory[ rs + imm ]     
                        Memory[ 4324 + 12 ] =  ...

clock cycle 5    : Instruction No 1 :-  (RegWrite) No register write back
'''

''' For Branch Insteruction output we'll try to do :-

clock cycle 1    : Instruction No 1 :-  (IF)   PC -> 101010101101010101101010101101010101
clock cycle 2    : Instruction No 1 :-  (ID)   instruction decoded as :-

                        Instruction[31:26] --- 10010 --- beq
                        Instruction[25:21] --- 10010 --- $s0 
                        Instruction[20:16] --- 10010 --- $s0
                        Instruction[15:0 ] --- 10010000000000000 --- 0

                        beq    $s0, $t0 , 0

( 2 possibilies )       
----------------------------------------------------------------------------------------------                 
clock cycle 3    : Instruction No 1 :-  (Ex)  ALU performing subtraction

                        register $rs contains  :- 124
                        register $rt contains  :- 120

                        ALU executing...
                        Output computed as     :- 124 - 120 = 4

                        No branching occurs
----------------------------------------------------------------------------------------------                 



----------------------------------------------------------------------------------------------                 
clock cycle 3    : Instruction No 1 :-  (Ex)  ALU performing subtraction

                        register $rs contains  :- 124
                        register $rt contains  :- 124

                        ALU executing...
                        Output computed as     :- 124 - 124 = 0

                        imm value              :- 12
                        left shift by 2        :- 48

                        => PC = PC + 4 + 12 * 4
----------------------------------------------------------------------------------------------                 

                        


clock cycle 4    : Instruction No 1 :-  (Mem) No memory access required  
clock cycle 5    : Instruction No 1 :-  (RegWrite) No register write back

'''


  
# To do 

#  [*]-> addi instruction
#  [*]-> sub instruction
#  [*]-> lw  instruction
#  [*]-> sw  instruction
#  [*]-> beq  instruction ( Do later )               
#  [*]-> j  instruction


t0 = int(input("Enter number of integers:"))
t1 = int(input("Enter base address of input:"))
t2 = int(input("Enter base address of output:"))


register_file = {
        "$0":0,

        "$t0" : t0,
        "$t1" : t1,
        "$t2" : t2,
        "$t3" : 0,
        "$t4" : 0,
        "$t5" : 0,
        "$t6" : 0,
        "$t7" : 0,
        "$t8" : 0,
        "$t9" : 0,

        "$s0" : 0,
        "$s1" : 0,
        "$s2" : 0,
        "$s3" : 0,
        "$s4" : 0,
        "$s5" : 0,
        "$s6" : 0,
        "$s7" : 0,

}


for i in range(t1, t1 + t0 ):
        data_memory[i] = int(input("Enter the number:"))



def integer_of_16_bit_imm(binary_str):
    is_negative = binary_str[0] == '1'

    if is_negative:
        inverted_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        binary_str = bin(int(inverted_str, 2) + 1)[2:]  

    decimal_value = int(binary_str, 2)

    if is_negative:
        decimal_value = -decimal_value

    return decimal_value



begining_space = "                        "
clk = 1; instruction_number = 1; output = 0
eof = len(instruction_memory)
branch_jump_flag = 0



while instruction_number - 1 != eof :

    # resetting if triggered  
    if branch_jump_flag == 1: 
        branch_jump_flag = 0
    else:
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


    if opcode_decoded in decodings.i_type or opcode_decoded in decodings.load_store_encoding or opcode_decoded in ['beq', 'ble']:
        rs  = line[6:11]
        rt  = line[11:16]
        imm = line[16:]

        rs_decoded = decodings.register_decoding[rs]        
        rt_decoded = decodings.register_decoding[rt]
        imm_decoded = integer_of_16_bit_imm(imm)
        
        print(begining_space + f'Instruction[25:21] --- {rs} --- {rs_decoded} ')
        print(begining_space + f'Instruction[20:16] --- {rt} --- {rt_decoded} ')
        print(begining_space + f'Instruction[15:0 ] --- {imm} --- {imm_decoded}\n')

        if opcode_decoded in decodings.load_store_encoding :
            print(begining_space + f'{opcode_decoded}    {rt_decoded}, {imm_decoded}({rs_decoded}), \n')
        else:
            print(begining_space + f'{opcode_decoded}    {rt_decoded}, {rs_decoded}, {imm_decoded}\n')


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
        print(begining_space + f'Instruction[5 :0 ] --- {func} --- {func_decoded}\n')

        print(begining_space + f'{func_decoded}    {rd_decoded}, {rs_decoded}, {rt_decoded}\n')


    clk+=1


    # ALU phase
    if (opcode_decoded in decodings.i_type) or (opcode_decoded in decodings.load_store_encoding) :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing addition\n')

        print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
        print(begining_space + f'immediate value        :- {imm_decoded}')
        print(begining_space + 'ALU executing...\n')

        # ALU addition
        output = imm_decoded + register_file[rs_decoded]

        print(begining_space + f'Output computed as     :- {register_file[rs_decoded]} + {imm_decoded} = {output}\n\n')

    if opcode_decoded in decodings.r_type :
        opertaion = { 'sub': "subrtation", 'add': "addition", 'mul': "multiplication", 'slt': "Set if less than"}

        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing {opertaion[func_decoded]}\n')
        print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
        print(begining_space + f'register {rt_decoded} contains  :- {register_file[rt_decoded]}')

        print(begining_space + 'ALU executing...\n')


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

        elif func_decoded == 'slt':
            output = rs_value <  rt_value
            operation_character = '<'

        print(begining_space + f'Output computed as     :-  + {register_file[rs_decoded]} {operation_character} {register_file[rt_decoded]} = {output}\n\n')



    if opcode_decoded == "beq":
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:-  (Ex)  ALU performing subtraction\n')

        print(begining_space + f'register {rs_decoded} contains  :- {register_file[rs_decoded]}')
        print(begining_space + f'register {rt_decoded} contains  :- {register_file[rt_decoded]}')

        print(begining_space + 'ALU executing...\n')

        rs_value = register_file[rs_decoded]
        rt_value = register_file[rt_decoded]

        # ALU operation
        output = rs_value - rt_value

        if output != 0 :
            print(begining_space + f'Output computed as     :- {register_file[rt_decoded]} - {register_file[rs_decoded]} = {output}\n')
            print(begining_space + 'No branching happens...\n\n')
            instruction_number += 1
            continue
        else:
            print(begining_space + f'Output computed as     :- {register_file[rt_decoded]} - {register_file[rs_decoded]} = {output}\n')
            print(begining_space + 'Branching happens...\n')
            print(begining_space + f'immediate value        :- {imm_decoded}')
            print(begining_space + f'imm value lshifted by 2:- {imm_decoded*4}\n\n')
            print(begining_space + f'New PC = PC + 4 + imm*4 = PC + 4 + {imm_decoded*4}')

            line = instruction_memory[instruction_number - 1 + 1 + imm_decoded ]
            instruction_number = instruction_number + 1 + imm_decoded
            branch_jump_flag = 1
            continue


    clk+=1






    # Mem Access phase
    if   opcode_decoded == 'sw' :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) Data Memory needs to written onto ...  ')


        print(begining_space + f'register {rt_decoded} = {register_file[rt_decoded]}\n')

        print(begining_space + f'Memory[ rs + imm ]')
        print(begining_space + f'Memory[ {rs_decoded} + {imm_decoded} ]')

        # Writing to data memory
        data_memory[output]  = register_file[rt_decoded]

        print(begining_space + f'Memory[ {output}] = {register_file[rt_decoded]} ')


    elif opcode_decoded == 'lw' :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No memory access required ')
        register_file[rt_decoded] =  data_memory[output]

        print(begining_space + f'Memory[ rs + imm ]')
        print(begining_space + f'Memory[ {rs_decoded} + {imm_decoded} ] = {data_memory[output]}')
        
    else:
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No memory access required ')

    clk+=1



    # MemWriteBack phase
    if opcode_decoded != 'sw' :
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (WriteBack) Writing ALU output back to RegFile  \n')
        
        if opcode_decoded == 'lw' :
            register_file[rt_decoded] = data_memory[output]
            print(begining_space + f'registers {rt_decoded} = Memory[ {output} ] = {data_memory[output]}\n')


        elif opcode_decoded in decodings.i_type :
            register_file[rt_decoded] = output
            print(begining_space + f'registers {rt_decoded} contains :-  {output}\n')


        else:
            register_file[rd_decoded] = output
            print(begining_space + f'registers {rd_decoded} contains :-  {output}\n')
    else:
        print(f'clock cycle {clk:<5}: Instruction No {instruction_number:<5}:- (Mem) No Writing back to register file required ')




    clk+=1
    instruction_number += 1


print(data_memory)
