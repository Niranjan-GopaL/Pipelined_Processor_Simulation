import decodings


'''        ||<-=- TO DO  -=->||


<--------- REALLY IMPORTANT ----------->

[DONE]
-> Generalise Hazard_detection_unit and Forwarding_unit 

[DONE; built Mem_WB pipeline reg]
-> since Mem works for only lw and sw NO CHANGE HAS BEEN MADE THERE
    -> LW SW support

[DONE]
-> there is no support for beq; bne in the ALU phase 
    ( think on how to  )
    -> how to change pc
    -> how to flush




<---------- LESS IMPORTANT ------------->
-> don't use clock cycles for ( Redudant stuff )  
    -> Mem for r_type 
    -> WB for store
-> printing r_type in print statements
    -> you only have add as '000000'
    -> you need to use func to make it work for all the r_types
-> support for instructions that your assmebly code does not use
    -> bgt
    -> subi
    -> move
    -> li


<---------- EASY FIX -------------> 
[DONE]
-> Instruction number shows 
    -> don't make pc a class member; make it a function parameter
    -> so you can choose what you are displaying WB(clk, pc-4) etc

[DONE]
-> get rid of  class members that were useful in non_pipelined but not in pipelined
        self.rt_decoded
        self.rs_decoded

[DONE]
-> USAGE OF  self.opcode_decoded in ID phase is horrendous

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
        

        self.IF_ID_pipeline_reg    =  []
        

        self.ID_EX_pipeline_reg    = []
        self.forwarded_rs          = ""
        self.forwarded_rt          = ""


        self.require_forwarding_rs = 0
        self.require_forwarding_rt = 0
        self.ALU_output            = ""

        self.ALU_MeM_pipeline_reg  = []

        self.Mem_out               = ""
        
        self.Mem_WB_pipeline_reg   = []



    # Complicated names for clarity
    def Hazard_Detection_and_Forwarding_Unit(self):
        print("\n\n",self.ALU_MeM_pipeline_reg)

        if self.ALU_MeM_pipeline_reg :
            now_op = self.ID_EX_pipeline_reg['op']
            
            ''' HOW IT WORKS 
            
            checking if these match or not :-
            
            instr   rd/rt,  __,  __    <------------------ THIS IS prev
            instr   __   ,  rs,  rt    <------------------ THIS IS NOW

            '''
            
            print("\n---------- forwarding unit ------------")

            if self.ALU_MeM_pipeline_reg[0] == 'beq':
                print("Previous instruction was beq ...")
                print("No need of forwarding ...\n\n")
                return

            if (now_op in decodings.r_type) or (now_op in ['beq', 'bne']):

                rs_now, rt_now = self.ID_EX_pipeline_reg['rs'] , self.ID_EX_pipeline_reg['rt']
                rd_or_rt_prev  = self.ALU_MeM_pipeline_reg[1]

                actual_rs = actual_rt = self.ALU_MeM_pipeline_reg[2]

                print(f'RS to ALU right now : {rs_now}')
                print(f'RT to ALU right now : {rt_now}')
                print(f'PEVIOUS RD/RT       : {rd_or_rt_prev}')


                if rs_now == rd_or_rt_prev :
                    self.require_forwarding_rs = 1 
                    self.forwarded_rs = actual_rs
                    
                if rt_now == rd_or_rt_prev :
                    self.require_forwarding_rt = 1
                    self.forwarded_rt = actual_rt
                    
  
            elif now_op in decodings.i_type :
                rs_now, rt_now = self.ID_EX_pipeline_reg['rs'] , self.ID_EX_pipeline_reg['rt']

                rt_prev   = self.ALU_MeM_pipeline_reg[1]
                actual_rs = self.ALU_MeM_pipeline_reg[2]

                print(f'RT to ALU right now : {rt_now}')
                print(f'PEVIOUS RT          : {rt_prev}')

                if rt_prev == rs_now:
                    self.require_forwarding_rs = 1
                    self.forwarded_rs          = actual_rs

            print('---------------------------------------\n')



    def IF(self, clk, pc):
        line  = self.instruction_memory[pc - 1]
        
        self.IF_ID_pipeline_reg = line.strip()
        print(f'clock cycle {clk:<5}: Instruction No {pc :<5}:-  (IF)   PC -> {self.IF_ID_pipeline_reg}')


    def ID(self, clk, pc):
        print(f'clock cycle {clk:<5}: Instruction No {pc :<5}:-  (ID)   instruction decoded as :-\n')

        opcode = self.IF_ID_pipeline_reg[:6]
        opcode_decoded = decodings.opcode_decodings[opcode]


        if (opcode_decoded in decodings.i_type) or (opcode_decoded in decodings.load_store_encoding) or (opcode_decoded in ['beq', 'ble']) :

            rs  = self.IF_ID_pipeline_reg[6:11]
            rt  = self.IF_ID_pipeline_reg[11:16]
            imm = self.IF_ID_pipeline_reg[16:]


            rs_decoded  = decodings.register_decoding[rs]        
            rt_decoded  = decodings.register_decoding[rt]
            imm_decoded = integer_of_16_bit_imm(imm)


            print(begining_space + f'Instruction[31:26] --- {opcode} --- {opcode_decoded }')
            print(begining_space + f'Instruction[25:21] --- {rs}            --- {rs_decoded} ')
            print(begining_space + f'Instruction[20:16] --- {rt}            --- {rt_decoded} ')
            print(begining_space + f'Instruction[15:0 ] --- {imm} --- {imm_decoded}\n')

            if opcode_decoded in decodings.load_store_encoding :
                print(begining_space + f'{opcode_decoded}    {rt_decoded}, {imm_decoded}({rs_decoded}), \n')
            else:
                print(begining_space + f'{opcode_decoded}    {rt_decoded}, {rs_decoded}, {imm_decoded}\n')

            
            # Loading the values to the ID_EXE pipeline registers
            self.ID_EX_pipeline_reg = {
                'op' :opcode_decoded, 
                'rs' :rs_decoded, 
                'rt' :rt_decoded,
                'imm' :imm_decoded
            }

            print(begining_space + f'Forwarding the source register RS, RT, IMM...')
            print(begining_space + f'ID_Exe_pipeline_reg = {rs_decoded, rt_decoded, imm_decoded}\n\n')




        elif opcode_decoded in decodings.r_type:

            rs    = self.IF_ID_pipeline_reg[6:11]
            rt    = self.IF_ID_pipeline_reg[11:16]
            rd    = self.IF_ID_pipeline_reg[16:21]
            shamt = self.IF_ID_pipeline_reg[21:26]
            func  = self.IF_ID_pipeline_reg[26:]

            rs_decoded    = decodings.register_decoding[rs]        
            rt_decoded    = decodings.register_decoding[rt]
            rd_decoded    = decodings.register_decoding[rd]
            func_decoded  = decodings.func_encoding[func]

            print(begining_space + f'Instruction[31:26] --- {opcode} --- {func_decoded}')

            print(begining_space + f'Instruction[25:21] --- {rs}  --- { rs_decoded } ')
            print(begining_space + f'Instruction[20:16] --- {rt}  --- { rt_decoded } ')
            print(begining_space + f'Instruction[15:11] --- {rd}  --- { rd_decoded } ')

            print(begining_space + f'Instruction[10:6 ] --- {shamt}  --- 0 ')
            print(begining_space + f'Instruction[5 :0 ] --- {func} --- {func_decoded}\n')

            print(begining_space + f'{func_decoded}    {rd_decoded}, {rs_decoded}, {rt_decoded}\n')


            # Loading the values to the ID_EXE pipeline registers
            self.ID_EX_pipeline_reg = {
                'op':opcode_decoded,
                'rs':rs_decoded,           
                'rt':rt_decoded,   
                'rd':rd_decoded,    
                'func':func_decoded,  
            }


            print(begining_space + f'Forwarding the source register RS and RT')
            print(begining_space + f'ID_Exe_pipeline_reg = {rs_decoded, rt_decoded}\n\n')


        
    def ALU(self, clk, pc):
        
        # Checking for hazards
        self.Hazard_Detection_and_Forwarding_Unit()


        # op from the pipeline reg
        op = self.ID_EX_pipeline_reg['op']

            
        if op in decodings.i_type :
            
            # Taking inputs from the pipeline registers
            rs  = self.ID_EX_pipeline_reg['rs']
            rt  = self.ID_EX_pipeline_reg['rt']
            imm = self.ID_EX_pipeline_reg['imm']
        
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Ex)  ALU performing addition\n')

            print(begining_space + f'register {rs} contains  :- {self.register_file[rs]}')
            print(begining_space + f'immediate value        :- {imm}')
            print(begining_space + 'ALU executing...\n')

            
            
            # ALU addition
            if not self.require_forwarding_rs:
                alu_output = imm + self.register_file[rs]
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RS register {rs} ...')
                print(begining_space + f'Current value of   {rs} --> {self.register_file[rs]} ')
                print(begining_space + f'Forwarded value of {rs} --> {self.forwarded_rs} ')

                alu_output = imm + self.forwarded_rs


            print(begining_space + f'Output computed as     :- {self.register_file[rs] if not self.require_forwarding_rs else self.forwarded_rs} + {imm} = {alu_output}\n')


            # Loading both the destination reg and ALU_output to ALU_MeM_pipeline_reg
            # self.ALU_MeM_pipeline_reg = {
            #     "op": op,
            #     "destination_reg": rt,
            #     "ALU_output":alu_output,
            # }
            self.ALU_MeM_pipeline_reg = [op, rt, alu_output]


            print(begining_space + f'Forwarding the destination register RT and ALU_output')
            print(begining_space + f'Exe_Mem_pipeline_reg = {rt, alu_output}\n\n\n')




        elif op in decodings.r_type :
            opertaion = { 'sub': "subrtation", 'add': "addition", 'mul': "multiplication", 'slt': "Set if less than"}

            # Taking inputs from the pipeline registers
            rs    = self.ID_EX_pipeline_reg['rs'  ]
            rt    = self.ID_EX_pipeline_reg['rt'  ]
            rd    = self.ID_EX_pipeline_reg['rd'  ]
            func  = self.ID_EX_pipeline_reg['func']


            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Ex)  ALU performing {opertaion[func]}\n')
            print(begining_space + f'register {rs} contains  :- {self.register_file[rs]}')
            print(begining_space + f'register {rt} contains  :- {self.register_file[rt]}')

            print(begining_space + 'ALU executing...\n')


            if not self.require_forwarding_rs:
                rs_value = self.register_file[rs]
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RS register {rs} ...')
                print(begining_space + f'Current value of   {rs} --> {self.register_file[rs]} ')
                print(begining_space + f'Forwarded value of {rs} --> {self.forwarded_rs}\n')
                rs_value = self.forwarded_rs


            if not self.require_forwarding_rt:
                rt_value = self.register_file[rt]
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RT register {rt} ...')
                print(begining_space + f'Current value of   {rt} --> {self.register_file[rt]} ')
                print(begining_space + f'Forwarded value of {rt} --> {self.forwarded_rt}\n')
                rt_value = self.forwarded_rt

          
            # ALU operation
            if func == 'sub':
                alu_output = rs_value - rt_value
                operation_character = '-'

            elif func == 'add':
                alu_output = rs_value + rt_value
                operation_character = '+'

            elif func == 'mul':
                alu_output = rs_value * rt_value
                operation_character = '*'

            elif func == 'slt':
                alu_output = 1 if rs_value <  rt_value else 0
                operation_character = '<'

            print(begining_space + f'Output computed as     :-  + {rs_value} {operation_character} {rt_value} = {alu_output}\n')


            # Loading both the destination reg and ALU_output to ALU_MeM_pipeline_reg
            # self.ALU_MeM_pipeline_reg = {
            #     "op"         : op,
            #     "destination_reg"         : rd,
            #     "ALU_output" : self.ALU_output
            # }
            self.ALU_MeM_pipeline_reg = [op, rd, alu_output]



            print(begining_space + f'Forwarding the destination register RD and ALU_output')
            print(begining_space + f'Exe_Mem_pipeline_reg = {rd, alu_output}\n\n\n')




        elif op == "beq":
            
            rs = self.ID_EX_pipeline_reg['rs']
            rt = self.ID_EX_pipeline_reg['rt']
            imm = self.ID_EX_pipeline_reg['imm']
            
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Ex)  ALU performing subtraction\n')
            
            if not self.require_forwarding_rs:
                rs_value = self.register_file[rs]
                print(begining_space + f'register {rs} contains  :- {rs_value}')
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RS register {rs} ...')
                print(begining_space + f'Current value of   {rs} --> {self.register_file[rs]} ')
                print(begining_space + f'Forwarded value of {rs} --> {self.forwarded_rs}\n')
                rs_value = self.forwarded_rs


            if not self.require_forwarding_rt:
                rt_value = self.register_file[rt]
                print(begining_space + f'register {rt} contains  :- {rt_value}')
            else:
                print(begining_space + f'Hazard detected ...')
                print(begining_space + f'Using the forwarded value of RT register {rt} ...')
                print(begining_space + f'Current value of   {rt} --> {self.register_file[rt]} ')
                print(begining_space + f'Forwarded value of {rt} --> {self.forwarded_rt}\n')
                rt_value = self.forwarded_rt


            print(begining_space + 'ALU executing...\n')

            # rs_value = self.register_file[rs]
            # rt_value = self.register_file[rt]

            # ALU operation
            alu_output = rt_value - rs_value

            if alu_output != 0 :
                print(begining_space + f'Output computed as     :- {rt_value} - {rs_value} = {alu_output}\n')
                print(begining_space + 'No branching happens...\n\n')

                # Loading the ALU_Mem pipeline registers
                self.ALU_MeM_pipeline_reg = [op]
                
            else:
                print(begining_space + f'Output computed as     :- {self.register_file[rt]} - {self.register_file[rs]} = {alu_output}\n')
                print(begining_space +  'Branching happens...\n')
                print(begining_space + f'immediate value        :- {imm}')
                print(begining_space + f'imm value lshifted by 2:- {imm*4}\n\n')
                print(begining_space + f'New PC = PC + 4 + imm*4 = PC + 4 + {imm*4}')


                self.ID_EX_pipeline_reg   = []
                print(begining_space + f'Flushing ID/EX pipline ...')

                self.ALU_MeM_pipeline_reg = []
                print(begining_space + f'Flushing ALU/Mem pipline ...')

                new_pc = pc + 1 + imm
                return new_pc





        # reseting the control signal
        self.require_forwarding_rs = 0    
        self.require_forwarding_rt = 0    
       


    # Data Memory access stage 
    def Mem(self, clk, pc):

        #  Getting input values from the ALU/Mem pipeline registers
        op= self.ALU_MeM_pipeline_reg[0]

        if len(self.ALU_MeM_pipeline_reg) > 1:
            rt_or_rd   = self.ALU_MeM_pipeline_reg[1]
            alu_output = self.ALU_MeM_pipeline_reg[2]


        # Three forms :-
        # self.Mem_WB_pipeline_reg = [op]                         <--- sw          
        # self.Mem_WB_pipeline_reg = [op, rt_or_rd, mem_out]      <--- lw            
        # self.Mem_WB_pipeline_reg = [op,rt_or_rd,alu_output]     <--- anything else             


        if   op == 'sw' :
            
            rt = rt_or_rd

            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Mem) Data Memory needs to written onto ...  ')

            print(begining_space + f'register {rt} = {self.register_file[rt_or_rd]}\n')
            print(begining_space + f'Storing to Memory[ rs + imm ] ...')

            # Writing to data memory
            self.data_memory[alu_output]  = self.register_file[rt]

            print("---------- intermediate data mem ---------")                

            print(f' rt values       --> {self.register_file[rt]}')
            print(f'Index in data mem -> {alu_output}\n\n')
            print(self.data_memory)

            print("---------- intermediate data mem ---------")                
            
            print(begining_space + f'Memory[ {alu_output}] = {self.register_file[rt]} ')

            # Loading the Mem_WB_pipeline_reg
            # No loading required for store command since there is no WB for store
            self.Mem_WB_pipeline_reg = [op]



        elif op == 'lw' :

            rt = rt_or_rd

            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Mem) Memory access required ')

            mem_out = self.data_memory[alu_output]

            print(begining_space + f'Memory[ rs + imm ]')
            print(begining_space + f'Memory[ {alu_output} ] = {mem_out}')
            
            # Loading the Mem_WB_pipeline_reg
            self.Mem_WB_pipeline_reg = [op, rt, mem_out]


        elif op == 'beq':
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Mem) No memory access required ')
            self.Mem_WB_pipeline_reg = [op]


        else:
            rd = rt_or_rd
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (Mem) No memory access required ')

            # Loading the Mem_WB_pipeline_reg
            self.Mem_WB_pipeline_reg = [op,rd,alu_output]


     #  Write Back phase
    def WB(self, clk,   pc):

        op = self.Mem_WB_pipeline_reg[0]
    
        if op in ['sw','beq'] :
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (WriteBack) No Writing back to register file required ')
        else:
            print(f'clock cycle {clk:<5}: Instruction No {pc:<5}:-  (WriteBack) Writing ALU output back to RegFile  \n')

            rt = self.Mem_WB_pipeline_reg[1]
            
            if op == 'lw' :
                mem_out = self.Mem_WB_pipeline_reg[2]
                self.register_file[rt] = mem_out
                print(begining_space + f'registers {rt} = {mem_out}\n')

            # addi , r_types will write back to registers the out_put of alu
            else:
                alu_out = self.Mem_WB_pipeline_reg[2]
                self.register_file[rt] = alu_out
                print(begining_space + f'registers {rt} contains :-  {alu_out}\n')









processor = Processor()


# 0 for factorial
# 1 for sorting 

choice = 1

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

    file_path = "bin_factorial_CLEAN.txt" 
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




clk = 1; pc = 1; beq_after_flush_flag = 5



def WB_condition()  : 
    return (beq_after_flush_flag == 2) or ( (pc-4 > 0) and (pc-4 <= processor.eof) and (beq_after_flush_flag-4 > 0) )

def Mem_condition() : 
    return (pc-3 > 0) and (pc-3 <= processor.eof) and (beq_after_flush_flag-3 > 0)

def ALU_condition() : 
    return (pc-2 > 0) and (pc-2 <= processor.eof) and (beq_after_flush_flag-2 > 0)

def ID_condition()  : 
    return (pc-1 > 0) and (pc-1 <= processor.eof) and (beq_after_flush_flag-1 > 0)
    
def IF_condition()  :
    return pc <= processor.eof



while pc <= processor.eof + 5 :
 
    if WB_condition():
        if beq_after_flush_flag!=2 :
            processor.WB(clk, pc-4)
        else:    
            processor.WB(clk, temp_pc)

    if  Mem_condition():
        processor.Mem(clk,pc-3)

    if ALU_condition():
        return_alu = processor.ALU(clk,pc-2)

        if return_alu :
            beq_after_flush_flag = 1
            temp_pc = pc
            pc = return_alu 


    if ID_condition():
         processor.ID(clk,pc-1)
         

    if IF_condition():
        processor.IF(clk,pc)
        


    pc += 1; clk += 1
    
    if beq_after_flush_flag != 5 : 
        beq_after_flush_flag += 1
    




print("\n\n\n\n<<---------DATA MEMORY------------>>\n\n")

print("-----------------------------")
for i in range(0,len(processor.data_memory), 4):
    for j in range(i,i+4):
        print(processor.data_memory[j], end= '   |   ')
    print()
    print("-----------------------------")
     

      
# BHT = [
    #  0 (initially NT) : NEXT -> entire PC + 4
    #  and in after ALU you'll understand if your correct or not :-
            # if it was NT then a new entry will be made :-     0 : NEXT -> PC + 4

            # if it was T then a new entry will be made :-      0 : NEXT -> PC + 4 + imm*4

            # so in next iteration we'll look at BHT[-1][0] if it's 0 or 1
            # and get IF( BHT[-1][1] )   



    #  1 (initially T)  : NEXT -> PC + 4 + imm*4 
    #  similar stuff 
# ]


# {
#     "beq_line" : [ 0 , 'PC'+1 ],
#     "beq_line" : [ 1 , 'PC'+4 ]
# }



# <---------------------- BASIC DESIGN ------------------->

# BHT = {
    
#     # when you decode a beq , add that PC adress as a key.
#     # In ALU add the NT and T as the value corresponding to that beq
    
#     # Next time, in ID if you decode and see that it is indeed a beq, and that has an entry in BHT,
#     # NEXT PC needs to be the value correpsonding to that pc

# }


# if processor.pc_from_branch_predictor :
#     # now all the following instruction will be after this pc
#     pc = processor.BHT['branch_pc']
#     processor.IF(clk, pc)
