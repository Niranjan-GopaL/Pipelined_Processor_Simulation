#  t5 -> cumulative product
#  t2 -> N


addi    $t5, $t5, 1
for:
	beq  $t0, $0   endFor
	mul  $t5, $t0, $t5
	addi $t0, $t0, -1
	beq  $0,  $0,  for

endFor:
	sw $t5,0($t2)

