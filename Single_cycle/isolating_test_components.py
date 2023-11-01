def integer_of_16_bit_imm(binary_str):
    is_negative = binary_str[0] == '1'

    if is_negative:
        inverted_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        # Convert to decimal and back to binary
        binary_str = bin(int(inverted_str, 2) + 1)[2:]  

    decimal_value = int(binary_str, 2)

    if is_negative:
        decimal_value = -decimal_value

    return decimal_value


vals = ["1111111111110110", "1111111111111010", "0000000000000010", "0000000000001100"]
for i in vals:
    print(integer_of_16_bit_imm(i))