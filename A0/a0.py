#!/usr/bin/env python3
# nrooks.py : Solve the N-Rooks, N-Queens and N-Knights problem!
# Based on the Prof. David Crandall's starter code
# Created by Varun Miranda, 2018

# a0.py : Solve the N-Rooks, N-Queens and N-Knights problem!

#Citations : 
#https://docs.python.org/3/library/functions.html - implementing the zip function

import sys

# Count # of pieces in given row
def count_on_row(board, row):    
    return sum(board[row]) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum([row[col] for row in board]) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

####################### N-ROOKS PROBLEM ##############################################

# Get list of successors of given board state
def successors_nrooks(board):      

    board_array = []
    if count_pieces(board) < N:
        for c in range(0,N):
            if count_on_col(board, c) == 0:        
                for r in range(0,N):
                    if count_on_row(board, r) == 0:
                        if (r,c) not in zip(k_array,l_array):
                            if board not in [add_piece(board, r, c)]:                    
                                board_array = board_array + [add_piece(board, r, c)]            
    return board_array
     
     
# check if board is a goal state
def is_goal_nrooks(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

########################### N-QUEENS PROBLEM ###########################################

# Create a function that checks diagonals
def diagonal(board):
     
    final_val = 0
    
    for col in range(0,N):
        for row in range(0,N):
            for count in range(1,N):
                if row+count < N and col+count < N: 
                    if board[row][col] + board[row+count][col+count] > 1:
                        final_val = 1
                        
                if row+count < N and col-count >= 0: 
                    if board[row][col] + board[row+count][col-count] > 1:
                        final_val = 1
                        
                if row-count >= 0 and col+count < N: 
                    if board[row][col] + board[row-count][col+count] > 1:
                        final_val = 1
                        
                if row-count >= 0 and col-count >= 0: 
                    if board[row][col] + board[row-count][col-count] > 1:
                        final_val = 1
    return final_val

# Get list of successors of given board state
def successors_nqueens(board):      
    board_array = []
    final_val = 0
    if count_pieces(board) < N:
        for c in range(0,N):
            if count_on_col(board, c) == 0:        
                for r in range(0,N):
                    if count_on_row(board, r) == 0:
                        if (r,c) not in zip(k_array,l_array): 
                            if board not in [add_piece(board, r, c)]:                    
                                final_val = diagonal(board)         
                                if final_val == 0:
                                    board_array = board_array + [add_piece(board, r, c)]              
    
    return board_array
     
     
# check if board is a goal state
def is_goal_nqueens(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) and \
        diagonal(board) == 0

#######################  N-KNIGHTS PROBLEM ##############################################

# Check the places where a knight can attack another knight
def knight_moves(board):
    
    final_val = 0
    
    for col in range(0,N):
        for row in range(0,N):    
            if row+1 < N and col+2 < N: 
                if board[row][col] + board[row+1][col+2] > 1:
                    final_val = 1                  
            if row+1 < N and col-2 >= 0: 
                if board[row][col] + board[row+1][col-2] > 1:
                    final_val = 1
            if row-1 >= 0 and col+2 < N: 
                if board[row][col] + board[row-1][col+2] > 1:
                    final_val = 1
            if row-1 >= 0 and col-2 >= 0: 
                if board[row][col] + board[row-1][col-2] > 1:
                    final_val = 1
                    
            if row+2 < N and col+1 < N: 
                if board[row][col] + board[row+2][col+1] > 1:
                    final_val = 1                  
            if row+2 < N and col-1 >= 0: 
                if board[row][col] + board[row+2][col-1] > 1:
                    final_val = 1
            if row-2 >= 0 and col+1 < N: 
                if board[row][col] + board[row-2][col+1] > 1:
                    final_val = 1
            if row-2 >= 0 and col-1 >= 0: 
                if board[row][col] + board[row-2][col-1] > 1:
                    final_val = 1

    return final_val

# Get list of successors of given board state
def successors_nknights(board):      

    board_array = []
    final_val = 0
    if count_pieces(board) < N:
        for c in range(0,N):       
                for r in range(0,N):
                    if (r,c) not in zip(k_array,l_array):
                        if board not in [add_piece(board, r, c)]:                    

                            final_val = knight_moves(board) 
                                        
                            if final_val == 0:
                                board_array = board_array + [add_piece(board, r, c)]

    return board_array
     
     
# check if board is a goal state
def is_goal_nknights(board):
    return count_pieces(board) == N and \
    knight_moves(board) == 0

###########################################################################################

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[2])

initial_board = [[0 for i in range(N)] for j in range(N)]   
blocked_spaces = int(sys.argv[3])

k_array = []
l_array = []

for i in range(4,4+(blocked_spaces*2),2):
    j = i+1
    k = int(sys.argv[i])-1
    k_array = k_array + [k]
    l = int(sys.argv[j])-1
    l_array = l_array + [l]

# Return a string with the board rendered in a human-friendly format
def printable_board(board):    
    str = ""
    for row in range(0,N):
        for col in range(0,N): 
            if (row,col) in zip(k_array,l_array):
                str = str + "X "
            elif board[row][col] == 0:
                str = str + "_ "
            else:
                if(sys.argv[1] == 'nrook'):
                    str = str + "R "   
                elif(sys.argv[1] == 'nqueen'):
                    str = str + "Q "
                elif(sys.argv[1] == 'nknight'):
                    str = str + "K "
        str = str + "\n"            
    return str

# Solve N-rooks, N-queens or N-knights
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        if sys.argv[1] == 'nrook':
            for s in successors_nrooks(fringe.pop()):
                if is_goal_nrooks(s):
                    return(s)
                fringe.append(s)
        elif sys.argv[1] == 'nqueen':
            for s in successors_nqueens(fringe.pop()):
                if is_goal_nqueens(s):
                    return(s)
                fringe.append(s)
        elif sys.argv[1] == 'nknight':
            for s in successors_nknights(fringe.pop()):
                if is_goal_nknights(s):
                    return(s)
                fringe.append(s)
    return False

print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")





