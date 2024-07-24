# Importing pygame and sys libraries
import random
import pygame
import sys
import pygame.locals

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

board = [[0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7]# Initializing the game board as a 2D list with all cells empty


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


def main():
    global board
    scoreboard = [0,0] # score board to determine number of wins by each player

    for i in range(100): # Run the game 100 times
        board = [[0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7] # Reinitialize the board
        pygame.init()
        screen = pygame.display.set_mode((WIDTH * NUM_COLS, WIDTH * NUM_ROWS))
        pygame.display.set_caption("Connect Four")

        who = random.choice([1,2]) # randomly decides which player will start first
        game_over = False

        while any_columns_free():
            display_board(screen)
            num_keys = list(range(7)) # list of possible columns
            coli = random.choice(num_keys)  # randomly choose one of the columns

            if is_column_free(coli):
                rowi = drop_in_column(coli, who)

                if has_just_won(who, rowi, coli):
                    if who == 1: # checking who won and adding it to the score board
                        scoreboard[0] += 1
                    else:
                        scoreboard[1] += 1

                    pygame.quit()
                    break

                who = 3 - who
                #pygame.time.wait(500) to see how each game plays out


        pygame.quit()
    print(f"Red won {scoreboard[0]} times while Yellow wins {scoreboard[1]} times")
    sys.exit()


if __name__ == "__main__":
    main()


