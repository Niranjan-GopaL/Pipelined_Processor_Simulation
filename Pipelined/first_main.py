import decodings


'''

[ LESS IMPORTANT ]
-> don't use clock cycles for WB, Mem etc ( Redudant stuff )
-> printing r_type in print statements
    -> you only have add as '000000'
    -> you need to use func to make it work for all the r_types

EASY FIX 
-> Instruction number shows 
    -> don't make pc a class member; make it a function parameter
    -> so you can choose what you are displaying WB(clk, pc-4) etc

'''




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




class Processor :
     
    def __init__(self):
        
        
        self.instruction_memory  = []
        self.register_file = {}
        self.data_memory = [0]*200
        self.eof = 0

        self.instruction   = ""

        self.opcode_decoded = ""
        self.rs_decoded     = ""        
        self.rt_decoded     = ""
        self.rd_decoded     = ""
        self.func_decoded   = ""
        self.imm_decoded    = ""


        self.ID_EX_pipeline_reg = []
        self.forwarded_rs   = ""
        self.forwarded_rt   = ""


        self.require_forwarding_rs = 0
        self.require_forwarding_rt = 0
        self.ALU_output     = ""

        self.ALU_MeM_pipeline_reg = []

        self.Mem_out        = ""



    # Complicated names for clarity
    def Hazard_Detection_and_Forwarding_Unit(self):
        print(self.ALU_MeM_pipeline_reg)

        if self.ALU_MeM_pipeline_reg :
            previous_op = self.ID_EX_pipeline_reg[0]
            
            ''' HOW IT WORKS 
            
            checking if these match or not :-
            
            instr   rd/rt,  __,  __
            instr   __   ,  rs,  rt

            '''

            if (previous_op in decodings.r_type) or (previous_op in ['beq', 'bne']):
                rs_now, rt_now = self.ID_EX_pipeline_reg[1] , self.ID_EX_pipeline_reg[2]
                rd_or_rt_prev = self.ALU_MeM_pipeline_reg[1]
                actual_rs = actual_rt = self.ALU_MeM_pipeline_reg[2]

                print(rs_now)
                print(rd_or_rt_prev)

                print(rt_now)
                print(rd_or_rt_prev)


                if rs_now == rd_or_rt_prev :
                    self.require_forwarding_rs = 1 
                    self.forwarded_rs = actual_rs
                    
                if rt_now == rd_or_rt_prev :
                    self.require_forwarding_rt = 1
                    self.forwarded_rt = actual_rt
                    
  
            elif previous_op in decodings.i_type :
                rs_now = self.ID_EX_pipeline_reg[1]
                rd_or_rt_prev = self.ALU_MeM_pipeline_reg[1]
                actual_rs = self.ALU_MeM_pipeline_reg[2]


                if rd_or_rt_prev == rs_now:
                    self.require_forwarding_rs = 1
                    self.forwarded_rs = actual_rs




    def IF(self, clk, pc):
        line  = self.instruction_memory[pc - 1]
        self.instruction = line.strip()
        print(f'clock cycle {clk:<5}: Instruction No {pc :<5}:-  (IF)   PC -> {self.instruction}')


    def ID(self, clk, pc):
        print(f'clock cycle {clk:<5}: Instruction No {pc :<5}:-  (ID)   instruction decoded as :-\n')

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


            print(begining_space + f'Instruction[25:21] --- {rs}            --- {self.rs_decoded} ')
            print(begining_space + f'Instruction[20:16] --- {rt}            --- {self.rt_decoded} ')
            print(begining_space + f'Instruction[15:0 ] --- {imm} --- {self.imm_decoded}\n')

            if self.opcode_decoded in decodings.load_store_encoding :
                print(begining_space + f'{self.opcode_decoded}    {self.rt_decoded}, {self.imm_decoded}({self.rs_decoded}), \n')
            else:
                print(begining_space + f'{self.opcode_decoded}    {self.rt_decoded}, {self.rs_decoded}, {self.imm_decoded}\n')


            
            # Loading the values to the ID_EXE pipeline registers
            
            # Loading only RS for i-type and load store
            if self.opcode_decoded not in ['beq','ble']:
                self.ID_EX_pipeline_reg = [self.opcode_decoded, self.rs_decoded ]

                print(begining_space + f'Forwarding the source register RS...')
                print(begining_space + f'ID_Exe_pipeline_reg = {self.rs_decoded}\n\n')

            else:
                # Loading both RS and RT for beq and ble
                self.ID_EX_pipeline_reg = [self.opcode_decoded, self.rs_decoded , self.rt_decoded ]

                print(begining_space + f'Forwarding the source register RS and RT')
                print(begining_space + f'ID_Exe_pipeline_reg = {self.rs_decoded, self.rt_decoded}\n\n')




        elif self.opcode_decoded in decodings.r_type:
            rs    = self.instruction[6:11]
            rt    = self.instruction[11:16]
            rd    = self.instruction[16:21]
            shamt = self.instruction[21:26]
            func  = self.instruction[26:]

            self.rs_decoded    = decodings.register_decoding[rs]        
            self.rt_decoded    = decodings.register_decoding[rt]
            self.rd_decoded    = decodings.register_decoding[rd]
            self.func_decoded  = decodings.func_encoding[func]

            print(begining_space + f'Instruction[25:21] --- {rs}  --- { self.rs_decoded } ')
            print(begining_space + f'Instruction[20:16] --- {rt}  --- { self.rt_decoded } ')
            print(begining_space + f'Instruction[15:11] --- {rd}  --- { self.rd_decoded } ')

            print(begining_space + f'Instruction[10:6 ] --- {shamt}  --- 0 ')
            print(begining_space + f'Instruction[5 :0 ] --- {func} --- {self.func_decoded}\n')

            print(begining_space + f'{self.func_decoded}    {self.rd_decoded}, {self.rs_decoded}, {self.rt_decoded}\n')


            # Loading the values to the ID_EXE pipeline registers
            self.ID_EX_pipeline_reg = [self.opcode_decoded, self.rs_decoded , self.rt_decoded ]

            print(begining_space + f'Forwarding the source register RS and RT')
            print(begining_space + f'ID_Exe_pipeline_reg = {self.rs_decoded, self.rt_decoded}\n\n')


        
    def ALU(self, clk, pc):
        
        # Checking for hazards
        self.Hazard_Detection_and_Forwarding_Unit()


        if self.opcode_decoded in decodings.i_type :
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Ex)  ALU performing addition\n')

            print(begining_space + f'register {self.rs_decoded} contains  :- {self.register_file[self.rs_decoded]}')
            print(begining_space + f'immediate value        :- {self.imm_decoded}')
            print(begining_space + 'ALU executing...\n')

            
            # ALU addition
            
            
            if not self.require_forwarding_rs:
                self.ALU_output = self.imm_decoded + self.register_file[self.rs_decoded]
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RS register {self.rs_decoded} ...')
                print(begining_space + f'Current value of   {self.rs_decoded} --> {self.register_file[self.rs_decoded]} ')
                print(begining_space + f'Forwarded value of {self.rs_decoded} --> {self.forwarded_rs} ')

                self.ALU_output = self.imm_decoded + self.forwarded_rs


            print(begining_space + f'Output computed as     :- {self.register_file[self.rs_decoded] if not self.require_forwarding_rs else self.forwarded_rs} + {self.imm_decoded} = {self.ALU_output}\n')

            # Loading the pipelined registers
            self.ALU_MeM_pipeline_reg = [self.opcode_decoded,self.rt_decoded,self.ALU_output]
            print(begining_space + f'Forwarding the destination register RT and ALU_output')
            print(begining_space + f'Exe_Mem_pipeline_reg = {self.rt_decoded, self.ALU_output}\n\n\n')




        elif self.opcode_decoded in decodings.r_type :
            opertaion = { 'sub': "subrtation", 'add': "addition", 'mul': "multiplication", 'slt': "Set if less than"}

            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Ex)  ALU performing {opertaion[self.func_decoded]}\n')
            print(begining_space + f'register {self.rs_decoded} contains  :- {self.register_file[self.rs_decoded]}')
            print(begining_space + f'register {self.rt_decoded} contains  :- {self.register_file[self.rt_decoded]}')

            print(begining_space + 'ALU executing...\n')


            if not self.require_forwarding_rs:
                rs_value = self.register_file[self.rs_decoded]
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RS register {self.rs_decoded} ...')
                print(begining_space + f'Current value of   {self.rs_decoded} --> {self.register_file[self.rs_decoded]} ')
                print(begining_space + f'Forwarded value of {self.rs_decoded} --> {self.forwarded_rs}\n')
                rs_value = self.forwarded_rs


            if not self.require_forwarding_rt:
                rt_value = self.register_file[self.rt_decoded]
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RT register {self.rt_decoded} ...')
                print(begining_space + f'Current value of   {self.rt_decoded} --> {self.register_file[self.rt_decoded]} ')
                print(begining_space + f'Forwarded value of {self.rt_decoded} --> {self.forwarded_rt}\n')
                rt_value = self.forwarded_rt

          
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

            print(begining_space + f'Output computed as     :-  + {rs_value} {operation_character} {rt_value} = {self.ALU_output}\n')

            # Loading the pipelined registers
            self.ALU_MeM_pipeline_reg = [self.opcode_decoded,self.rd_decoded, self.ALU_output]
            print(begining_space + f'Forwarding the destination register RD and ALU_output')
            print(begining_space + f'Exe_Mem_pipeline_reg = {self.rt_decoded, self.ALU_output}\n\n\n')




        elif self.opcode_decoded == "beq":
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Ex)  ALU performing subtraction\n')

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
                pc += 1
                
            else:
                print(begining_space + f'Output computed as     :- {self.register_file[self.rt_decoded]} - {self.register_file[self.rs_decoded]} = {self.ALU_output}\n')
                print(begining_space + 'Branching happens...\n')
                print(begining_space + f'immediate value        :- {self.imm_decoded}')
                print(begining_space + f'imm value lshifted by 2:- {self.imm_decoded*4}\n\n')
                print(begining_space + f'New PC = PC + 4 + imm*4 = PC + 4 + {self.imm_decoded*4}')

                self.instruction = self.instruction_memory[pc - 1 + 1 + self.imm_decoded ]
                pc = pc + 1 + self.imm_decoded

        # reseting the control signal
        self.require_forwarding_rs = 0    
        self.require_forwarding_rt = 0    
       

    # Data Memory access stage 
    def Mem(self, clk, pc):
            if   self.opcode_decoded == 'sw' :
                print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:- (Mem) Data Memory needs to written onto ...  ')

                print(begining_space + f'register {self.rt_decoded} = {self.register_file[self.rt_decoded]}\n')

                print(begining_space + f'Memory[ rs + imm ]')
                print(begining_space + f'Memory[ {self.rs_decoded} + {self.imm_decoded} ]')

                # Writing to data memory
                self.data_memory[self.ALU_output]  = self.register_file[self.rt_decoded]

                print(begining_space + f'Memory[ {self.ALU_output}] = {self.register_file[self.rt_decoded]} ')


            elif self.opcode_decoded == 'lw' :
                print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:- (Mem) Memory access required ')

                self.Mem_out = self.data_memory[self.ALU_output]

                print(begining_space + f'Memory[ rs + imm ]')
                print(begining_space + f'Memory[ {self.rs_decoded} + {self.imm_decoded} ] = {self.data_memory[self.ALU_output]}')
                
            else:
                print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:- (Mem) No memory access required ')


     #  Write Back phase
    def WB(self, clk,   pc):
         if self.opcode_decoded != 'sw' :
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:- (WriteBack) Writing ALU output back to RegFile  \n')
            
            if self.opcode_decoded == 'lw' :
                self.register_file[self.rt_decoded] = self.Mem_out
                print(begining_space + f'registers {self.rt_decoded} = Memory[ {self.ALU_output} ] = {self.data_memory[self.ALU_output]}\n')


            elif self.opcode_decoded in decodings.i_type :
                self.register_file[self.rt_decoded] = self.ALU_output
                print(begining_space + f'registers {self.rt_decoded} contains :-  {self.ALU_output}\n')


            else:
                self.register_file[self.rd_decoded] = self.ALU_output
                print(begining_space + f'registers {self.rd_decoded} contains :-  {self.ALU_output}\n')
         else:
             print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:- (Mem) No Writing back to register file required ')

        







processor = Processor()


# 1 for sorting 
# 0 for factorial

choice = 0

if choice :
    t0 = int(input("Enter number of integers:"))
    t1 = int(input("Enter base address of input:"))
    t2 = int(input("Enter base address of output:"))

    file_path = "bin_sort_CLEAN.txt" 
    with open(file_path, "r") as file:
        processor.instruction_memory = file.readlines()

    offset = t2 - t1
    for i in range(t1,t1 + t0):
            num = int(input("Enter the number:"))
            processor.data_memory[i*4] = num
            processor.data_memory[offset + i*4 ] = num 
        
else:
    t0 = int(input("Enter number to find factorial:"))
    t2 = int(input("Enter base address of output:"))

    file_path = "bin_test.txt" 
    with open(file_path, "r") as file:
        processor.instruction_memory = file.readlines()


processor.eof = len(processor.instruction_memory)

processor.register_file = {
        "$0":0,

        "$t0" : t0,
        "$t1" : t1 if choice else 0,
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




clk = 1; pc = 1


while pc <= processor.eof + 5 :
 
    if (pc-4 > 0) and (pc-4 <= processor.eof):
        processor.WB(clk,pc-4)

    if (pc-3 > 0) and (pc-3 <= processor.eof):
        processor.Mem(clk,pc-3)

    if (pc-2 > 0) and (pc-2 <= processor.eof):
        processor.ALU(clk,pc-2)
        if processor.opcode_decoded == "beq" : 
            continue

    if (pc-1 > 0) and (pc-1 <= processor.eof):
        processor.ID(clk,pc-1)


    if pc <= processor.eof:
        processor.IF(clk,pc)
    pc += 1   

    clk += 1
    
    

print("\n\n\n\n<<---------DATA MEMORY------------>>\n\n")

print("-----------------------------")
for i in range(0,len(processor.data_memory), 4):
    for j in range(i,i+4):
        print(processor.data_memory[j], end= '   |   ')
    print()
    print("-----------------------------")
     