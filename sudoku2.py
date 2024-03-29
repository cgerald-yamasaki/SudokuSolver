
# TO-DO:
# - make universal looping strat that takes in strat name and loops it 
#   until it stops changing then returns?
# - type mat: list to be mat: list[list[int]]
# - make input handling
# - decide whether to use 'block' or 'b_in' for block number/index
# - rename 'block_l_in_ins'
# - 'ins' for indexes switch to 'pos' instead?
# - switch to numpy arrays instead of lists of lists
# - add strat where for example if there are three blanks in a 
#   block and numA can go in blanks x or y and numB can go in 
#   blanks x or y and numC can go in blank z (or some combo of 
#   other blanks), numC must go in blank z.
# - replace 'block_in' with 'block-num'?
# - keep data in format [[0, 3, 8], [1], ...] such that lists 
#   possibilities for each num



import copy

# Notes:
# - 'block' means 3x3 set of numbers in sudoku matrix, e.g. indices (0-2, 0,2) or (3-5, 6-8) inclusive

# *************** TEST SUDOKU MATRICES: commented out mats for visualizing and their code versions ***************

# test1
# [0, 0, 0, 6, 0, 0, 1, 0, 7]
# [6, 8, 0, 9, 5, 1, 3, 0, 0]
# [0, 0, 3, 0, 0, 2, 5, 6, 8]
# [0, 4, 0, 8, 1, 0, 0, 2, 0]
# [0, 0, 0, 0, 0, 0, 8, 5, 1]
# [0, 9, 1, 0, 6, 5, 0, 7, 3]
# [4, 0, 9, 0, 0, 3, 0, 8, 5]
# [1, 6, 2, 0, 0, 9, 0, 3, 0]
# [5, 0, 0, 7, 0, 6, 0, 0, 0]

# actual easy sudoku game, unsolved
test1 = [[0, 0, 0, 6, 0, 0, 1, 0, 7], [6, 8, 0, 9, 5, 1, 3, 0, 0], [0, 0, 3, 0, 0, 2, 5, 6, 8], [0, 4, 0, 8, 1, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 8, 5, 1], [0, 9, 1, 0, 6, 5, 0, 7, 3], [4, 0, 9, 0, 0, 3, 0, 8, 5], [1, 6, 2, 0, 0, 9, 0, 3, 0], [5, 0, 0, 7, 0, 6, 0, 0, 0]]

# test2
# [2, 5, 4, 6, 3, 8, 1, 9, 7]
# [6, 8, 7, 9, 5, 1, 3, 4, 2]
# [9, 1, 3, 4, 7, 2, 5, 6, 8]
# [3, 4, 5, 8, 1, 7, 9, 2, 6]
# [7, 2, 6, 3, 9, 4, 8, 5, 1]
# [8, 9, 1, 2, 6, 5, 4, 7, 3]
# [4, 7, 9, 1, 2, 3, 6, 8, 5]
# [1, 6, 2, 5, 8, 9, 7, 3, 4]
# [5, 3, 8, 7, 4, 6, 2, 1, 9]

# test1, solved
test2 = [[2, 5, 4, 6, 3, 8, 1, 9, 7], [6, 8, 7, 9, 5, 1, 3, 4, 2], [9, 1, 3, 4, 7, 2, 5, 6, 8], [3, 4, 5, 8, 1, 7, 9, 2, 6], [7, 2, 6, 3, 9, 4, 8, 5, 1], [8, 9, 1, 2, 6, 5, 4, 7, 3], [4, 7, 9, 1, 2, 3, 6, 8, 5], [1, 6, 2, 5, 8, 9, 7, 3, 4], [5, 3, 8, 7, 4, 6, 2, 1, 9]]

# test3
# [0, 5, 0, 6, 3, 0, 1, 9, 7]
# [6, 8, 7, 9, 5, 1, 3, 0, 2]
# [0, 1, 3, 0, 0, 2, 5, 6, 8]
# [3, 4, 5, 8, 1, 0, 0, 2, 6]
# [0, 0, 0, 3, 0, 0, 8, 5, 1]
# [8, 9, 1, 0, 6, 5, 4, 7, 3]
# [4, 7, 9, 1, 0, 3, 6, 8, 5]
# [1, 6, 2, 5, 8, 9, 0, 3, 0]
# [5, 3, 8, 7, 0, 6, 0, 1, 0]

# test1, partially solved
test3 = [[0, 5, 0, 6, 3, 0, 1, 9, 7], [6, 8, 7, 9, 5, 1, 3, 0, 2], [0, 1, 3, 0, 0, 2, 5, 6, 8], [3, 4, 5, 8, 1, 0, 0, 2, 6], [0, 0, 0, 3, 0, 0, 8, 5, 1], [8, 9, 1, 0, 6, 5, 4, 7, 3], [4, 7, 9, 1, 0, 3, 6, 8, 5], [1, 6, 2, 5, 8, 9, 0, 3, 0], [5, 3, 8, 7, 0, 6, 0, 1, 0]]

# test4
# [0, 5, 0, 6, 3, 0, 1, 9, 7]
# [6, 8, 7, 9, 5, 1, 3, 0, 2]
# [0, 1, 3, 0, 7, 2, 5, 6, 8]
# [3, 4, 5, 8, 1, 0, 0, 2, 6]
# [0, 0, 0, 3, 0, 0, 8, 5, 1]
# [8, 9, 1, 0, 6, 5, 4, 7, 3]
# [4, 7, 9, 1, 0, 3, 6, 8, 5]
# [1, 6, 2, 5, 8, 9, 0, 3, 0]
# [5, 3, 8, 7, 0, 6, 2, 1, 0]

# test1, partially solved, same as test3 but with (8, 4) and (8, 6) filled in
test4 = [[0, 5, 0, 6, 3, 0, 1, 9, 7], [6, 8, 7, 9, 5, 1, 3, 0, 2], [0, 1, 3, 0, 7, 2, 5, 6, 8], [3, 4, 5, 8, 1, 0, 0, 2, 6], [0, 0, 0, 3, 9, 0, 8, 5, 1], [8, 9, 1, 0, 6, 5, 4, 7, 3], [4, 7, 9, 1, 0, 3, 6, 8, 5], [1, 6, 2, 5, 8, 9, 0, 3, 0], [5, 3, 8, 7, 0, 6, 2, 1, 0]]

# test5
# [0, 0, 0, 0, 0, 0, 0, 0, 8]
# [0, 0, 0, 0, 5, 0, 9, 0, 1]
# [6, 0, 0, 0, 0, 7, 0, 0, 5]
# [0, 3, 0, 0, 6, 0, 0, 9, 0]
# [5, 0, 0, 3, 0, 4, 1, 0, 0]
# [0, 6, 4, 0, 2, 9, 0, 0, 3]
# [0, 7, 0, 0, 9, 0, 0, 0, 4]
# [0, 0, 9, 0, 8, 1, 7, 6, 0]
# [2, 5, 0, 0, 0, 3, 0, 0, 0]

# new, medium level sudoku
test5 = [[0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 5, 0, 9, 0, 1], [6, 0, 0, 0, 0, 7, 0, 0, 5], [0, 3, 0, 0, 6, 0, 0, 9, 0], [5, 0, 0, 3, 0, 4, 1, 0, 0], [0, 6, 4, 0, 2, 9, 0, 0, 3], [0, 7, 0, 0, 9, 0, 0, 0, 4], [0, 0, 9, 0, 8, 1, 7, 6, 0], [2, 5, 0, 0, 0, 3, 0, 0, 0]]

# test6
# [0, 0, 0, 0, 0, 0, 1, 0, 0]
# [0, 0, 2, 0, 9, 0, 0, 0, 0]
# [4, 7, 9, 1, 0, 2, 0, 0, 0]
# [0, 0, 0, 8, 0, 0, 2, 6, 9]
# [0, 0, 0, 0, 0, 0, 0, 0, 8]
# [0, 0, 0, 2, 0, 0, 7, 3, 0]
# [9, 0, 0, 0, 0, 7, 0, 0, 5]
# [6, 0, 0, 9, 1, 0, 0, 0, 0]
# [2, 0, 4, 6, 8, 0, 0, 7, 1]

# new, hard level sudoku
test6 = [[0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 2, 0, 9, 0, 0, 0, 0], [4, 7, 9, 1, 0, 2, 0, 0, 0], [0, 0, 0, 8, 0, 0, 2, 6, 9], [0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 2, 0, 0, 7, 3, 0], [9, 0, 0, 0, 0, 7, 0, 0, 5], [6, 0, 0, 9, 1, 0, 0, 0, 0], [2, 0, 4, 6, 8, 0, 0, 7, 1]]

# test6 solved: 
# 5  3  8 | 7  6  4 | 1  9  2 | 
# 1  6  2 | 5  9  8 | 3  4  7 | 
# 4  7  9 | 1  3  2 | 8  5  6 | 
# -----------------------------
# 3  4  5 | 8  7  1 | 2  6  9 | 
# 7  2  6 | 3  4  9 | 5  1  8 | 
# 8  9  1 | 2  5  6 | 7  3  4 | 
# -----------------------------
# 9  1  3 | 4  2  7 | 6  8  5 | 
# 6  8  7 | 9  1  5 | 4  2  3 | 
# 2  5  4 | 6  8  3 | 9  7  1 | 

# test7:
# 0  0  6 | 8  0  0 | 3  0  5 | 
# 0  5  0 | 0  0  9 | 7  0  6 | 
# 4  0  0 | 2  0  0 | 0  0  0 | 
# -----------------------------
# 5  0  0 | 0  0  7 | 9  0  0 | 
# 1  9  0 | 0  0  0 | 0  0  0 | 
# 0  4  0 | 0  0  0 | 0  8  0 | 
# -----------------------------
# 0  0  0 | 0  0  0 | 0  6  2 | 
# 0  0  0 | 1  3  0 | 0  0  0 | 
# 0  0  0 | 0  0  0 | 5  0  0 | 

# expert level
test7 = [[0, 0, 6, 8, 0, 0, 3, 0, 5], [0, 5, 0, 0, 0, 9, 7, 0, 6], [4, 0, 0, 2, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 7, 9, 0, 0], [1, 9, 0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 6, 2], [0, 0, 0, 1, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0]]

# hard level
test8 = [[0, 0, 8, 0, 0, 7, 0, 0, 0], [0, 4, 0, 9, 0, 0, 0, 6, 0], [1, 9, 0, 0, 8, 3, 5, 0, 0], [0, 0, 0, 0, 0, 8, 0, 1, 0], [6, 0, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 7, 0, 0, 3, 0, 0], [8, 0, 1, 0, 0, 9, 2, 7, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 4, 0, 5]]

# test8, after one iteration of loopstrat
test8b = [[0, 6, 8, 0, 0, 7, 0, 0, 0], [0, 4, 0, 9, 0, 0, 0, 6, 0], [1, 9, 0, 6, 8, 3, 5, 0, 0], [0, 0, 4, 0, 0, 8, 6, 1, 0], [6, 0, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 7, 6, 4, 3, 5, 0], [8, 0, 1, 0, 0, 9, 2, 7, 6], [4, 0, 3, 0, 0, 6, 0, 0, 0], [9, 0, 6, 0, 0, 0, 4, 0, 5]]


# test9:
# 5  6  8 | 4  2  7 | 1  9  3 | 
# 3  4  2 | 9  1  5 | 8  6  7 | 
# 1  9  7 | 6  8  3 | 5  2  4 | 
# -----------------------------
# 7  3  4 | 5  9  8 | 6  1  2 | 
# 6  8  5 | 1  3  2 | 7  4  9 | 
# 2  1  9 | 7  6  4 | 3  5  8 | 
# -----------------------------
# 8  5  1 | 3  4  9 | 2  7  6 | 
# 4  7  3 | 2  5  6 | 9  8  1 | 
# 9  2  6 | 8  7  1 | 4  3  5 | 
# -----------------------------

# test8 solved:
test9 = [[5, 6, 8, 4, 2, 7, 1, 9, 3], [3, 4, 2, 9, 1, 5, 8, 6, 7], [1,  9, 7, 6, 8, 3, 5, 2, 4], [7, 3, 4, 5, 9, 8, 6, 1, 2], [6, 8, 5, 1, 3, 2, 7, 4, 9], [2, 1, 9, 7, 6, 4, 3, 5, 8], [8, 5, 1, 3, 4, 9, 2, 7, 6], [4, 7, 3, 2, 5, 6, 9, 8, 1], [9, 2, 6, 8, 7, 1, 4, 3, 5]]

# *************** HELPER, SURROUNDING APPARATUS, NON-STRAT STUFF ***************

sudoku = test7

def print_mat(mat: list) -> None:       # prints sudoku matrix with lines between blocks
    for i in range(9):
        for j in range(9):
            print(mat[i][j], ' ', end='')
            if (j % 3) == 2: print("| ", end='')
        print("\n")
        if (i % 3) == 2: print("--------------------------------")
    print("\n")

def check_same_nums(mat1: list, mat2: list) -> bool:    # checks that all non_blanks of mat1 are represented the same in mat2 (even if mat2 has additional blanks filled in)
    for i in range(9):
        for j in range(9):
            if mat1[i][j] == 0 or mat1[i][j] == mat2[i][j]:
                continue
            else:
                return False
    return True

def check_row_rules(mat: list) -> bool:     # checks that all rows of mat have 9 elements and cover numbers 1-9 inclusive
    for row in mat:
        if len(row) != 9: 
            return False
        for i in range(1, 10):
            if i not in row:
                return False
    return True

def get_col(mat: list, c_in) -> list:       # given column index (0-8) and total sudoku matrix, returns list of column elements
    col = []
    for row in mat:
        col.append(row[c_in])
    return col

def check_col_rules(mat: list) -> bool:     # checks that all cols of mat have 9 elements and cover numbers 1-9 inclusive
    for c in range(9):
        col = get_col(mat, c)
        if len(col) != 9: 
            return False
        for i in range(1, 10):
            if i not in col:
                return False
    return True

def get_block_ins(block: int) -> list:   # returns list of block's starting row and starting column (eg. block 5 -> [3, 6])
    in_l = []
    in_l.append(int(block / 3) * 3)  # gets row index of first element of block
    in_l.append((block % 3) * 3)     # gets col index of first element in block
    return in_l

def make_block_l(mat: list, block: int) -> list:    # returns list of block's elements row by row
    if block < 0 or block > 8:
        return None
    block_ins = get_block_ins(block)
    block_l = []
    for r in range(3):
        for c in range(3):
            block_l.append(mat[block_ins[0] + r][block_ins[1] + c])
    return block_l

def check_block_rules(mat: list) -> bool:     # returns true if each block has 9 elements and all numbers 1-9 inclusive accounted for
    for b in range(9):
        block_l = make_block_l(mat, b)
        if len(block_l) != 9:
            return False
        for i in range(1, 10):
            if i not in block_l:
                return False
    return True

def check_complete(mat: list) -> bool:   # True if sudoku completed and every number (1-9) accounted for in every row, col, block
    if check_row_rules(mat) and check_col_rules(mat) and check_block_rules(mat):
        return True
    else:
        return False

def mat_of_zeros() -> list:
    mat = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    return mat

def find_changes(mat1: list, mat2: list) -> list:  # given mats that pass check_same_nums, returns mat containing only the numbers of mat2 not included in mat1
    ret_mat = mat_of_zeros()
    for r in range(9):
        for c in range(9):
            if mat1[r][c] != mat2[r][c]:
                ret_mat[r][c] = mat2[r][c]
    return ret_mat

def check_same_mat(mat1: list, mat2: list) -> bool: # checks if mats are exactly the same
    for r_in in range(9):
        if mat1[r_in] != mat2[r_in]:
            return False
    return True

def ins_from_block_in(block, block_in: int) -> list[int]:
    block_ins = get_block_ins(block)
    row_in = int(block_in / 3) + block_ins[0]
    col_in = (block_in % 3) + block_ins[1]
    return [row_in, col_in]

# ******************************************************************************

# IF THERE'S ONE ZERO IN A LINE:

def find_one_zero(l: list) -> int:     # if l has only one blank/zero, returns index of blank in list
    blank_in = 10
    for i in range(9):
        if l[i] == 0:
            if blank_in == 10:
                blank_in = i
            else:
                return 10
    return blank_in      # return 10 means more or less than one zero/blank

def find_missing_nums(l: list) -> list: # given a list (row, col, or block list), returns list of missing numbers (between 1-9 incl)
    missing_nums = []
    for num in range(1, 10):
        if num not in l:
            missing_nums.append(num)
    return missing_nums

def fill_oz_row(mat: list, num=10) -> list:     # returns mat with all rows with only one zero filled
    filled_mat = copy.deepcopy(mat)
    for r_in in range(9): 
        blank_in = find_one_zero(mat[r_in])
        # if num == 9 and r_in == 4: print("r_in=4, blank_in=", blank_in)
        if blank_in != 10:
            if num == 10:
                num = find_missing_nums(mat[r_in])[0]
            filled_mat[r_in][blank_in] = num
    return filled_mat

def fill_oz_col(mat: list, num=10) -> list:     # returns mat with all cols with only one zero/blank filled
    filled_mat = copy.deepcopy(mat)
    for c_in in range(9):
        col = get_col(filled_mat, c_in)    # column as a list
        blank_in = find_one_zero(col)
        if num == 9 and c_in == 2: 
            print("c_in=2, blank_in=", blank_in)
            print(col)
        if blank_in != 10:
            if num == 10:
                num = find_missing_nums(mat[c_in])[0]
            filled_mat[blank_in][c_in] = num
    return filled_mat

def fill_oz_lines(mat: list, num=10) -> list:   # does not change input mat, returns new mat after looping filling one-zero lines until none left
    old_mat = copy.deepcopy(mat)
    new_mat = copy.deepcopy(mat)
    new_mat = fill_oz_row(new_mat, num)
    new_mat = elim_in_blanks(new_mat, num)  # previously didn't have this here and it was a weird bug
    new_mat = fill_oz_col(new_mat, num)
    while new_mat != old_mat:
        old_mat = copy.deepcopy(new_mat)
        new_mat = fill_oz_row(new_mat, num)
        new_mat = elim_in_blanks(new_mat, num)  # previously didn't have this here and it was a weird bug
        new_mat = fill_oz_col(new_mat, num)
    return new_mat

# IF THERE'S ONE ZERO IN A BLOCK:

def block_l_in_ins(block_in: int, block_l_in: int) -> list:    # given block number and index in list of block elements, return [row, col] indices w/ regard to full matrix
    num_ins = get_block_ins(block_in)
    num_ins[0] = num_ins[0] + int(block_l_in / 3)
    num_ins[1] = num_ins[1] + (block_l_in % 3)
    return num_ins

def fill_one_zero_block(mat: list, block_in: int, num=10) -> list:      # if given block has only one blank/zero, fill it. Destructive
    block_l = make_block_l(mat, block_in)
    blank_block_in = find_one_zero(block_l)
    if blank_block_in != 10:
        blank_ins = block_l_in_ins(block_in, blank_block_in)
        if num == 10:
            num = find_missing_nums(block_l)[0]
        mat[blank_ins[0]][blank_ins[1]] = num
    return mat

def fill_oz_blocks(mat: list, num=10) -> list:  # iterates through blocks, fills ones that only have one zero
    for block_in in range(9):
        mat = fill_one_zero_block(mat, block_in, num)  # destructively changes mat 
    return mat

# FULL-MATRIX ELIMINATION STRATEGY (1)
# goes through one NUM at a time
# prep: make a copy of the full sudoku matrix, use this copy for 1-2
# 1. In all rows which contain NUM, replace remaining 0s with 10s
#       - do the same with columns
#       - do the same with blocks
# 2. If all remaining blanks are in a line in a given block, replace 0s in that line in other blocks with 10s
#       - (this is for rows and columns)
#       - repeat this step until there are no changes
# 3. Fill single blanks in rows, cols, and blocks, with num
# 4. Repeat 1-3 until stops changing
# 5. Replace all remaining 10s with 0s again
# 6. Repeat whole process with next number
# 7. Loop through strat with all numbers until stops changing

# STEP 1:

def elim_blanks_row(mat, row_in):   # replaces all blanks with 10s in given row
    for i in range(9):
        if mat[row_in][i] == 0:
            mat[row_in][i] = 10
    return mat

def elim_blanks_col(mat, col_in):   # replaces all blanks with 10s in given col
    for i in range(9):
        if mat[i][col_in] == 0:
            mat[i][col_in] = 10
    return mat

def elim_blanks_block(mat, block_in):  #  replaces all blanks with 10s in given block
    block_ins = get_block_ins(block_in)     # [row, col] of upper left corner of block
    for i in range(3):
        for j in range(3):
            if mat[i + block_ins[0]][j + block_ins[1]] == 0: 
                mat[i + block_ins[0]][j + block_ins[1]] = 10
    return mat

def elim_in_blanks(mat: list, num: int):   # eliminate all blanks in row, col, or block with num, destructive
    for i in range(9):
        if num in mat[i]:
            mat = elim_blanks_row(mat, i)
        col = get_col(mat, i)
        if num in col:
            mat = elim_blanks_col(mat, i)
        block_l = make_block_l(mat, i)
        if num in block_l:
            mat = elim_blanks_block(mat, i)
    return mat

# STEP 2:

def check_blanks_row_block(mat: list, block: int) -> int:  # checks if blanks/zeros in given block are in a row, returns row index (with regard to block, 0-2) or 10 if not in a row
    blank_row = 10
    block_l = make_block_l(mat, block)
    for i in range(9):
        if block_l[i] == 0:
            if blank_row == 10 or int(i / 3) == blank_row:
                blank_row = int(i / 3)
            else: return 10
    block_ins = get_block_ins(block)
    if blank_row == 10: return 10
    return blank_row + block_ins[0]

def check_blanks_col_block(mat: list, block: int) -> int:  # checks if blanks/zeros in given block are in a col, returns col index or 10 if not in a col
    blank_col = 10
    block_l = make_block_l(mat, block)
    for i in range(9):
        if block_l[i] == 0:
            if blank_col == 10 or (i % 3) == blank_col:
                blank_col = (i % 3)
            else: return 10
    block_ins = get_block_ins(block)
    if blank_col == 10: return 10
    return blank_col + block_ins[1]

def elim_row_other_blocks(mat: list, block: int, row: int) -> list:     # returns matrix with row's blanks filled with 10s in adjacent blocks
    block_ins = get_block_ins(block)
    block_row = [block_ins[1], block_ins[1] + 1, block_ins[1] + 2]
    for i in range(9):
        if i in block_row: continue
        elif mat[row][i] == 0: 
            mat[row][i] = 10
    return mat

def elim_col_other_blocks(mat: list, block: int, col: int) -> list:     # returns matrix with col's blanks replaced with 10s in other blocks
    block_ins = get_block_ins(block)
    block_col = [block_ins[0], block_ins[0] + 1, block_ins[0] + 2]
    for i in range(9):
        if i in block_col: continue
        elif mat[i][col] == 0: 
            mat[i][col] = 10
    return mat

def elim_line_blanks(mat: list) -> list:    # iterates through blocks, if all blanks in block are in a line, elim blanks in that line in other blocks
    for block in range(9):
        blank_row = check_blanks_row_block(mat, block)
        if blank_row < 10:
            mat = elim_row_other_blocks(mat, block, blank_row)
        blank_col = check_blanks_col_block(mat, block)
        if blank_col < 10:
            mat = elim_col_other_blocks(mat, block, blank_col)
    return mat

def loop_elb(mat: list) -> list:    # loops elim_line_blanks until no more blanks can be eliminated
    old_mat = copy.deepcopy(mat)
    new_mat = copy.deepcopy(mat)
    new_mat = elim_line_blanks(new_mat)
    while new_mat != old_mat:
        old_mat = copy.deepcopy(new_mat)
        new_mat = elim_line_blanks(new_mat)
    return new_mat

# STEP 3:

def fill_one_zeros(mat: list, num=10) -> list:  # if there is only one 0 left in a line or block, replace with num
    ret_mat = fill_oz_lines(mat, num)
    # if num == 9:
    #     print("fill_oz_lines:")
    #     print_mat(ret_mat)
    ret_mat = elim_in_blanks(ret_mat, num)
    # if num == 9:
    #     print("eliminblanks:")
    #     print_mat(ret_mat)
    ret_mat = fill_oz_blocks(ret_mat, num)
    # if num == 9:
    #     print("fill_oz_blocks:")
    #     print_mat(ret_mat)
    return ret_mat

# STEP 4:

def elim_and_fill(mat: list, num: int) -> list: # do steps 1-3
    # if num == 9: return elim_and_fill_fix(mat, num)
    ret_mat = elim_in_blanks(mat, num)
    ret_mat = loop_elb(ret_mat)
    ret_mat = fill_one_zeros(ret_mat, num)
    return ret_mat

def elim_and_fill_fix(mat: list, num: int) -> list: # do steps 1-3
    ret_mat = elim_in_blanks(mat, num)
    print("elim_in_blanks:")
    print_mat(ret_mat)
    ret_mat = loop_elb(ret_mat)
    print("loop_elb:")
    print_mat(ret_mat)
    ret_mat = fill_one_zeros(ret_mat, num)
    print("fill_one_zeros")
    print_mat(ret_mat)
    return ret_mat

def loop_elim_fill(mat: list, num: int) -> list:    # loop steps 1-3 until mat stops changing
    old_mat = copy.deepcopy(mat)
    new_mat = copy.deepcopy(mat)
    new_mat = elim_and_fill(new_mat, num)
    while new_mat != old_mat:
        old_mat = copy.deepcopy(new_mat)
        new_mat = elim_and_fill(new_mat, num)
    return new_mat

# STEP 5

def replace_10s(mat: list) -> list: # replaces 10s with 0s again
    for r in range(9):
        for c in range(9): 
            if mat[r][c] == 10:
                mat[r][c] = 0
    return mat

# STEP 6

def strat1_numbers(mat: list) -> list:  # steps 1-5
    for num in range(1, 10):
        mat = loop_elim_fill(mat, num)
        mat = replace_10s(mat)
        # print_mat(mat)
    return mat

# STEP 7

# third it loop (4, 2) is 9 as well as (5, 2), test8

def loop_strat1(mat: list) -> list: # loop strategy until stops changing
    old_mat = copy.deepcopy(mat)
    new_mat = copy.deepcopy(mat)
    new_mat = strat1_numbers(new_mat)
    while new_mat != old_mat:
        print_mat(old_mat)
        old_mat = copy.deepcopy(new_mat)
        new_mat = strat1_numbers(new_mat)
    return new_mat

# LINE/BLOCK POSSIBILITIES STRAT if only one of the remaining numbers can go in a blank within a line/block, put that number there
# for a line, for each missing number, make a list of blanks where it could go 
# if there is a blank space that is only in one of the missing numbers' lists, 
# put that number in that blank
# simple version only looking at direct intersections with lines containing num
    # rather than taking into account if adjacent block can only have num in a particular line so that line should be eliminated from block looking at

def row_blank_ins(mat: list[list[int]], row: int) -> list[int]: # returns list of row indices of blanks 
    blanks = []
    for i in range(9):
        if mat[row][i] == 0:
            blanks.append(i)
    return blanks

def row_num_possibilities(mat: list[list[int]], row: int, num: int) -> list[int]:   # returns list of row indices where num could go
    elim_mat = copy.deepcopy(mat)
    elim_mat = elim_in_blanks(elim_mat, num)    # destructive
    return row_blank_ins(elim_mat, row)

def poss_lists_row(mat: list[list[int]], row: int) -> list[list[int]]:    # returns list of missing numbers with where they could go using row-indices
    poss_lists = []     # returns list of lists, for every internal list the first element is the number and 2nd el is list of row-indices of where that number could go
    missing_nums = find_missing_nums(mat[row])
    for num in missing_nums:
        num_poss_list = [num]
        num_poss_list.append(row_num_possibilities(mat, row, num))
        poss_lists.append(num_poss_list)
    return poss_lists   # format [[num1, [index1, index2...]], [num2, [index1...]]]

def find_one_poss(poss_lists: list[list[int, list[int]]]) -> list[list[int]]: # finds all instances where num only has one spot it can go in, returns list of pairs [num, index num must go]
    fill_list = []
    for pl in poss_lists:
        if len(pl[1]) == 1:
            fill_list.append([pl[0], pl[1][0]])
    return fill_list

def poss_fill_list(poss_lists: list, blanks: list): # returns list of nums and indices where num must go in row/col/block
    fill_list = []  # in the format [num, index] where index can be block, row, or col index
    for i in blanks:    # indices of blanks
        only_num = 10
        for l in poss_lists:    # poss_lists is [[num1, [indices where num1 could go]], [num2, ...], ...]
            if i in l[1]:   # if index i is in l's index-possibilities list
                if only_num == 10:
                    only_num = l[0]
                else:
                    only_num = 10
                    break
        if only_num != 10:  # if only one num can go in i
            fill_list.append([only_num, i])
    return fill_list

def merge_fill_lists(poss_lists: list[list[int, list[int]]], blanks: list[int]) -> list[list[int]]: # merges fill_lists (ie from find_one_poss and poss_fill_list) to return list of pairs [num, index where num should go]
    fill_list1 = find_one_poss(poss_lists)
    fill_list2 = poss_fill_list(poss_lists, blanks)
    ret_fill_list = fill_list1
    for fl in fill_list2:
        if fl not in ret_fill_list:
            ret_fill_list.append(fl)
    return ret_fill_list

def possibilities_strat_row(mat: list[list[int]], row: int) -> list[list[int]]: # if only one number can go in a given blank in row, fill blank with that number
    poss_lists = poss_lists_row(mat, row)
    blanks = row_blank_ins(mat, row)
    # fill_list = poss_fill_list(poss_lists, blanks)
    fill_list = merge_fill_lists(poss_lists, blanks)
    for fill_pair in fill_list:
        mat[row][fill_pair[1]] = fill_pair[0]
    return mat

def poss_strat_rows(mat: list[list[int]]) -> list[list[int]]:   # run possibilities_strat_row on each row
    for r in range(9):
        possibilities_strat_row(mat, r)
    return mat

def col_blank_ins(mat: list[list[int]], col: int) -> list[int]: # returns list of col indices of blanks 
    blanks = []
    for i in range(9):
        if mat[i][col] == 0:
            blanks.append(i)
    return blanks

def col_num_possibilities(mat: list[list[int]], col: int, num: int) -> list[int]:   # returns list of col indices where num could go
    elim_mat = copy.deepcopy(mat)
    elim_mat = elim_in_blanks(elim_mat, num)    # destructive
    return col_blank_ins(elim_mat, col)

def poss_lists_col(mat: list[list[int]], col: int) -> list[list[int]]:    # returns list of missing numbers with where they could go using col-indices
    poss_lists = []     # returns list of lists, for every internal list the first element is the number and 2nd el is list of row-indices of where that number could go
    col_list = get_col(mat, col)
    missing_nums = find_missing_nums(col_list)
    for num in missing_nums:
        num_poss_list = [num]
        num_poss_list.append(col_num_possibilities(mat, col, num))
        poss_lists.append(num_poss_list)
    return poss_lists   # format [[num1, [index1, index2...]], [num2, [index1...]]]

def possibilities_strat_col(mat: list[list[int]], col: int) -> list[list[int]]: # if only one number can go in a given blank in col, fill blank with that number
    poss_lists = poss_lists_col(mat, col)
    blanks = col_blank_ins(mat, col)
    # fill_list = poss_fill_list(poss_lists, blanks)
    fill_list = merge_fill_lists(poss_lists, blanks)
    for fill_pair in fill_list:
        mat[fill_pair[1]][col] = fill_pair[0]
    return mat

def poss_strat_cols(mat: list[list[int]]) -> list[list[int]]:   # run possibilities_strat_col on each col
    for c in range(9):
        possibilities_strat_col(mat, c)
    return mat

def block_missing_nums(mat: list[list[int]], block: int) -> list[int]:    # returns list of numbers missing from block
    block_l = make_block_l(mat, block)
    return find_missing_nums(block_l)

def block_num_possibilities(mat: list[list[int]], block: int, num: int) -> list[int]: # returns list of block-indices where num could go
    elim_mat = copy.deepcopy(mat)
    elim_mat = elim_in_blanks(elim_mat, num)    # destructive
    block_l = make_block_l(elim_mat, block)
    possibilities = []
    for i in range(9):
        if block_l[i] == 0:
            possibilities.append(i)
    return possibilities

def poss_lists_block(mat: list[list[int]], block: int) -> list[list[int]]:    # returns list of missing numbers with where they could go using block-indices
    poss_lists = []     # returns list of lists, for every internal list the first element is the number and 2nd el is list of block-indices of where that number could go
    for num in block_missing_nums(mat, block):
        num_poss_list = [num]
        num_poss_list.append(block_num_possibilities(mat, block, num))
        poss_lists.append(num_poss_list)
    return poss_lists   # format [[num1, [index1, index2...]], [num2, [index1...]]]

# ELIM POSSIBILITIES STRAT/addition 
# if two numbers' possibilities lists (for a block or line) each only have
# two options and they're the same spaces, eliminate those possibilites from
# other numbers' possibility lists

def find_pls_pairs_matches(poss_lists: list[list]) -> list[list[int]]: # returns list of nums whose possibilities lists are identical and of length 2 and list of possibilities to be eliminated from other nums' lists
    pls_copy = copy.deepcopy(poss_lists)
    match_nums = []
    match_posss = []
    for pl in poss_lists:
        pls_copy.remove(pl)
        for plc in pls_copy:
            if pl[1] in plc and len(pl[1]) == 2:
                match_nums.append(pl[0])
                match_nums.append(plc[0])
                match_posss.append(pl[1][0])
                match_posss.append(pl[1][1])
    return [match_nums, match_posss]

def elim_pair_match_nums(poss_lists: list[list], matches: list[list[int], list[int]]) -> list[int]:  # given list of matching pairs of possibility lists, returns poss_lists such that pair possible spaces are eliminated from other numbers' poss lists
    for pl in poss_lists:
        if pl[0] in matches[0]: # if first el of poss_lists poss_list is in matches list of nums, skip
            continue
        for poss in matches[1]: # take all items from matches second list out of other possibility lists
            try:
                pl[1].remove(poss)
            except:
                continue
    return poss_lists

def block_blank_ins(mat: list[list[int]], block: int) -> list[int]: # return list of block-indices of blanks in block
    blanks = []
    block_l = make_block_l(mat, block)
    for i in range(9):
        if block_l[i] == 0:
            blanks.append(i)
    return blanks

def possibilities_strat_block(mat: list[list[int]], block: int) -> list[list[int]]: # where only one num can go in a blank in a block, fill that blank w that num
    pls = poss_lists_block(mat, block)
    poss_lists = elim_pair_match_nums(pls, find_pls_pairs_matches(pls))
    blanks = block_blank_ins(mat, block)
    fill_list = merge_fill_lists(poss_lists, blanks)
    for fill_pair in fill_list:
        indices = ins_from_block_in(block, fill_pair[1])
        mat[indices[0]][indices[1]] = fill_pair[0]
    return mat

def poss_strat_blocks(mat: list[list[int]]) -> list[list[int]]: # run possibilities_strat_block on each block
    for block in range(9):
        possibilities_strat_block(mat, block)
    return mat

def poss_strat_all(mat: list[list[int]]) -> list[list[int]]: # performs poss_strat_rows, _cols, and _blocks
    mat = poss_strat_rows(mat)
    mat = poss_strat_cols(mat)
    mat = poss_strat_blocks(mat)
    return mat

def possibilities_strat(mat: list[list[int]]) -> list[list[int]]: # loop strategy until stops changing
    old_mat = copy.deepcopy(mat)
    new_mat = copy.deepcopy(mat)
    new_mat = poss_strat_all(new_mat)
    while new_mat != old_mat:
        old_mat = copy.deepcopy(new_mat)
        new_mat = poss_strat_all(new_mat)
    return new_mat



# *************** USER INPUT ***************

yes_set = ["yes", "true", "True", "Yes", "y", "Y", "ye"]

def enter_input() -> bool:
    input_bool = input("Would you like to enter a sudoku puzzle?\n")
    if input_bool in yes_set:
        return True
    else:
        return False

def input_handler() -> list:
    print("Enter a row in the format\n[1, 0, 4, 5, 0, 0, 3, 2, 9]\nusing 0s for blanks")
    r1 = input("Enter first row:")
    r2 = input("Enter second row:")
    r3 = input("Enter third row:")
    r4 = input("Enter fourth row:")
    r5 = input("Enter fifth row:")
    r6 = input("Enter sixth row:")
    r7 = input("Enter seventh row:")
    r8 = input("Enter eighth row:")
    r9 = input("Enter ninth row:")
    return [r1, r2, r3, r4, r5, r6, r7, r8, r9]

def check_input_mat(mat: list) -> bool: # check that input matrix follows the rules
    pass



def print_info(mat, solved_mat):
    print('Pre-solving:')
    print_mat(mat)
    print('Post-solving:')
    print_mat(solved_mat)
    print('Changes:')
    print_mat(find_changes(mat, solved_mat))
    print('Same numbers?')
    print(check_same_nums(mat, solved_mat))
    print('Completed?')
    print(check_complete(solved_mat))

def run_strats(mat):
    mat = fill_oz_lines(mat)
    mat = fill_oz_blocks(mat)
    mat = loop_strat1(mat)
    print("loop:")
    print_mat(mat)
    # mat = possibilities_strat(mat)
    # print("poss:")
    # print_mat(mat)
    return mat

def main():
    if enter_input():
        input_handler()
    old_mat = copy.deepcopy(sudoku)
    new_mat = copy.deepcopy(sudoku)
    new_mat = run_strats(new_mat)
    while new_mat != old_mat:
        old_mat = copy.deepcopy(new_mat)
        new_mat = run_strats(new_mat)
    print_info(sudoku, new_mat)
    return new_mat

# main()


# *************** CODING TESTS ***************

test8_solved = copy.deepcopy(test8)
test8_solved = run_strats(test8_solved)
print_info(test8, test8_solved)

# loop8 = loop_strat1(test8b)

# loop8 = loop_strat1(test8)
# print_mat(loop8)
# print(check_same_nums(loop8, test9))

# print_mat(test9)

# print(check_complete(test9))
# print(check_same_nums(test8, test9))

# print_mat(loop_strat1(test8))
# print(check_complete(test9))
# print(check_same_nums(test8, test9))
# print(check_complete(test10))
# print(check_same_nums(test8, test10))

# test8_solved = copy.deepcopy(test8)
# test8_solved = run_strats(test8_solved)
# print_info(test8, test8_solved)
# does something weird in loop

# test7_solved = copy.deepcopy(test7)
# test7_solved = run_strats(test7_solved)
# print_info(test7, test7_solved)

# test6_solved = copy.deepcopy(test6)
# test6_solved = run_strats(test6_solved)
# print_info(test6, test6_solved)

# test6_solved = copy.deepcopy(test6)
# test6_solved = possibilities_strat(test6_solved)
# print_info(test6, test6_solved)

# test7_solved = copy.deepcopy(test7)
# test7_solved = possibilities_strat(test7_solved)
# print_info(test7, test7_solved)

# poss_lists = [[1, [1, 2]], [3, [3, 8]], [4, [1, 2]], [5, [7, 8]], [6, [7, 8]], [7, [1, 4, 7]]]
# print(poss_lists)
# matches = find_pls_pairs_matches(poss_lists)
# print(matches)
# print(elim_pair_match_nums(poss_lists, matches))

# poss_lists = [[1, [1, 2, 4, 7, 8]], [3, [3, 8]], [4, [1, 2, 3, 4]], [5, [7, 8]], [6, [7, 8]], [7, [1, 7]]]
# poss_lists = [[1, [1, 2]], [3, [3, 8]], [4, [1, 2]], [5, [7, 8]], [6, [7, 8]], [7, [1, 7]]]
# print(find_pls_pairs_matches(poss_lists))


# poss_lists = poss_lists_block(test7, 1)
# print(poss_lists)
# print(elim_repeat_ps(poss_lists, [7, 8]))

# test7_solved = copy.deepcopy(test7)
# test7_solved = possibilities_strat(test7_solved)
# print_info(test7, test7_solved)

# test6_solved = copy.deepcopy(test6)
# test6_solved = possibilities_strat(test6_solved)
# print_info(test6, test6_solved)

# test5_solved = copy.deepcopy(test5)
# test5_solved = possibilities_strat(test5_solved)
# print_info(test5, test5_solved)

# print_mat(poss_strat_all(test1))

# print_mat(test1)
# test1_solved = copy.deepcopy(test1)
# test1_solved = possibilities_strat(test1_solved)
# print_info(test1, test1_solved)
# print_mat(test1_solved)
# print_mat(find_changes(test1, test1_solved))
# print(check_same_nums(test1_solved, test2))

# print_mat(test1)
# test1_solved = copy.deepcopy(test1)
# poss_strat_cols(test1_solved)
# print_mat(test1_solved)
# print_mat(find_changes(test1, test1_solved))
# print(check_same_nums(test1_solved, test2))

# print_mat(test1)
# test1_solved = copy.deepcopy(test1)
# poss_strat_rows(test1_solved)
# print_mat(test1_solved)
# print_mat(find_changes(test1, test1_solved))
# print(check_same_nums(test1_solved, test2))

# print_mat(test1)
# test1_solved = copy.deepcopy(test1)
# poss_strat_blocks(test1_solved)
# print_mat(test1_solved)
# print_mat(find_changes(test1, test1_solved))
# print(check_same_nums(test1_solved, test2))

# print_mat(test1)
# print(block_blank_ins(test1, 1))
# print(block_blank_ins(test1, 7))

# print_mat(possibilities_strat_block(test1, 1))

# print_mat(test3)
# print_mat(test)

# print_mat(test1)
# print(poss_lists_block(test1, 0))

# print(block_num_possibilities(test1, 0, 1))
# print(block_num_possibilities(test1, 0, 2))
# print(block_num_possibilities(test1, 4, 2))

# input_handler()

# print_mat(test7)
# test7strat1 = loop_strat1(test7)
# print_mat(test7strat1)
# print_mat(find_changes(test7, test7strat1))
# print(check_same_nums(test7, test7strat1))
# print(check_complete(test7strat1))

# print_mat(test6)
# test6strat1 = loop_strat1(test6)
# print_mat(test6strat1)
# print_mat(find_changes(test6, test6strat1))
# print(check_same_nums(test6, test6strat1))
# print(check_complete(test6strat1))

# print_mat(test5)
# test5strat1 = loop_strat1(test5)
# print_mat(test5strat1)
# print_mat(find_changes(test5, test5strat1))
# print(check_same_nums(test5, test5strat1))
# print(check_complete(test5strat1))
# print_mat(loop_elim_fill(test5strat1, 3))

# temptest = [[2, 5, 4, 6, 3, 8, 1, 9, 7], [6, 8, 7, 9, 5, 1, 3, 4, 2], [0, 1, 3, 4, 7, 2, 5, 6, 8], [3, 4, 5, 8, 1, 7, 0, 2, 6], [7, 2, 6, 3, 0, 4, 8, 5, 1], [8, 9, 1, 2, 6, 5, 4, 7, 3], [4, 7, 9, 1, 2, 3, 6, 8, 5], [1, 6, 2, 5, 8, 9, 7, 3, 4], [5, 3, 8, 7, 4, 6, 2, 1, 0]]
# print_mat(strat1_numbers(temptest))

# print_mat(test3)
# test3strat1 = loop_strat1(test3)
# print_mat(test3strat1)
# print_mat(find_changes(test3, test3strat1))
# print(check_same_nums(test3strat1, test2))
# print(check_complete(test3strat1))
# print_mat(fill_one_zeros(test3strat1))

# print_mat(loop_elim_fill(test3, 4))

# print_mat(test3)
# filled4 = loop_elim_fill(test3, 4)
# print_mat(filled4)
# print_mat(replace_10s(filled4))
# print_mat(find_changes(test3, filled4))
# print(check_same_nums(filled4, test2))

# def fill_oz_row2(mat: list, num=10) -> list:     # returns mat with all rows with only one zero filled
#     filled_mat = mat
#     for r_in in range(9): 
#         blank_in = find_one_zero(mat[r_in])
#         if blank_in != 10:
#             if num == 10:
#                 num = find_missing_num(mat[r_in])
#             filled_mat[r_in][blank_in] = num
#     return filled_mat

# test3_filled = fill_oz_row2(copy.deepcopy(test3), 70)
# print_mat(test3_filled)
# print_mat(find_changes(test3, test3_filled))

# test3_elim = loop_elb(test3)
# print_mat(test3_elim)
# print(check_same_nums(test3, test3_elim))

# print_mat(elim_col_other_blocks(test3, 7, 4))
# print_mat(elim_col_other_blocks(test3, 5, 6))

# print_mat(elim_row_other_blocks(test3, 5, 3))
# print_mat(elim_row_other_blocks(test3, 3, 4))

# print(check_blanks_col_block(test3, 2))
# print(check_blanks_col_block(test3, 7))
# print(check_blanks_col_block(test3, 5))
# print(check_blanks_col_block(test3, 6))
# print(check_blanks_col_block(test3, 8))

# print(check_blanks_row_block(test3, 2))
# print(check_blanks_row_block(test3, 3))
# print(check_blanks_row_block(test3, 5))
# print(check_blanks_row_block(test3, 8))
# print(check_blanks_row_block(test3, 6))

# print_mat(test3)
# test3_filled = fill_oz_blocks(test3)
# print_mat(test3_filled)
# print(check_same_nums(test3_filled, test2))

# print(block_l_in_ins(1, 5))
# print(block_l_in_ins(5, 3))

# print(check_same_nums(test3, test4))
# print_mat(find_changes(test3, test4))

# print_mat(test4)
# test4_filled = fill_oz_lines(test4)
# print_mat(test4_filled)
# print_mat(find_changes(test4, test4_filled))

# print_mat(test3)
# old_test3 = copy.deepcopy(test3)
# test3_filled = fill_oz_lines(test3)
# print_mat(test3_filled)
# print_mat(find_changes(test3, test3_filled))
# print_mat(find_changes(old_test3, test3))

# print_mat(test3)
# test3_filled = fill_oz_col(copy.deepcopy(test3))
# print_mat(test3_filled)
# print_mat(find_changes(test3, test3_filled))
# print(check_same_nums(test3, test3_filled))

# print(check_same_nums(test1, test3))
# print_mat(find_changes(test1, test3))
# print_mat(test3)
# test3_filled = fill_oz_row(copy.deepcopy(test3))
# print_mat(test3_filled)
# print_mat(find_changes(test3, test3_filled))

# print_mat(find_changes(test1, test2))
# print(check_same_nums(test1, test2))
# print(check_block_rules(test2))
# print(make_block_l(test1, 5))
