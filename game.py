import random


def drawgrid(board, game_size):
	print("-"*((4*game_size)+1))
	for i in range(game_size):
		print("|", end="", flush=True)
		for j in range(game_size):
			print("",board[i][j] , "|", end="", flush=True)
		print("")
		print("-"*((4*game_size)+1))


#for x in range(game_size):
#        if board[x]
#	print()
	

def check_state(board, game_size):
	game_on=True
	computer_win=0
	d/iagonalup=0
	diagonaldown=0
	for m in range(game_size):
		horizontal=(sum(board[m]))
		if horizontal==0:
			computer_win=1
			game_on=False
		elif horizontal==game_size*2:
			game_on=False
	for m in range(game_size):
		vertical=(sum(i[m] for i in board))
		if vertical==0:
			computer_win=1
			game_on=False
		elif vertical==game_size*2:
			game_on=False
			diagonal = 0
	for m in range(game_size):
		diagonalup += board[m][m]
	if diagonalup==0:
		computer_win=1
		game_on=False
	elif diagonalup==game_size*2:
		game_on=False
	for m in range(game_size):
		diagonaldown+=board[m][game_size-1-m]
	if diagonaldown==0:
		computer_win=1
		game_on=False
	elif diagonaldown==game_size*2:
		game_on=False
	return game_on, computer_win
	
def get_computer_move(board):
	*
			
def main():	
	game_on=True
	computer_win=0
	#0 for computer 1 for player
	player_turn = int(input("Do you wanna go first? Type 1 for yes, 0 for no\n"))
	game_size = int(input("What is the size of the grid that you want to play on?\n"))
	board=[]
	for x in range(game_size):
		board.append([1] * game_size)
	drawgrid(board, game_size)
	while game_on:
		if player_turn == 1:
			a, b =input("Your turn! Please type your position in this format x,y\n").replace(" ", "").split(",")
			x, y=int(a), int(b)
			board[game_size-y-1][x]=2
			player_turn = 0
		elif player_turn == 0:
			correct_turn=0
			print("My turn!")
			while correct_turn==0:
				y=random.randint(0,2)
				x=random.randint(0,2)
				if board[game_size-y-1][x]==1:
					board[game_size-y-1][x]=0
					correct_turn=1
			player_turn = 1
		drawgrid(board, game_size)
		game_on, computer_win=check_state(board, game_size)
		
	if computer_win==1:
		print("I win!")
	else:
		print("You win!")

main()			

