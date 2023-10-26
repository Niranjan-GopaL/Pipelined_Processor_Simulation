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




# matrix multiplication

# t0, t1, t4, t5,t6,t7   used 


# row_offset  -> s3 
# clm_offset  -> s4

addi	$s0, $s0, -1		        # $s0 -> 0  ( k )
addi	$s3, $s3, 0		        # $s3 -> 0  (row_offset)
addi	$s4, $s4, 0		        # $s4 -> 0  (clm_offset)
addi	$t3, $0,  4	    # $t3 = 4
addi    $t8, $t7, 0           # temporarily sotring matrix C's address

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