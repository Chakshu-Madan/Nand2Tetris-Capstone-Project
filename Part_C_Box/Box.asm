// ==========================================
// Roll Number: 2501730068
// K = 68
// Starting Row = 68
// Height = 20 rows
// Width = 16 pixels
// ==========================================

(LOOP)
    // Check whether a key is pressed
    @KBD
    D=M
    @DRAW
    D;JGT

    // KEY RELEASED: CLEAR THE BOX
    @18560
    D=A
    @addr
    M=D

    @20
    D=A
    @rows
    M=D

(CLEAR_LOOP)
    @addr
    A=M
    M=0

    @32
    D=A
    @addr
    M=D+M

    @rows
    MD=M-1
    @CLEAR_LOOP
    D;JGT

    @LOOP
    0;JMP

    // KEY PRESSED: DRAW THE BOX
(DRAW)
    @18560
    D=A
    @addr
    M=D

    @20
    D=A
    @rows
    M=D

(DRAW_LOOP)
    @addr
    A=M
    M=-1

    @32
    D=A
    @addr
    M=D+M

    @rows
    MD=M-1
    @DRAW_LOOP
    D;JGT

    @LOOP
    0;JMP
