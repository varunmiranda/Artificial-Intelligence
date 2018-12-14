# Elements-of-AI-N-Rooks-N-Queens-N-Knights

This program aims to place N rooks, N queens or N knights in an N * N chess board, such that no two pieces can attack each other. As there are multiple ways to arrange these pieces, the program has an additional functionality to place blocks at certain positions in the chessboard such that a piece cannot be placed there. The program will still find a board configuration that will generate N pieces that don't attack each other.

Command line arguments: 

[1] solve: nqueen nrook or nknight
[2] size of the board: a number that denotes the size of the board and the number of pieces to place
[3] number of blocked spaces: a number that denotes the number of spaces you want to block on the board
[4 onwards] configuration of the blocked spaces: 1 1 7 8 for instance means you blocked two spaces, one at the first row and the first column and the other at the seventh row and eight column
