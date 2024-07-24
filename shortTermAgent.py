# Importing necessary libraries
import pygame
import sys
import pygame.locals
import random
import copy
import time

# Constants for the game board
NUM_COLS = 7  # Number of columns in the game board
NUM_ROWS = 6  # Number of rows in the game board
WIDTH = 50    # Width of each cell
# defining colour variables with RGB values
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
cols = [BLACK, RED, YELLOW]  # Colors for cells
names = ["black", "red", "yellow"]  # Names for colours defined in the list cols

# Initializing the game board as a 2D list with all cells empty
board = [[0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7]


def display_board(screen):
    """
    Function to display the game board on the screen.

    Args:
        screen (pygame.Surface): The screen to draw on.
    """
    screen.fill(BLUE)  # Fill the screen with blue background
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            location = ((c + 0.5) * WIDTH, (r + 0.5) * WIDTH)
            co = cols[board[r][c]]
            pygame.draw.circle(screen, co, location, 20)
    pygame.display.update()


def is_column_free(coli):
    """
    Function to check if a column is free for a move.

    Args:
        coli (int): The column index to check.

    Returns: True if the column is free, False otherwise.
    """
    return board[0][coli] == 0



def drop_in_column(coli, who):
    """
    Function to make a move by dropping a piece into a column.

    Args:
        coli (int): The column index to drop the piece into.
        who (int): The player making the move (1 or 2).

    Returns: The row index where the piece was dropped.
    """
    rowi = 0
    while ((rowi < NUM_ROWS - 1) and (board[rowi + 1][coli] == 0)):
        rowi += 1
    board[rowi][coli] = who
    return rowi



def any_columns_free():
    """
    Function to check if there are any columns left for a move. Used to check if the game can still continue.

    Returns: True if there are available columns, False if the board is full.
    """
    for c in range(NUM_COLS):
        if is_column_free(c):
            return True
    return False



def count_occs_from(who, rowi, coli, rowinc, colinc):
    """
    Function to count consecutive occurrences of a player's piece in a specific direction.
    Used to check if a player has achieved to get 4 pieces in a line

    Args:
        who (int): The player's number (1 or 2).
        rowi (int): The starting row index.
        coli (int): The starting column index.
        rowinc (int): The row increment (1, -1, or 0).
        colinc (int): The column increment (1, -1, or 0).

    Returns: The number of consecutive occurrences in the specified direction.
    """
    occs = 0
    rowi += rowinc
    coli += colinc

    while (rowi in range(0, NUM_ROWS) and coli in range(0, NUM_COLS) and board[rowi][coli] == who):
        occs += 1
        rowi += rowinc
        coli += colinc

    return occs


def has_just_won(who, rowi, coli):
    """
    Function to check if a player has just won the game by forming a winning sequence.

    Args:
        who (int): The player's number (1 or 2).
        rowi (int): The row index of the last move.
        coli (int): The column index of the last move.

    Returns: True if the player has won, False otherwise.
    """
    count = lambda rowinc, colinc: count_occs_from(who, rowi, coli, rowinc, colinc)
    return count(+1, -1) + count(-1, +1) >= 3 or \
           count(-1, +1) + count(+1, -1) >= 3 or \
           count(0, -1) + count(0, +1) >= 3 or \
           count(+1, 0) >= 3

def calculate_score(window, who):
	"""
		Function to calculate the score for a given window.

		Args:
			window (list): list of 4 consecutive slots in a particular orientation.
			who (int): The player's number (1 or 2).

		Returns: Score of the particular window.
	"""
	score = 0
	opp = 3 - who
	if window.count(who) == 4:
		score += 100
	elif window.count(who) == 3 and window.count(0) == 1:
		score += 10
	elif window.count(who) == 2 and window.count(0) == 2:
		score += 5
	if window.count(opp) == 3 and window.count(0) == 1:
		score -= 80
	return score

def score_pos(board, who):
    """
        Function to calculate the score for current board state.

        Args:
            board (2D list): list containing current state of the game board.
            who (int): The player's number (1 or 2).

        Returns: Score of the board at current state.
    """
    score = 0

    # Horizontal
    for r in range(NUM_ROWS):
        row_arr = [int(board[r][c]) for c in range(NUM_COLS)]   #[int(i) for i in list(board[r][:])]
        for c in range(NUM_COLS-3):
            window = row_arr[c:c+4]
            score += calculate_score(window, who)
    for c in range(NUM_COLS):
        col_arr = [int(board[r][c]) for r in range(NUM_ROWS)]  #[int(i) for i in list(board[:][c])]
        for r in range(NUM_ROWS-3):
            window = col_arr[r:r+4]
            score += calculate_score(window, who)
    for r in range(NUM_ROWS-3):
        for c in range(NUM_COLS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += calculate_score(window, who)
    for r in range(NUM_ROWS-3):
        for c in range(NUM_COLS-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += calculate_score(window, who)
    return score

def valid_loc():
    """
        To calculate the available columns among which the agent can choose.

        Returns: List of available columns.
    """
    valid = []
    for c in range(NUM_COLS):
        if is_column_free(c):
            valid.append(c)
    return valid

def best_move(who):
    """
        Function to calculate the best possible decision that can be made by the player(AI agent).

        Args:
            who (int): The player's number (1 or 2).

        Returns: column where player should put their piece.
    """
    valid = valid_loc()
    best_score = -10000
    best_col = random.choice(valid)
    for col in valid:
        tempboard = copy.deepcopy(board)
        rowi = 0
        while ((rowi < NUM_ROWS - 1) and (tempboard[rowi + 1][col] == 0)):
            rowi += 1
        tempboard[rowi][col] = who
        score = score_pos(tempboard, who)
        if col == 3: # preferring centre
            score += 6
        if score > best_score:
            best_score = score
            best_col = col
    return best_col



# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * NUM_COLS, WIDTH * NUM_ROWS))
    pygame.display.set_caption("Connect Four")

    who = 1  # Player 1 starts
    game_over = False

    while any_columns_free(): # while loop keeps iterating till there are no free columns left on the board
        display_board(screen)
        num_keys = list(range(pygame.K_1, pygame.K_8)) # list of possible choices


        for event in pygame.event.get():
            coli = -1
            # Checking if the players wish to quit by pressing escape or the quit button
            if event.type == pygame.locals.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Checking if players made a choice using number keys
            elif event.type == pygame.KEYDOWN and event.key in num_keys:
                coli = num_keys.index(event.key)
            # Checking if players made a choice using a mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coli = pygame.mouse.get_pos()[0] // WIDTH

            if coli != -1:
                if is_column_free(coli):
                    rowi = drop_in_column(coli, who) # drops a player's piece into column 'coli' and returns row number of the dropped piece

                    if has_just_won(who, rowi, coli): # checking if the player won
                        print(names[who], "has just won")
                        for i in range(NUM_ROWS):
                            print(board[i])
                        pygame.quit() # quits the game if a player wins
                        sys.exit()

                    who = 3 - who  # Switch between players 1 and 2
        if who == 2: # AI's turn
            # Start timer
            start_time = time.perf_counter()

            coli = best_move(who) # Calculate best move that the AI can make at the current state
            if coli != -1:
                if is_column_free(coli):
                    rowi = drop_in_column(coli, who) # drops a player's piece into column 'coli' and returns row number of the dropped piece

                    if has_just_won(who, rowi, coli): # checking if the player won
                        pygame.time.wait(500)
                        print(names[who], "has just won")
                        for i in range(NUM_ROWS):
                            print(board[i])
                        pygame.quit() # quits the game if a player wins
                        sys.exit()

                    who = 3 - who

                    # End timer
                    end_time = time.perf_counter()

                    # Calculate elapsed time
                    print("Time taken for move: ",end_time - start_time, "seconds")

    pygame.quit() # quits the game
    sys.exit()

if __name__ == "__main__":
    # If it is the main program, call the main() function to start the game
    main()
