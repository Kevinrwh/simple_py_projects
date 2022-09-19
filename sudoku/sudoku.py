from pprint import pprint

def find_next_empty(puzzle):
    # Find the next row, col in the puzzle that's not filled in yet.
    # return row, col tuple (or (None, None) if there is none)
    # Keep in mind we're zero-indexing so 0-8 are our indices
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r,c
    
    return None, None # no spaces left

def is_valid(puzzle, guess, row, col):
    # Figures out if the guess is valid. Return True if so, False if not.
    # Guess is false is the row OR col or the square have the value

    # Row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    # Col
    col_vals = []
    # for i in range(9):
    #     col_vals.append(puzzle[i])
    col_vals = [puzzle[i][col] for i in range(9)] # using list comprehension
    if guess in col_vals:
        return False
    
    # Then the square
    # We want to get where the 3x3 square starts and iterate over the 3 values in the row/col
    row_start = (row // 3) * 3 # 1 // 3 = 0, 5 // 3 = 1 and so on
    col_start = (col // 3 ) * 3 

    for r in range(row_start, row_start+3):
        for c in range(col_start, col_start+1):
            if puzzle[r][c] == guess:
                return False
    
    return True # guess is valid


def solve_sudoku(puzzle):
    # Solving a sudoku puzzle using backtracking
    # The puzzle is a list of lists, where each innner list is a row
    # Return whether a solution exists
    # Mutate the puzzle to be the solution (if the solution exists)

    # Step 1: Check where we can go in the puzzle
    row, col = find_next_empty(puzzle)

    # Step 1.1: If nowhere left, then we're done because we only allowed valid inputs
    if row is None:
        return True # puzzle has been solved
    
    # Step 2: If there's an empty spot to place a guess, make a guess between 1-9
    for guess in range(1,10):
        # Step 3: Check if it's a valid guess
        if is_valid(puzzle, guess, row, col):
            # Step 3.1: If valid, place the guess on the puzzle
            puzzle[row][col] = guess

            # now recurse using this puzzle!
            # Step 4
            if solve_sudoku(puzzle):
                return True
        
        # Step 5: guess is not valid OR guess does not solve the puzzle 
        puzzle[row][col] = -1 # reset the value - backtrack
    
    # Step 6: None of the numbers we try work, so this puzzle is unsolvable
    return False

if __name__ == '__main__':

    # Initialize an example board
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]

    # Determine if we can solve it!
    print(solve_sudoku(example_board))
    pprint(example_board)