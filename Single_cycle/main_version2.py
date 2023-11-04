import decodings


begining_space = "                        "; 

def integer_of_16_bit_imm(binary_str):
    is_negative = binary_str[0] == '1'

    if is_negative:
        inverted_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        binary_str = bin(int(inverted_str, 2) + 1)[2:]  

    decimal_value = int(binary_str, 2)

    if is_negative:
        decimal_value = -decimal_value

    return decimal_value



class ALU:
     
     def __init__(self):
         pass
 
 
     def adder():
         pass
 
     def subtractor():
         pass
 
     def mutliplier():
        pass
     



class Processor :
     
     def __init__(self):
        self.pc = 1
        
        self.instruction_memory  = []
        self.register_file = {}
        self.ALU = ALU()
        self.data_memory = [0]*200
        self.eof = len(self.instruction_memory)

        self.instruction   = ""

        self.self.opcode_decoded = ""
        self.rs_decoded     = ""        
        self.rt_decoded     = ""
        self.rd_decoded     = ""
        self.func_decoded   = ""
        self.imm_decoded    = ""

        self.ALU_output     = ""


     def IF(self,clk):
        line  = self.instruction_memory[self.pc - 1]
        self.instruction = line.strip()
        print(f'clock cycle {clk:<5}: Instruction No {self.pc :<5}:-  (IF)   PC -> {self.instruction}')



     def ID(self,clk):
        print(f'clock cycle {clk:<5}: Instruction No {self.pc :<5}:-  (ID)   instruction decoded as :-\n')

        opcode = self.instruction[:6]
        self.opcode_decoded = decodings.opcode_decodings[opcode]
        print(begining_space + f'Instruction[31:26] --- {opcode} --- {self.opcode_decoded}')


        if (self.opcode_decoded in decodings.i_type) or (self.opcode_decoded in decodings.load_store_encoding) or (self.opcode_decoded in ['beq', 'ble']) :
            rs  = self.instruction[6:11]
            rt  = self.instruction[11:16]
            imm = self.instruction[16:]


            self.rs_decoded = decodings.register_decoding[rs]        
            self.rt_decoded = decodings.register_decoding[rt]
            self.imm_decoded = integer_of_16_bit_imm(imm)


            print(begining_space + f'Instruction[25:21] --- {rs} --- {self.rs_decoded} ')
            print(begining_space + f'Instruction[20:16] --- {rt} --- {self.rt_decoded} ')
            print(begining_space + f'Instruction[15:0 ] --- {imm} --- {self.imm_decoded}\n')

            if self.opcode_decoded in decodings.load_store_encoding :
                print(begining_space + f'{self.opcode_decoded}    {self.rt_decoded}, {self.imm_decoded}({self.rs_decoded}), \n')
            else:
                print(begining_space + f'{self.opcode_decoded}    {self.rt_decoded}, {self.rs_decoded}, {self.imm_decoded}\n')


        elif self.opcode_decoded in decodings.r_type:
            rs = self.instruction[6:11]
            rt = self.instruction[11:16]
            rd = self.instruction[16:21]
            shamt = self.instruction[21:26]
            func = self.instruction[26:]

            self.rs_decoded    = decodings.register_decoding[rs]        
            self.rt_decoded    = decodings.register_decoding[rt]
            self.rd_decoded    = decodings.register_decoding[rd]
            self.func_decoded  = decodings.func_encoding[func]

            print(begining_space + f'Instruction[25:21] --- {rs} --- { self.rs_decoded } ')
            print(begining_space + f'Instruction[20:16] --- {rt} --- { self.rt_decoded } ')
            print(begining_space + f'Instruction[15:11] --- {rd} --- { self.rd_decoded } ')

            print(begining_space + f'Instruction[10:6 ] --- {shamt} --- 0 ')
            print(begining_space + f'Instruction[5 :0 ] --- {func} --- {self.func_decoded}\n')

            print(begining_space + f'{self.func_decoded}    {self.rd_decoded}, {self.rs_decoded}, {self.rt_decoded}\n')





     def ALU(self,clk):

        if (self.opcode_decoded in decodings.i_type) or (self.opcode_decoded in decodings.load_store_encoding) :
            print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:-  (Ex)  ALU performing addition\n')

            print(begining_space + f'register {self.rs_decoded} contains  :- {self.register_file[self.rs_decoded]}')
            print(begining_space + f'immediate value        :- {self.imm_decoded}')
            print(begining_space + 'ALU executing...\n')

            # ALU addition
            self.ALU_output = self.imm_decoded + self.register_file[self.rs_decoded]

            print(begining_space + f'Output computed as     :- {self.register_file[self.rs_decoded]} + {self.imm_decoded} = {self.ALU_output}\n\n')

        if self.opcode_decoded in decodings.r_type :
            opertaion = { 'sub': "subrtation", 'add': "addition", 'mul': "multiplication", 'slt': "Set if less than"}

            print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:-  (Ex)  ALU performing {opertaion[self.func_decoded]}\n')
            print(begining_space + f'register {self.rs_decoded} contains  :- {self.register_file[self.rs_decoded]}')
            print(begining_space + f'register {self.rt_decoded} contains  :- {self.register_file[self.rt_decoded]}')

            print(begining_space + 'ALU executing...\n')


            rs_value = self.register_file[self.rs_decoded]
            rt_value = self.register_file[self.rt_decoded]

          
            # ALU operation
            if self.func_decoded == 'sub':
                self.ALU_output = rs_value - rt_value
                operation_character = '-'

            elif self.func_decoded == 'add':
                self.ALU_output = rs_value + rt_value
                operation_character = '+'

            elif self.func_decoded == 'mul':
                self.ALU_output = rs_value * rt_value
                operation_character = '*'

            elif self.func_decoded == 'slt':
                self.ALU_output = 1 if rs_value <  rt_value else 0
                operation_character = '<'

            print(begining_space + f'Output computed as     :-  + {self.register_file[self.rs_decoded]} {operation_character} {self.register_file[self.rt_decoded]} = {self.ALU_output}\n\n')



        if self.opcode_decoded == "beq":
            print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:-  (Ex)  ALU performing subtraction\n')

            print(begining_space + f'register {self.rs_decoded} contains  :- {self.register_file[self.rs_decoded]}')
            print(begining_space + f'register {self.rt_decoded} contains  :- {self.register_file[self.rt_decoded]}')

            print(begining_space + 'ALU executing...\n')

            rs_value = self.register_file[self.rs_decoded]
            rt_value = self.register_file[self.rt_decoded]

            # ALU operation
            self.ALU_output = rs_value - rt_value

            if self.ALU_output != 0 :
                print(begining_space + f'Output computed as     :- {self.register_file[self.rt_decoded]} - {self.register_file[self.rs_decoded]} = {self.ALU_output}\n')
                print(begining_space + 'No branching happens...\n\n')
                self.pc += 1
                
            else:
                print(begining_space + f'Output computed as     :- {self.register_file[self.rt_decoded]} - {self.register_file[self.rs_decoded]} = {self.ALU_output}\n')
                print(begining_space + 'Branching happens...\n')
                print(begining_space + f'immediate value        :- {self.imm_decoded}')
                print(begining_space + f'imm value lshifted by 2:- {self.imm_decoded*4}\n\n')
                print(begining_space + f'New PC = PC + 4 + imm*4 = PC + 4 + {self.imm_decoded*4}')

                self.instruction = self.instruction_memory[self.pc - 1 + 1 + self.imm_decoded ]
                self.pc = self.pc + 1 + self.imm_decoded


       

    # Data Memory access stage 
     def Mem(self,clk):
            if   self.opcode_decoded == 'sw' :
                print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:- (Mem) Data Memory needs to written onto ...  ')

                print(begining_space + f'register {self.rt_decoded} = {self.register_file[self.rt_decoded]}\n')

                print(begining_space + f'Memory[ rs + imm ]')
                print(begining_space + f'Memory[ {self.rs_decoded} + {self.imm_decoded} ]')

                # Writing to data memory
                self.data_memory[self.ALU_output]  = self.register_file[self.rt_decoded]

                print(begining_space + f'Memory[ {self.ALU_output}] = {self.register_file[self.rt_decoded]} ')


            elif self.opcode_decoded == 'lw' :
                print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:- (Mem) No memory access required ')
                self.register_file[self.rt_decoded] =  self.data_memory[self.ALU_output]

                print(begining_space + f'Memory[ rs + imm ]')
                print(begining_space + f'Memory[ {self.rs_decoded} + {self.imm_decoded} ] = {self.data_memory[self.ALU_output]}')
                
            else:
                print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:- (Mem) No memory access required ')


     #  Write Back phase
     def WB(self,clk):
         if self.opcode_decoded != 'sw' :
            print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:- (WriteBack) Writing ALU output back to RegFile  \n')
            
            if self.opcode_decoded == 'lw' :
                self.register_file[self.rt_decoded] = self.data_memory[self.ALU_output]
                print(begining_space + f'registers {self.rt_decoded} = Memory[ {self.ALU_output} ] = {self.ata_memory[self.self.ALU_output]}\n')


            elif self.opcode_decoded in decodings.i_type :
                self.register_file[self.rt_decoded] = self.ALU_output
                print(begining_space + f'registers {self.rt_decoded} contains :-  {self.self.ALU_output}\n')


            else:
                self.register_file[self.rd_decoded] = self.ALU_output
                print(begining_space + f'registers {self.rd_decoded} contains :-  {self.ALU_output}\n')
         else:
             print(f'clock cycle {clk:<5}: Instruction No {self.pc:<5}:- (Mem) No Writing back to register file required ')

        







processor = Processor()


file_path = "test_bin_dump.txt" 
with open(file_path, "r") as file:
    processor.instruction_memory = file.readlines()



clk = 1; 

while processor.pc  <= processor.eof:
 
    processor.IF(clk)
    clk += 1

    processor.ID(clk)
    clk += 1

    processor.ALU(clk)
    clk += 1

    if processor.opcode_decoded == "beq" : 
        continue

    processor.Mem(clk)
    clk+=1

    processor.WB(clk)
    clk+1

    processor.pc += 1