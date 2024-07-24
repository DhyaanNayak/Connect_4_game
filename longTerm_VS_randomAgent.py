# Importing necessary libraries
import pygame
import sys
import pygame.locals
import random
import copy
import math
import time
from statistics import mean
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


def is_column_free(board, coli):
	"""
	Function to check if a column is free for a move.

	Args:
		coli (int): The column index to check.

	Returns: True if the column is free, False otherwise.
	"""
	return board[0][coli] == 0



def drop_in_column(board, coli, who):
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
		if is_column_free(board, c):
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

def valid_loc(board):
	"""
		To calculate the available columns among which the agent can choose.

		Returns: List of available columns.
	"""
	valid = []
	for c in range(NUM_COLS):
		if is_column_free(board, c):
			valid.append(c)
	return valid


def checking_win(board, who):
	"""
		Determines if the placement of a specific game piece results in a winning move on the Connect 4 board.

		Args:
		board (2D list): list containing current state of the game board.
		who:  The player's number (1 or 2).

		Returns:True if the placement of the specified piece results in a winning move, False otherwise.
		"""
	# Check horizontal locations for win
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS):
			if board[r][c] == who and board[r][c+1] == who and board[r][c+2] == who and board[r][c+3] == who:
				return True

	# Check vertical locations for win
	for c in range(NUM_COLS):
		for r in range(NUM_ROWS-3):
			if board[r][c] == who and board[r+1][c] == who and board[r+2][c] == who and board[r+3][c] == who:
				return True

	# Check positively sloped diagonals
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS-3):
			if board[r][c] == who and board[r+1][c+1] == who and board[r+2][c+2] == who and board[r+3][c+3] == who:
				return True

	# Check negatively sloped diagonals
	for c in range(NUM_COLS-3):
		for r in range(3, NUM_ROWS):
			if board[r][c] == who and board[r-1][c+1] == who and board[r-2][c+2] == who and board[r-3][c+3] == who:
				return True


def terminal_node(board):
	"""
		Function to check if game is at its terminal node.

		Args:
			board (2D list): list containing current state of the game board.

		Returns: True if game state is a terminal node and False otherwise.
	"""
	if checking_win(board, 1) or checking_win(board, 2) or len(valid_loc(board))== 0:
		return True
	else:
		return False




def minimax(board, depth, alpha, beta, maximizingPlayer):
	"""
		Function to implement the minimax algorithm.

		Args:
			board (2D list): list containing current state of the game board.
			depth (int) : depth of the minimax search
			alpha (float) : alpha value for alpha-beta pruning
			beta (float) : beta value for alpha-beta pruning
		Returns: column number for the best outcome and score of the outcome.
	"""
	valid_locations = valid_loc(board)
	if depth == 0 or terminal_node(board):
		if terminal_node(board):
			if checking_win(board, 1):
				return (None, -1000000000)
			elif checking_win(board, 2):
				return (None, 1000000000)
			else:
				return (None, 0)
		else: # depth is 0
			return (None, score_pos(board, 2))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			temp_board = copy.deepcopy(board)
			row  = drop_in_column(temp_board, col, 2)
			new_score =  minimax(temp_board, depth - 1, alpha, beta, False)[1]
			if new_score> value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else:
		value = math.inf
		for col in valid_locations:
			temp_board = copy.deepcopy(board)
			row = drop_in_column(temp_board, col, 1)
			new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
			if new_score< value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value




# Main game loop
def main():
	global board
	scoreboard = [0, 0]  # score board to determine number of wins by each player
	longterm_time = []
	randomagent_time = []
	for i in range(20):  # Run the game 100 times
		board = [[0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7, [0] * 7]  # Reinitialize the board
		pygame.init()
		screen = pygame.display.set_mode((WIDTH * NUM_COLS, WIDTH * NUM_ROWS))
		pygame.display.set_caption("Connect Four")

		who = 1  # Player 1 starts
		game_over = False

		while any_columns_free(): # while loop keeps iterating till there are no free columns left on the board
			display_board(screen)

			for event in pygame.event.get():
				# Checking if the players wish to quit by pressing escape or the quit button
				if event.type == pygame.locals.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

			if who == 1:  # Random agent AI's turn
				start_time = time.perf_counter()
				num_keys = list(range(7))  # list of possible choices
				coli = random.choice(num_keys)  # Making random choice

				if is_column_free(board, coli):
					rowi = drop_in_column(board, coli, who)

					if has_just_won(who, rowi, coli):  # checking if the player won
						scoreboard[0] += 1
						pygame.quit()
						break
				end_time = time.perf_counter()
				randomagent_time.append(end_time - start_time)
			if who == 2: # Long term AI's turn
				start_time = time.perf_counter()
				(coli, minimaxscore) = minimax(board, 5, -math.inf, math.inf, True )
				if coli == None:
					coli = random.choice(valid_loc(board))

				if is_column_free(board, coli):
					rowi = drop_in_column(board, coli, who) # drops a player's piece into column 'coli' and returns row number of the dropped piece

					if has_just_won(who, rowi, coli): # checking if the player won
						scoreboard[1] += 1
						pygame.quit()
						break
				# End timer
				end_time = time.perf_counter()
				longterm_time.append(end_time - start_time)
			who = 3 - who

		pygame.quit() # quits the game
	print(f"random agent won {scoreboard[0]} times while long term agent won {scoreboard[1]} times")
	print(f"On average: \n Random agent took {mean(randomagent_time)} seconds \n Long term agent took {mean(longterm_time)} seconds")
	sys.exit()

if __name__ == "__main__":
	# If it is the main program, call the main() function to start the game
	main()
