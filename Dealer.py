# Calculate win score of player. lose score of dealer using MDP like process.

# make a class here or whatever

# function for returning reward of player after stand state.
# called in Player Black Jack MDP


#TODO: Handle doubling on player side

#TODO: Input probability
p = 0.37

def rewardPlayer(player_hand_value, dealer_first_card):
	if(dealer_first_card == 1):
		return(reward_player_calculate(player_hand_value, 1, 11))
	else:
		return(reward_player_calculate(player_hand_value, 0, dealer_first_card))

#is_ace_card == 1 (if ace is treated as 11)
#else !1
def reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value):

	expected_reward = 0

	if(dealer_hand_value > 21):
		if(is_ace_card == 1):
			return(reward_player_calculate(player_hand_value,0,dealer_hand_value-10))
		else:
			return(tellReward(player_hand_value, dealer_hand_value))
	elif(dealer_hand_value >= 17):
		return(tellReward(player_hand_value, dealer_hand_value))
	else:
		for i in range(1,11):
			if(i == 10):
				expected_reward += p * reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value+10)
			elif(i == 1):
				expected_reward += ((1-p)/9) * reward_player_calculate(player_hand_value, 1, dealer_hand_value+11)
			else:
				expected_reward += ((1-p)/9) * reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value+i)
	return(expected_reward)

def tellReward(player_hand_value, dealer_hand_value):
	if(dealer_hand_value > 21):
		if(player_hand_value == 21):
			return 1.5
		elif(player_hand_value < 21):
			return 1
	elif(dealer_hand_value == 21):
		if(player_hand_value == 21):
			return 0
		elif(player_hand_value < 21):
			return -1
	elif(dealer_hand_value < 21):
		if(player_hand_value == 21):
			return 1.5
		elif(player_hand_value > dealer_hand_value):
			return 1
		elif(player_hand_value == dealer_hand_value):
			return 0
		elif(player_hand_value < dealer_hand_value):
			return -1

for i in range(2,22):
	for j in range(1,11):
		print(str(i)+" "+str(j)+" "+str(rewardPlayer(i,j)))