import decodings


instruction_memory = []
data_memory        = [0]*100

register_file = {
    '$0': 0,

    '$t0': 10,
    '$t1': '01001',
    '$t2': 43123,
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$t8': '11000',
    '$t9': '11001',

    '$s0': 12,
    '$s1': '10001',
    '$s2': '10010',
    '$s3': '10011',
    '$s4': '10100',
    '$s5': '10101',
    '$s6': '10110',
    '$s7': '10111',
}





file_path = "test_bin_dump.txt" 
with open(file_path, "r") as file:
    instruction_memory = file.readlines()

