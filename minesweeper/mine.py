import random
import re

# Board creation
class Board:
    def __init__(self, dim_size, num_bombs) -> None:
        # Keep track of dimensions and number of bombs
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Initial set of locations dug into as a set of tuples
        self.dug = set()

        # Make the board
        self.board = self.make_new_board() # plant bombs
        
        # Add values to the board
        self.assign_values_to_board()

    # Helper function to make the board given dimensions and number of bombs.
    def make_new_board(self):

        # Initialize 2D board given dimensions
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # Track bombs
        bombs_planted = 0

        # Plant the bombs
        while bombs_planted < self.num_bombs:
            # Choose a random location in the board
            loc = random.randint(0, self.dim_size**2-1)

            # Identify the location as a row, col tuple
            row = loc // self.dim_size # division gets row
            col = loc % self.dim_size # mod gets col
            
            # Ignore if there's a bomb there already
            if board[row][col] == '*':
                continue

            # Plant the bomb
            board[row][col] = '*' 
            bombs_planted += 1
        
        return board

    # Helper function precomputes andassigns values to locations 
    # corresponding to bombs in proximity of each location
    def assign_values_to_board(self):

         # Assign values from 0-8 to each location
         # since there are max a total of 8 neighboring spaces
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                # If there's a bomb here, don't calculate anything
                if self.board[r][c] == '*':
                    continue

                # Identifies neighboring bombs of this location
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)
    
    # Helper function to determine neighboring bombs for this location
    def get_num_neighboring_bombs(self, row, col):

        # Keep track of bombs
        num_neighboring_bombs = 0

        # Sum up all bombs neighboring this location
        # Make sure to check bounds with min and max
        for r in range(max(0,row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size, (col-1)+1)):
                # Ignore location of interest
                if r == row and c == col:
                    continue
                
                # If there's a bomb, add it
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        
        return num_neighboring_bombs
    
    # Helper function to "dig" at that location. Returns True if success, or False
    # if there was a bomb at the location.
    def dig(self, row, col):

        # 3 Scenarios
        # Bomb is hit -> game over
        # Successful dig at a location with neighboring bombs
        # Successful dig at a location with no neighboring bombs -> dig neighbors

        self.dug.add((row, col)) # Keep track of digs

        #  Check if bomb or not. If not, determine return if neighboring bombs
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # No neighboring bombs (self.board[row][col] == 0) -> dig neighbors
        for r in range(max(0,row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size, (col-1)+1)):
                if (r,c) in self.dug:
                    continue # Ignore where we've dug already
                self.dig(r,c)
        
        # Return true, impossible to hit a bomb at this point.
        return True

    # Helper function that returns an object that when printed, shows the board
    def __str__(self):

        # Array to represent the board
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # Initialize string representation
        string_rep = ''

        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# Main/Game 
def play(dim_size=10, num_bombs=10):

    # 1) Create the board and plant bombs
    board = Board(dim_size, num_bombs)
    safe = True

    # 2) Optional: Show the user the board and ask where to plant the bombs
    # print(board.__str__())

    # Gameplay
    # 3a) If bomb, show game over
    # 3b) If not bomb, dig recursively until each square
    #       is at least next to a bomb
    # 4) Repeat 2 and 3 until there are no more places to dig -> Win

    # Show the board and ask the user for input until the game is over
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)

        # regex split is used to split the string by the regex
        # comma means detect commas, parentheses means eliminate any amount of spaces
        # match any part of the string that contains a comma
        # 0,0 or 0 or 0,     0
        user_input = re.split(',(\\s)*', input("Where would you like to dig?\nChoice: "))
        
        # take first and last value only
        row, col = int(user_input[0]), int(user_input[-1])

        # out of bounds
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again")
            continue
    
        # valid move, dig here
        safe = board.dig(row, col)

        if not safe:
            # dug a bomb 
            break # game over
        
    # 2 ways we could've ended the loop. Check for win or lose.
    if safe:
        print("Congratulations! You won!")
    else:
        print("Sorry. Game over!")
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

# Good practice
if __name__ == '__main__':
    play()
