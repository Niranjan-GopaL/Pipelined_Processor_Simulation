# t2 = 3
addi	$t2, $0, 3			# $t0 = $t1 + 3

# t1 = N + 3
add		$t1, $t0, $t2		# $t1 = $t0 + $t2

# t0 = 2( N + 3)
add		$t0, $t1, $t1		# $t0 = $t1 - $t1
