# # t2 = 3
# addi	$t2, $0, 3			    # $t0 = $t1 + 3

# # t1 = N + 3
# add		$t1, $t0, $t2		# $t1 = $t0 + $t2

# # t0 = 2( N + 3)
# add		$t0, $t1, $t1		# $t0 = $t1 - $t1



addi	$t0, $0, 5			    # $t0 = $0 + 5
add		$t1, $t0, $t0		    # $t1 = $t0 + $t0
mul		$t2, $t0, $t1		    # $t2 = $t0 * $t1

# t2 -> 50