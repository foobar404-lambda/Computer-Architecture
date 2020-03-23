"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.r = [0] * 8
        self.pc = 0
        self.fl = [0] * 8
        self.address = 0

        # Opcodes
        self.opcodes = {
            "10100000": {"type": 2, "code": "ADD"},
            "10101000": {"type": 2, "code": "AND"},
            "01010000": {"type": 1, "code": "CALL"},
            "10100111": {"type": 2, "code": "CMP"},
            "01100110": {"type": 1, "code": "DEC"},
            "10100011": {"type": 2, "code": "DIV"},
            "00000001": {"type": 0, "code": "HLT"},
            "01100101": {"type": 1, "code": "INC"},
            "01010010": {"type": 1, "code": "INT"},
            "00010011": {"type": 0, "code": "IRET"},
            "01010101": {"type": 1, "code": "JEQ"},
            "01011010": {"type": 1, "code": "JGE"},
            "01010111": {"type": 1, "code": "JGT"},
            "01011001": {"type": 1, "code": "JLE"},
            "01011000": {"type": 1, "code": "JLT"},
            "01010100": {"type": 1, "code": "JMP"},
            "01010110": {"type": 1, "code": "JNE"},
            "10000011": {"type": 2, "code": "LD"},
            "10000010": {"type": 2, "code": "LDI"},
            "10100100": {"type": 2, "code": "MOD"},
            "10100010": {"type": 2, "code": "MUL"},
            "00000000": {"type": 0, "code": "NOP"},
            "01101001": {"type": 1, "code": "NOT"},
            "10101010": {"type": 2, "code": "OR"},
            "01000110": {"type": 1, "code": "POP"},
            "01001000": {"type": 1, "code": "PRA"},
            "01000111": {"type": 1, "code": "PRN"},
            "01000101": {"type": 1, "code": "PUSH"},
            "00010001": {"type": 0, "code": "RET"},
            "10101100": {"type": 2, "code": "SHL"},
            "10101101": {"type": 2, "code": "SHR"},
            "10000100": {"type": 2, "code": "ST"},
            "10100001": {"type": 2, "code": "SUB"},
            "10101011": {"type": 2, "code": "XOR"},
        }

    def load(self):
        """Load a program into memory."""

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[self.address] = instruction
            self.address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "LDI":
            self.r[reg_a] = reg_b
        elif op == "PRN":
            print(self.r[reg_a])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        while self.pc <= self.address:
            ir = bin(self.ram_read(self.pc))[2:].zfill(8)  # binary
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            objMap = self.opcodes[ir]
            op = objMap["code"]

            if op != "HLT":
                self.alu(op, operand_a, operand_b)
                self.pc += 1 + objMap["type"]
            else:
                return

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
