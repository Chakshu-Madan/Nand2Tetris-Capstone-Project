import sys
import re

PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i

def clean_lines(source):
    instructions = []

    for line in source:
        line = line.split("//")[0].strip()
        if line:
            instructions.append(line)
    return instructions


def first_pass(instructions):
    """Collect labels and their ROM addresses."""

    symbols = PREDEFINED_SYMBOLS.copy()
    declared_labels = set()
    cleaned_instructions = []
    rom_address = 0

    for line in instructions:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()

            if not label:
                raise ValueError("Empty label declaration")

            if label in declared_labels:
                print(f"Warning: Duplicate label '{label}' declared.")
            else:
                declared_labels.add(label)

                if label in symbols:
                    print(f"Warning: Label '{label}' conflicts with a predefined symbol.")
                else:
                    symbols[label] = rom_address

        else:
            cleaned_instructions.append(line)
            rom_address += 1

    return symbols, cleaned_instructions

# Destination codes
DEST_TABLE = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "DM": "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

# Computation codes
COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

# Jump codes
JUMP_TABLE = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def to_binary(value):
    """Convert an integer into a 15-bit binary string."""
    return format(value, "015b")

def assemble_a_instruction(instruction, symbols):
    """Convert an A-instruction into 16-bit binary."""
    symbol = instruction[1:]

    if symbol.isdigit():
        address = int(symbol)
    else:
        if symbol not in symbols:
            symbols[symbol] = assemble_a_instruction.next_variable
            assemble_a_instruction.next_variable += 1

        address = symbols[symbol]

    if not 0 <= address <= 32767:
        raise ValueError(f"Invalid A-instruction address: {address}")

    return "0" + to_binary(address)

# First available RAM address for variables
assemble_a_instruction.next_variable = 16

def assemble_c_instruction(instruction):
    """Convert a C-instruction into 16-bit binary."""

    if "=" in instruction:
        dest, remaining = instruction.split("=", 1)
    else:
        dest, remaining = "", instruction

    if ";" in remaining:
        comp, jump = remaining.split(";", 1)
    else:
        comp, jump = remaining, ""

    dest = dest.strip()
    comp = comp.strip()
    jump = jump.strip()

    if dest not in DEST_TABLE:
        raise ValueError(f"Invalid destination: {dest}")

    if comp not in COMP_TABLE:
        raise ValueError(f"Invalid computation: {comp}")

    if jump not in JUMP_TABLE:
        raise ValueError(f"Invalid jump: {jump}")

    return (
        "111"
        + COMP_TABLE[comp]
        + DEST_TABLE[dest]
        + JUMP_TABLE[jump]
    )

def second_pass(instructions, symbols):
    """Translate all instructions into machine code."""

    machine_code = []

    assemble_a_instruction.next_variable = 16

    for instruction in instructions:
        if instruction.startswith("@"):
            binary = assemble_a_instruction(instruction, symbols)
        else:
            binary = assemble_c_instruction(instruction)

        machine_code.append(binary)

    return machine_code

def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <filename.asm>")
        return

    input_file = sys.argv[1]

    if not input_file.lower().endswith(".asm"):
        print("Error: Input file must have .asm extension.")
        return

    try:
        with open(input_file, "r") as file:
            source = file.readlines()

        # Clean comments and blank lines
        instructions = clean_lines(source)

        # First pass: collect labels
        symbols, instructions = first_pass(instructions)

        # Second pass: generate machine code
        machine_code = second_pass(instructions, symbols)

        # Generate output filename
        output_file = input_file[:-4] + ".hack"

        with open(output_file, "w") as file:
            file.write("\n".join(machine_code) + "\n")

        print(f"Assembly successful!")
        print(f"Output generated: {output_file}")
        print(f"Total instructions: {len(machine_code)}")

    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")

    except ValueError as error:
        print(f"Assembly error: {error}")

if __name__ == "__main__":
    main()