# s0 -> i
# s1 -> j

# t3 => maximum number of comparisons needed
# i.e  j -> [0 to t3)


1) addi    $s0, $0 , 0		            # i = 0
2) addi	   $t5, $t2, 0			        # t5  <- temp_t2 

outer_loop__:
3)     addi    $s0, $s0, 1             # i++
4)     addi    $t2, $t5, 0             # restoring t2 back to start of array


5)     beq     $s0, $t0, print_sorted_loop_init__
 
    # inner loop initialisation
6)     addi     $s1, $0	, 0		        # j = 0
7)     sub		$t3, $t0, $s0		    # $t3 <- N - i    ( you can do this using one register)

      inner_loop__:
8)     beq     $s1, $t3, outer_loop__  # j == N - i go to outer lopp

9)     lw      $s3, 0($t2)             # s3 <- M[ t2 ]
10)    lw      $s4, 4($t2)             # s4 <- M[t2+4]

11)       addi	   $s7, $s7, 1			# $s7 = $t1 + 0
12)       addi	   $s7, $s7, 100			# $s7 = $t1 + 0
        

    # Only if A[j] > A[j+1] we'll swap
13)    slt		$t1, $s4, $s3		    # $t1 = ($s3 < $s4) ? 1 : 0
14)    beq      $t1, $0, no_swap        # j == N - i go to outer lopp
    

    # swapping
15)    sw		$s3, 4($t2)		        # s3 -> M[t2+4]
16)    sw		$s4, 0($t2)		        # s4 -> M[ t2 ] 

     no_swap:
17)    addi     $s1, $s1, 1            # j++
18)    addi     $t2, $t2, 4            # t2 += 4   
19)    beq		 $0 , $0 , inner_loop__				# next iteration of inner loop


print_sorted_loop_init__:
addi    $s1, $0	, 0		            # j = 0