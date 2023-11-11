#include <bits/stdc++.h>
using namespace std;


class Processor {
public:
    int pc;
    vector<string> instruction_memory;
    unordered_map<string, int> register_file;
    vector<int> data_memory;
    int eof;

    string instruction;
    string opcode_decoded;
    string rs_decoded;
    string rt_decoded;
    string rd_decoded;
    string func_decoded;
    int imm_decoded;
    int ALU_output;
    int Mem_out;

public:
    Processor() : pc(1), eof(0), instruction(""), opcode_decoded(""), rs_decoded(""), rt_decoded(""), rd_decoded(""),
                  func_decoded(""), imm_decoded(0), ALU_output(0), Mem_out(0) {
        // Initialize data_memory with zeros
        data_memory = vector<int>(200, 0);
    }

    void IF(int clk) {
        string line = instruction_memory[pc - 1];
        instruction = line;
        cout << "clock cycle " << clk << ": Instruction No " << pc << ":-  (IF)   PC -> " << instruction << endl;
    }

    void ID(int clk) {
        cout << "clock cycle " << clk << ": Instruction No " << pc << ":-  (ID)   instruction decoded as :-" << endl;

        string opcode = instruction.substr(0, 6);
        opcode_decoded = opcode;
        cout << "                        Instruction[31:26] --- " << opcode << " --- " << opcode_decoded << endl;

        if (opcode_decoded == "beq" || opcode_decoded == "ble") {
            string rs = instruction.substr(6, 5);
            string rt = instruction.substr(11, 5);
            string imm = instruction.substr(16);

            rs_decoded = rs;
            rt_decoded = rt;
            imm_decoded = integer_of_16_bit_imm(imm);

            cout << "                        Instruction[25:21] --- " << rs << " --- " << rs_decoded << endl;
            cout << "                        Instruction[20:16] --- " << rt << " --- " << rt_decoded << endl;
            cout << "                        Instruction[15:0 ] --- " << imm << " --- " << imm_decoded << endl;

            if (opcode_decoded == "ble") {
                cout << "ble    " << rt_decoded << ", " << rs_decoded << ", " << imm_decoded << endl;
            }
            else {
                cout << "beq    " << rt_decoded << ", " << rs_decoded << ", " << imm_decoded << endl;
            }
        }
        // Add more cases for other opcodes and their decodings.
    }

    void ALU(int clk) {
        // ALU operations
        // You can implement ALU operations here.
    }

    void Mem(int clk) {
        // Memory operations (lw, sw)
        // Implement memory operations here.
    }

    void WB(int clk) {
        // Write Back operations
        // Implement write-back operations here.
    }

    int integer_of_16_bit_imm(const string& binary_str) {
        bool is_negative = (binary_str[0] == '1');
        string inverted_str;

        if (is_negative) {
            for (char bit : binary_str) {
                inverted_str += (bit == '0') ? '1' : '0';
            }
            imm_decoded = stoi(inverted_str, nullptr, 2) + 1;
        } else {
            imm_decoded = stoi(binary_str, nullptr, 2);
        }

        if (is_negative) {
            imm_decoded = -imm_decoded;
        }

        return imm_decoded;
    }
};




int main() {
    Processor processor;

    // 1 for sorting, 0 for factorial
    int choice = 0;

    if (choice) {
        int t0, t1, t2;
        cout << "Enter number of integers: ";
        cin >> t0;
        cout << "Enter base address of input: ";
        cin >> t1;
        cout << "Enter base address of output: ";
        cin >> t2;

        string file_path = "bin_sort_CLEAN.txt";
        ifstream file(file_path);

        if (file.is_open()) {
            string line;
            int offset = t2 - t1;
            for (int i = t1; i < t1 + t0; ++i) {
                int num;
                cout << "Enter the number: ";
                cin >> num;

                processor.data_memory[i * 4] = num;
                processor.data_memory[offset + i * 4] = num;
            }
        } else {
            cerr << "Error opening file " << file_path << endl;
            return 1;
        }
    } else {
        int t0, t2;
        cout << "Enter number to find factorial: ";
        cin >> t0;
        cout << "Enter base address of output: ";
        cin >> t2;

        string file_path = "bin_Test.txt";
        ifstream file(file_path);

        if (file.is_open()) {
            processor.instruction_memory.clear();
            string line;
            while (getline(file, line)) {
                processor.instruction_memory.push_back(line);
            }
        } else {
            cerr << "Error opening file " << file_path << endl;
            return 1;
        }

        processor.eof = processor.instruction_memory.size();
        cout << processor.eof << endl;
    }

    processor.register_file = { { "$0",   }, { "$t0", 2 }, { "$t1", 0 }, { "$t2", 0 }, { "$t3", 0 }, { "$t4", 0 }, { "$t5", 0 }, { "$t6", 0 }, { "$t7", 0 }, { "$t8", 0 }, { "$t9", 0 }, { "$s0", 0 }, { "$s1", 0 }, { "$s2", 0 }, { "$s3", 0 }, { "$s4", 0 }, { "$s5", 0 }, { "$s6", 0 }, { "$s7", 0 } };

    int clk = 1;

    while (processor.pc <= processor.eof) {
        processor.IF(clk);
        clk++;

        processor.ID(clk);
        clk++;

        processor.ALU(clk);
        clk++;

        if (processor.opcode_decoded == "beq") {
            continue;
        }

        processor.Mem(clk);
        clk++;

        processor.WB(clk);
        clk++;

        processor.pc++;
    }

    cout << "\n\n\n\n<<---------DATA MEMORY------------>>\n\n";

    cout << "-----------------------------" << endl;
    for (size_t i = 0; i < processor.data_memory.size(); i += 4) {
        for (size_t j = i; j < i + 4; ++j) {
            cout << processor.data_memory[j] << "   |   ";
        }
        cout << endl;
        cout << "-----------------------------" << endl;
    }

    return 0;
}