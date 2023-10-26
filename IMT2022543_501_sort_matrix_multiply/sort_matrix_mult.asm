# data that we need to have in random access memory
.data
	next_line:                           .asciiz   "\n"
	inp_statement:                       .asciiz   "Enter No. of integers to be taken as input: "
	inp_int_statement:                   .asciiz   "Enter starting address of inputs(in decimal format)  : "
	out_int_statement:                   .asciiz   "Enter starting address of outputs (in decimal format): "
    matrix_order_inp_statement:          .asciiz   "Enter order of matrix: "
	inp_matrix_A_statement:              .asciiz   "Enter starting address of Matrix A (in decimal format)      : "
	inp_matrix_B_statement:              .asciiz   "Enter starting address of Matrix B (in decimal format)      : "
	inp_matrix_C_statement:              .asciiz   "Enter starting address of output matrix (in decimal format) : "
	enter_int:                           .asciiz   "Enter the integer: "
    inp_enter_matrix_A:                  .asciiz   "------ INPUTS FOR MATRIX A -----"
    inp_enter_matrix_B:                  .asciiz   "------ INPUTS FOR MATRIX B -----"
    inp_enter_matrix_output:             .asciiz   "------ OUTPUT MATRIX C  -----"
    inp_enter_choice:                    .asciiz   "Enter choice ( 1/2/3 )  :"


.text


# Switch case program to sort or matrix multiply
#   1 -> sort numbers
#   2 -> matrix multiply
#   3 -> exit

start:
jal		print_enter_choice
jal     get_input_int
move 	$t9, $t4		# $t9 <- $t4

li		$t1, 1		
beq		$t9, $t1, bubble_start	         # if $t9 == $t1 then goto bubble_start

li		$t1, 2
beq		$t9, $t1, matrix_multiply_start	 # if $t9 == $t1 then goto matrix_multiply_start

li		$t1, 3
beq		$t9, $t1, done                 	 # if $t9 == $t1 then goto done ( EXIT !! )








bubble_start:

# conventions being followed :-
# N ( number of inputs )         -> t0 
# input start address            -> t1
# output start address           -> t2

jal		print_no_of_inputs  
jal     get_input_int
move 	$t0, $t4		        # $t0 <- $t4


jal		print_input_starting_address  
jal     get_input_int
move 	$t1, $t4		        # $t1 <- $t4


jal		print_output_starting_adress 
jal     get_input_int
move 	$t2, $t4		        # $t2 <- $t4



move    $t8, $t1                # temporily store t1 -> t8
move    $t7, $t2                # temporily store t2 -> t7
move    $s0, $zero	            # loop vairable (i)  -> s0

loop1_:  
        beq $s0, $t0, loop1end_ # 

	    jal print_enter_int_from_user
	    jal get_input_int
        # store user inputs to an array starting from t1
	    sw $t4, 0($t1)
	    sw $t4, 0($t2)

	    addi $t1, $t1, 4        # updating t1 to have t1 + 4 value
	    addi $t2, $t2, 4        # updating t2 to have t2 + 4 value
      	addi $s0, $s0, 1        # s0++
        j loop1_                 # jump to top

loop1end_: 
        move $t1, $t8           # t1'    value restored from t8  
        move $t2, $t7           # t1's value restored from t8  




# Bubble sort algorithm

# s0 <- outer_loop variable
# s1 <- inner_loop variable

# outer loop initialisation
addi    $s0, $0	, 0		            # j = 0
addi	$t5, $t2, 0			        # t5  <- temp_t2 

outer_loop__:
    addi    $s0, $s0, 1             # i++
    addi    $t2, $t5, 0             # restoring t2 back to start of array


    beq     $s0, $t0, print_sorted_loop_init__

    # inner loop initialisation
    addi    $s1, $0	, 0		            # j = 0
    sub		$t3, $t0, $s0		    # $t3 <- N - i    ( you can do this using one register)

    inner_loop__:
    beq     $s1, $t3, outer_loop__    # j == N - i go to outer lopp

    lw      $s3, 0($t2)             # s3 <- M[ t2 ]
    lw      $s4, 4($t2)             # s4 <- M[t2+4]

    ble		$s3, $s4, no_swap       # Only if A[j] > A[j+1] we'll swap

    # swapping
    sw		$s3, 4($t2)		        # s3 -> M[t2+4]
    sw		$s4, 0($t2)		        # s4 -> M[ t2 ] 

    no_swap:
    addi     $s1, $s1, 1            # j++
    addi     $t2, $t2, 4            # t2 += 4
    j		inner_loop__				# next iteration of inner loop


print_sorted_loop_init__:
addi    $s1, $0	, 0		            # j = 0


print_sorted_loop:
        beq     $s1, $t0, start      # If i == N, go back to the begining

        # Load and print the integer at address $t1
        lw      $t4, 0($t2)
        jal     print_int
        jal     print_line

        addi    $t2, $t2, 4         # t2 += 4
        addi    $s1, $s1, 1         # i++
        j       print_sorted_loop   













matrix_multiply_start:

# the conventions and logic used would be best understood 
# by comparing it with it's python counterpart



# conventions being followed :-
# N ( Order of matrix  )           -> t0
# N*N                              -> t1 

# Matrix A start address           -> t5
# Matrix B start address           -> t6
# Matrix C start address           -> t7


jal		print_order_of_square_matrix  
jal     get_input_int
move 	$t0, $t4		# $t0 (N)   <-- $t4
mul     $t1, $t0, $t0   # $t1 (N*N) <-- $t0 * $t0


jal		print_matrix_A_starting_address
jal     get_input_int
move 	$t5, $t4		# $t5 <- $t4


jal		print_matrix_B_starting_adress 
jal     get_input_int
move 	$t6, $t4		# $t6 <- $t4


jal		print_matrix_C_starting_adress 
jal     get_input_int
move 	$t7, $t4		# $t7 <- $t4




#jal     print_line
jal     print_line
jal     enter_matrix_A
jal     print_line
#jal     print_line

move    $t8, $t5       # temporily store t5 -> t8
move    $s0, $zero	   # loop vairable (i)  -> s0

# get N*N inputs for matrix A
loop1:  beq $s0, $t1, loop1end

	    jal print_enter_int_from_user
	    jal get_input_int
        # store user inputs to an array starting from t5
	    sw $t4, 0($t5)

	    addi $t5, $t5, 4      # updating t5 to have t5+4 value
      	addi $s0, $s0, 1      # s0 ++
        j loop1               # jump to top

loop1end: move $t5, $t8  # t5's value restored from t8  




#jal     print_line
jal     print_line
jal     enter_matrix_B
jal     print_line
#jal     print_line

move    $t8, $t6       # temporily store t6 -> t8
move    $s0, $zero	   # loop vairable (i)  -> s0

# get N*N inputs for matrix B
loop2:  beq $s0, $t1, loop2end

	    jal print_enter_int_from_user
	    jal get_input_int
        # store user inputs to an array starting from t6
	    sw $t4, 0($t6)

	    addi $t6, $t6, 4      # updating t6 to have t6+4 value
      	addi $s0, $s0, 1      # s0 ++
        j loop2               # jump to top

loop2end: move $t6, $t8  # t6's value restored from t8  






# matrix multiplication

# t0, t1, t4, t5,t6,t7   used 


# row_offset  -> s3 
# clm_offset  -> s4

addi	$s0, $0,  -1		# $s0 -> 0  ( k )
addi	$s3, $0,  0		    # $s3 -> 0  (row_offset)
addi	$s4, $0,  0		    # $s4 -> 0  (clm_offset)
addi	$t3, $0,  4         # $t3 = 4
addi    $t8, $t7, 0         # temporarily sotring matrix C's address

outer_loop: 

addi	$s0, $s0, 1			# k++

beq		$s0, $t1, DONE


divu    $t2, $s0, $t0
mfhi    $t2                 # $t2 <- Remainder

beq		$s0, $zero, inner_loop_init__
bne     $t2, $zero, inner_loop_init__

addi	$s3, $0, 1			# s3++ ( row offset++)
addi	$s4, $0, 0	            # resetting the column offset 


inner_loop_init__:
addi	$s1, $0, 0		        # $s1 <- 0 
addi    $t2, $0, 0              # accumulator C[k]

inner_loop:

beq		$s1, $t0, outside_inner_loop	# if j == N then go outside inner_loop


# generating offsets for matrix A and matrix B

mul     $s7, $s3, $t0
add     $s7, $s7, $s1       # s7 <- index of matrix A

mul     $s6, $s1, $t0
add     $s6, $s6, $s4       # s6 <- index of matrix B


# you have to multiply the index by 4 to get exact offsets 
mul     $s6, $s6, $t3
mul     $s7, $s7, $t3


add     $s7, $s7, $t5       # s7 <- mem address of exact number in matrix A
add     $s6, $s6, $t6       # s6 <- mem address of exact number in matrix B


# A[S7]   B[s6] 
lw		$s6, 0($s6)		    
lw		$s7, 0($s7)		    

# s6 is the result of their multiplication
mul     $s6, $s6, $s7

# Cumulatively summing up
add     $t2, $t2, $s6       # C[k] += s6
addi	$s1, $s1, 1			# j++ 


j		inner_loop			# jump to inner_loop



outside_inner_loop:

# C[k] = A[row_offset*N + j] * B[clm_offset + j*N]
sw		$t2, 0($t7)

addi	$t7, $t7, 4			# moving to next address of matrix C to fill
addi	$s4, $s4, 1			# s4++ ( column offset++)

j       outer_loop


DONE:
addi	$s1, $0, 0		
addi    $t7, $t8, 0







#jal     print_line
jal     print_line
jal     enter_matrix_output
jal     print_line
#jal     print_line


print_output_matrix:
        beq     $s1, $t1, start      # If i == N, go back to initial start

        # Load and print the integer at address $t1
        lw      $t4, 0($t7)
        jal     print_int
        jal     print_line

        addi    $t7, $t7, 4         # t7 += 4
        addi    $s1, $s1, 1         # i++
        j       print_output_matrix   






# Exit the program
done:
        li      $v0, 10
        syscall













print_enter_choice: li $v0,4
		la $a0,inp_enter_choice
		syscall 
		jr $ra

get_input_int: 
        li $v0,5
        syscall
        move $t4,$v0
        jr $ra

#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra

#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_no_of_inputs: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra

print_input_starting_address: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra

print_output_starting_adress: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra

#print enter integer statement
print_enter_int_from_user: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra


enter_matrix_A: li $v0,4
		la $a0, inp_enter_matrix_A
		syscall 
		jr $ra

enter_matrix_B: li $v0,4
		la $a0, inp_enter_matrix_B
		syscall 
		jr $ra


enter_matrix_output: li $v0,4
		la $a0, inp_enter_matrix_output
		syscall 
		jr $ra

print_order_of_square_matrix: li $v0,4
		la $a0,matrix_order_inp_statement
		syscall 
		jr $ra

print_matrix_A_starting_address: li $v0,4
		la $a0,inp_matrix_A_statement
		syscall 
		jr $ra

print_matrix_B_starting_adress: li $v0,4
		la $a0,inp_matrix_B_statement
		syscall 
		jr $ra

print_matrix_C_starting_adress: li $v0,4
		la $a0,inp_matrix_C_statement
		syscall 
		jr $ra