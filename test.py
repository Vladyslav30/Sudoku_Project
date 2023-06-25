# Import numpy library
import numpy as np

# Sample sudoku problem
my_sudoku = [0,7,1,0,6,9,5,0,0,0,0,9,0,0,0,6,0,0,0,0,6,7,0,0,0,9,0,0,9,8,0,0,7,2,6,0,1,3,2,8,0,0,0,7,4,0,0,4,1,9,2,8,3,0,0,0,7,0,8,0,0,0,0,9,1,0,4,0,3,7,8,0,0,8,0,0,0,1,0,0,2]

# Function to create a 9x9 matrix from list
def create_matrix(li):
    matrix = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            matrix[i, j] = li[i*9 + j]
    return matrix

# Function to print the Sudoku board
def print_sudoku(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - ")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if j == 8:
                print(board[i, j])
            else:
                print(str(board[i, j]) + " ", end=" ")

# Function to find an empty space in the board
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

# Function to check if the current board is valid
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

# Function to solve the Sudoku
def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False


