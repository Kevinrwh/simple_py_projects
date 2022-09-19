import random
import re

# Board creation
class Board:
    def __init__(self, dim_size, num_bombs) -> None:
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Create the board

        # Initialize the set of locations unconvered
        # We'll save row, col tuples
        self.dug = set()

        # Helper function makes new board based on
        # dimensions and number of bombs
        # constructing the list or lists here (2D board)
        self.board = self.make_new_board() # plant bombs
        
        # Helper function assigns values to board
        self.assign_values_to_board()

    def make_new_board(self):

        # Creates a 2D board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # Plant bombs
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            # pick a random location - used as an ID
            loc = random.randint(0, self.dim_size**2-1)

            # get the row,col for location
            row = loc // self.dim_size # division gets row
            col = loc % self.dim_size # mod gets col
            
            # If we've alread planted a bomb there
            if board[row][col] == '*':
                continue

            board[row][col] = '*' # plant bomb
            bombs_planted += 1
        
        return board

    def assign_values_to_board(self):
        # Now that we have bombs planted. Assign 0-8 
        # to all empty spaces, representing how many
        # neighboring bombs there are. Precomputing
        # makes things faster. 

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if bomb, don't calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)
    
    def get_num_neighboring_bombs(self, row, col):
        # Iterate through neighboring positions and sum
        # number of bombs

        num_neighboring_bombs = 0

        # Sum up bombs of neighbors, make sure to check bounds
        for r in range(max(0,row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size, (col-1)+1)):
                if r == row and c == col:
                    # original location, don't check this
                    continue
                
                # Sum bombs
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        
        return num_neighboring_bombs
    
    def dig(self, row, col):
        # dig at the location
        # return True if successful dig, False if bomb dug

        # Scenarios
        # hit bomb -> game over
        # dig location with neighboring bombs
        # dig at  location with no neighboring bombs -> dig neighbors!

        self.dug.add((row, col)) # keep track of digs

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # self.board[row][col] == 0
        for r in range(max(0,row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size, (col-1)+1)):
                if (r,c) in self.dug:
                    continue # don't dig where you've already dug
                self.dig(r,c)
        
        # If our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
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

# Gameplay
def play(dim_size=10, num_bombs=10):
    # 1) Create the board and plant bombs
    board = Board(dim_size, num_bombs)
    safe = True

    # 2) Show the user the board and ask where to plant the bombs
    # print(board.__str__())

    # 3a) If bomb, show game over

    # 3b) If not bomb, dig recursively until each square
    #       is at least next to a bomb

    # 4) Repeat 2 and 3 until there are no more places to dig -> Win

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)

        # regex split is used to split the string by the regex
        # comma means detect commas, parentheses means eliminate any amount of spaces
        # match any part of the string that contains a comma
        # 0,0 or 0 or 0,     0
        user_input = re.split(',(\\s)*', input("Where would you like to dig?\nChoice: "))
        
        # take first and last value
        row, col = int(user_input[0]), int(user_input[-1])

        # out of bounds
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again")
            continue
    
        # valid move, dig
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
