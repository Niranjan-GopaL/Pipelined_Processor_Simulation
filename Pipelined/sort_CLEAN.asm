# s0 -> i
# s1 -> j

# t3 => maximum number of comparisons needed
# i.e  j -> [0 to t3)


addi    $s0, $0	, 0		            # i = 0
addi	$t5, $t2, 0			        # t5  <- temp_t2 

outer_loop__:
    addi    $s0, $s0, 1             # i++
    addi    $t2, $t5, 0             # restoring t2 back to start of array


    beq     $s0, $t0, print_sorted_loop_init__

    # inner loop initialisation
    addi    $s1, $0	, 0		        # j = 0
    sub		$t3, $t0, $s0		    # $t3 <- N - i    ( you can do this using one register)

    inner_loop__:
    beq     $s1, $t3, outer_loop__  # j == N - i go to outer lopp

    lw      $s3, 0($t2)             # s3 <- M[ t2 ]
    lw      $s4, 4($t2)             # s4 <- M[t2+4]

    addi	$s7, $s7, 1			    # $s7 = $t1 + 0
    addi	$s7, $s7, 100			# $s7 = $t1 + 0

    # Only if A[j] > A[j+1] we'll swap
    slt		$t1, $s4, $s3		    # $t1 = ($s3 < $s4) ? 1 : 0
    beq     $t1, $0, no_swap        # j == N - i go to outer lopp
    

    # swapping
    sw		$s3, 4($t2)		        # s3 -> M[t2+4]
    sw		$s4, 0($t2)		        # s4 -> M[ t2 ] 

    no_swap:
    addi     $s1, $s1, 1            # j++
    addi     $t2, $t2, 4            # t2 += 4   
    beq		 $0 , $0 , inner_loop__				# next iteration of inner loop


print_sorted_loop_init__:
addi    $s1, $0	, 0		            # j = 0