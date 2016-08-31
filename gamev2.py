import random
import math
import copy

###USE [[0] * 4 for i in range(4)] FOR THE PROBLEM OF CHANGING MULTIPLE LISTS BLUEARRRRRR
def drawgrid(board, game_size):
	print("-" * ((4 * game_size) + 1))
	for i in range(game_size):
		print("|", end = "", flush=True)
		for j in range(game_size):
			print("" , board[i][j] , "|" , end="" , flush=True)
		print("")
		print("-" * ((4 * game_size) + 1))


#for x in range(game_size):
#        if board[x]
print()
	

def check_state(board, game_size):
	game_on = True
	computer_win = 0
	diagonalup = 0
	diagonaldown = 0
	for m in range(game_size):
		horizontal = (sum(board[m]))
		if horizontal == 0:
			computer_win = 1
			game_on = False
		elif horizontal == game_size*2:
			game_on = False
	for m in range(game_size):
		vertical = (sum(i[m] for i in board))
		if vertical == 0:
			computer_win = 1
			game_on = False
		elif vertical == game_size*2:
			game_on = False
			diagonal = 0
	for m in range(game_size):
		diagonalup += board[m][m]
	if diagonalup == 0:
		computer_win = 1
		game_on = False
	elif diagonalup == game_size*2:
		game_on = False
	for m in range(game_size):
		diagonaldown += board[m][game_size-1-m]
	if diagonaldown == 0:
		computer_win = 1
		game_on = False
	elif diagonaldown == game_size*2:
		game_on = False
	if 1 not in board:
		computer_win = 2
		game_on = False
	return game_on, computer_win
	
def build_tree(board, game_size):
	computer_value = 0 # TODO
	player_value = 2
	
	#dict as board- turns dict to board format to parse whether its won or not
	dict_as_board = [[[]*game_size]*game_size]
	for x,y in curr_state[0]:
		dict_as_board[y][x] = 0
	for x,y in curr_state[1]:
		dict_as_board[y][x] = 1
	for x,y in curr_state[2]:
		dict_as_board[y][x] = 2
		
	check_state(dict_as_board, )
	
	

	board_as_dict = {0:[], 1:[], 2:[]}
	links_dict = {}# shows the possible moves that can be made after this board.
	states_dict = {}# the dictionary for all of the actual boards stored in numbers(nodes)
	player_turn_to_move= {}
	state_index_counter = 0
	stack = []
	# make the initial state and add it to states_dict
	for y in range(game_size):
		for x in range(game_size):
			cell_value = board[y][x]
			board_as_dict[cell_value].append((x,y))#board_as_dict is now a dict with the positions of the boxes on the values that they have.
	states_dict[state_index_counter] = board_as_dict
	stack.append(state_index_counter)
	player_turn_to_move[state_index_counter] = computer_value
	links_dict[state_index_counter] = []

	state_index_counter += 1 # same as state_index_counter = state_index_counter + 1

	# build the tree from the initial state (i.e. populate links_dict and states_dict)
	while len(stack) > 0:
		state_index = stack.pop()
		curr_player = player_turn_to_move[state_index]
		curr_state = states_dict[state_index]
		for free_coordinate in curr_state[1]:
			new_state = copy.deepcopy(curr_state)
			#move free_coordinate from [1] to [curr_player]
			new_state[1].remove(free_coordinate)
			new_state[curr_player].append(free_coordinate)
			
			# link to parent
			links_dict[state_index].append(state_index_counter)
			
			# initalise all the data for the new state
			states_dict[state_index_counter] = new_state
			links_dict[state_index_counter] = []
			player_turn_to_move[state_index_counter] = 2 - curr_player
			
			# tidy up/preparefor next iteration of the 2 enclosing loops
			
			state_index_counter += 1
			

			stack.append(state_index_counter)
	return links_dict, states_dict, player_turn_to_move

		

def get_computer_move(board, game_size):
	#the players piece will always be two and the computer is 0
	computer_value = 0
	player_value = 2
	# DFS - build the tree
	links_dict, states_dict, player_turn_to_move = build_tree(board, game_size)
	print(links_dict)
	print(states_dict)
	print(player_turn_to_move)
	
	# 
	
	
			
def main():	
	game_on = True
	computer_win = 0
	#0 for computer 1 for player
	player_turn = int(input("Do you wanna go first? Type 1 for yes, 0 for no\n"))
	game_size = int(input("What is the size of the grid that you want to play on?\n"))
	board = []
	for x in range(game_size):
		board.append([1] * game_size)
	drawgrid(board, game_size)
	while game_on:
		if player_turn == 1:
			a, b = input("Your turn! Please type your position in this format x,y\n").replace(" ", "").split(",")
			x, y = int(a), int(b)
			board[game_size-y-1][x] = 2
			player_turn = 0
		elif player_turn == 0:
			correct_turn = 0
			print("My turn!")
			while correct_turn == 0:
				y = random.randint(0,2)
				x = random.randint(0,2)
				if board[game_size-y-1][x] == 1:
					board[game_size-y-1][x] = 0
					correct_turn = 1
			player_turn = 1
		drawgrid(board, game_size)
		game_on, computer_win = check_state(board, game_size)
		
	if computer_win == 1:
		print("I win!")
		get_computer_move(board, game_on, game_size)
	elif computer_win == 2:
		print("It's a draw!")
		get_computer_move(board, game_on, game_size)
	else:
		print("You win!")
		get_computer_move(board, game_on, game_size)

#main()			

