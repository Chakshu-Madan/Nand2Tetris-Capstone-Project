# Nand2Tetris Capstone -- Make the Computer Draw a Box

A capstone project for **Nand to Tetris -- I (ETCCNT301)** at K.R.
Mangalam University. The project builds a Hack computer, implements a
two-pass assembler in Python, and creates a keyboard-controlled screen
box using Hack assembly.

## Project Details

-   **Roll Number:** 2501730068
-   **Personal Number (K):** 68
-   **Box position:** Starts at screen row 68
-   **Box dimensions:** 16 pixels wide × 20 rows high
-   **Assembler extension:** Warns when a label is declared more than
    once (`K mod 3 = 2`)

## Project Parts

### Part A -- Hack Computer

HDL implementation and integration of the CPU, memory and computer, with
supporting chips: - `CPU.hdl` - `Memory.hdl` - `Computer.hdl` -
`ALU.hdl` - `PC.hdl` - `RAM16K.hdl`

The implementation was tested using the official CPU, Memory,
ComputerAdd, ComputerMax and ComputerRect test scripts.

### Part B -- Python Assembler

`assembler.py` translates Hack `.asm` programs into 16-bit `.hack`
machine code using two passes: 1. Records label addresses and removes
comments and blank lines. 2. Encodes A- and C-instructions and allocates
variables from RAM address 16.

Test programs: `Add.asm`, `Max.asm`, `Rect.asm` and `Pong.asm`. Their
generated machine code was compared with the official Nand2Tetris
assembler.

### Part C -- Box Program

`Box.asm` checks the keyboard and draws or clears the assigned box on
the Hack screen. It is assembled with the custom Python assembler to
produce `Box.hack`, then run in the CPU Emulator.

## Run the Assembler

From the `Part_B_Assembler` directory, run:

``` bash
python assembler.py Add.asm
python assembler.py Max.asm
python assembler.py Rect.asm
python assembler.py Pong.asm
```

To assemble the box program from the `Part_B_Assembler` directory:

``` bash
python assembler.py ../Part_C_Box/Box.asm
```

The `.hack` output is created alongside the corresponding `.asm` file.

## Repository Structure

``` text
capstone/
├── Part_A_Computer/
│   ├── CPU.hdl
│   ├── Memory.hdl
│   ├── Computer.hdl
│   ├── ALU.hdl
│   ├── PC.hdl
│   └── RAM16K.hdl
├── Part_B_Assembler/
│   ├── assembler.py
│   └── test .asm/.hack files
├── Part_C_Box/
│   ├── Box.asm
│   └── Box.hack
└── Screenshots/
    ├── Part A/
    ├── Part B/
    └── Part C/
```

## Tools

-   Nand2Tetris Hardware Simulator and CPU Emulator
-   Python 3
-   Visual Studio Code

------------------------------------------------------------------------

**Student:** \[Your Name\]\
**University:** K.R. Mangalam University
