game_on=True
#0 for computer 1 for player
player_turn = int(input("Do you wanna go first? Type 1 for yes, 0 for no\n"))
game_size=3

while game_on:
	if player_turn == 1:
		x, y =input("Your turn! Please type your position in this format x,y\n").replace(" ", "").split(",")
		print(x, y)
		player_turn = 0
	else:
		print("My turn!")
		player_turn = 1
