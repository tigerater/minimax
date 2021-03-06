import random
import math
import copy

COMPUTER_VARIABLE = 0
PLAYER_VARIABLE = 2
AMBIGUOUS = 1
INFINITE_VALUE = 100000000000000000000000000000000000000
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
#print()
	

def check_state(board, game_size):
	game_on = True
	computer_win = 0
	diagonalup = 0
	diagonaldown = 0
	string_board = str(board)
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
	if "1" not in string_board:
		computer_win = 2
		game_on = False
		print(board)
	return game_on, computer_win
	
def check_game_win_tree(new_state, game_size):
	computer_win = 2
	computer_has_won = -3
	computer_has_lost = 3
	rows_to_check=[0]*game_size
	columns_to_check=[0]*game_size
	diagonal_down_to_check_computer = 0
	diagonal_up_to_check_computer = 0
	diagonal_down_to_check_player = 0
	diagonal_up_to_check_player = 0
	for x,y in new_state[0]: #subtracts one from each row/column value per times a player or computer has moved there
		rows_to_check[y] -= 1
		columns_to_check[x] -= 1
	for x,y in new_state[2]:
		rows_to_check[y] += 1
		columns_to_check[x] += 1
	if computer_has_lost in rows_to_check:
		computer_win = PLAYER_VARIABLE+1
	if computer_has_won in rows_to_check:
		computer_win = COMPUTER_VARIABLE+1
	if computer_has_lost in columns_to_check:
		computer_win = PLAYER_VARIABLE+1
	if computer_has_won in columns_to_check:
		computer_win = COMPUTER_VARIABLE+1
		
	for x,y in new_state[0]:
		if x == y:
			diagonal_down_to_check_computer+=1
		if x == 2-y:
			diagonal_up_to_check_computer+=1
	for x,y in new_state[2]:
		if x == y:
			diagonal_down_to_check_player+=1
		if x == 2-y:
			diagonal_up_to_check_player+=1
			#######################################################
	if diagonal_down_to_check_computer == 3:
		computer_win = COMPUTER_VARIABLE+1
	if diagonal_up_to_check_computer == 3:
		computer_win = COMPUTER_VARIABLE+1
	if diagonal_down_to_check_player == 3:
		computer_win = PLAYER_VARIABLE+1
	if diagonal_up_to_check_player == 3:
		computer_win = PLAYER_VARIABLE+1
		
	return computer_win


def build_tree(board, game_size):
	computer_value = COMPUTER_VARIABLE # TODO
	player_value = PLAYER_VARIABLE
	

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
		computer_win_in_tree = check_game_win_tree(curr_state, game_size)
		if computer_win_in_tree == 3 or computer_win_in_tree == 1:
			continue
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
			
			stack.append(state_index_counter)
			
			state_index_counter += 1
			


	return links_dict, states_dict, player_turn_to_move

		
	
def postorder(links_dict, states_dict, player_turn_to_move, minimax_tree, current_node, game_size):
	for child in links_dict[current_node]:
		postorder(links_dict, states_dict, player_turn_to_move, minimax_tree, child, game_size)
	#append value of current node to the minimax tree
	if len(links_dict[current_node]) == 0:
		game_winning_state = check_game_win_tree(states_dict[current_node],game_size)
		minimax_tree[current_node] = 0
		if game_winning_state == PLAYER_VARIABLE+1:
			minimax_tree[current_node]+=1
		elif game_winning_state == COMPUTER_VARIABLE+1:
			minimax_tree[current_node]-=1
	else:
		if player_turn_to_move[current_node] == COMPUTER_VARIABLE:
			minimum_constituents = links_dict[current_node]
			group_of_children=[]
			for individual_child in minimum_constituents:
				group_of_children.append(minimax_tree[individual_child])
			minimax_tree[current_node] = min(group_of_children)
		else:
			maximum_constituents = links_dict[current_node]
			group_of_children = []
			for individual_child in maximum_constituents:
				group_of_children.append(minimax_tree[individual_child])
			minimax_tree[current_node] = max(group_of_children)
####values represent the worth to the player where positive is player win and negative is computer win

def get_computer_move(board, game_size):
	#the players piece will always be two and the computer is 0
	computer_value = 0
	player_value = 2
	# DFS - build the tree
	links_dict, states_dict, player_turn_to_move = build_tree(board, game_size)
	minimax_tree = get_values(links_dict, states_dict, player_turn_to_move, game_size)
	new_children = links_dict[0]
	smallest_child = INFINITE_VALUE
	smallest_child_value = INFINITE_VALUE
	for child in new_children:
		if minimax_tree[child]<=smallest_child_value:
			smallest_child = child
			smallest_child_value = minimax_tree[smallest_child]
	if smallest_child == INFINITE_VALUE:
		quit()
	new_board_in_states = states_dict[smallest_child]
	new_board = [[1,1,1],[1,1,1],[1,1,1]]
	for player in range(3):
		for x,y in new_board_in_states[player]:
			new_board[y][x] = player
	return new_board

	
	



def get_values(links_dict, states_dict, player_turn_to_move, game_size):
	current_node = 0
	minimax_tree = {}
	postorder(links_dict, states_dict, player_turn_to_move, minimax_tree, current_node, game_size)
	return minimax_tree
			
def main():	
	game_on = True
	computer_win = 0
	#0 for computer 1 for player 2 for actual computer ai
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
			player_turn = 2
		elif player_turn == 0:
			correct_turn = 0
			print("My turn!")
			while correct_turn == 0: #optimisation to randomise first move
				y = random.randint(0,2)
				x = random.randint(0,2)
				if board[game_size-y-1][x] == 1:
					board[game_size-y-1][x] = 0
					correct_turn = 1
			player_turn = 1
		elif player_turn == 2: #minimax here
			board = get_computer_move(board, game_size)
			player_turn = 1
		drawgrid(board, game_size)
		game_on, computer_win = check_state(board, game_size)

	if computer_win == COMPUTER_VARIABLE+1: #1
		print("I win!")
	elif computer_win == AMBIGUOUS+1: #2
		print("It's a draw!")
	elif computer_win ==PLAYER_VARIABLE+1: #3
		print("You win!")

main()			

