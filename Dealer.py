# Calculate win score of player. lose score of dealer using MDP like process.

# make a class here or whatever

# function for returning reward of player after stand state.
# called in Player Black Jack MDP

#TODO: Handle doubling on player side

#TODO: Input probability

reward_dict = {}

def rewardPlayer(player_hand_value, dealer_first_card, probability_face_card):
	if(dealer_first_card == 1):
		return(reward_player_calculate(player_hand_value, 1, 11, probability_face_card))
	else:
		return(reward_player_calculate(player_hand_value, 0, dealer_first_card, probability_face_card))

#is_ace_card == 1 (if ace is treated as 11)
#else !1
def reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value, probability_face_card):

	r = 0
	config_key = (player_hand_value, is_ace_card, dealer_hand_value)

	if config_key in reward_dict:
		return reward_dict[config_key]
	else:
		if(dealer_hand_value > 21):
			if(is_ace_card == 1):
				return(reward_player_calculate(player_hand_value,0,dealer_hand_value-10, probability_face_card))
			else:
				r = tellReward(player_hand_value, is_ace_card, dealer_hand_value)
				reward_dict[config_key] = r
		elif(dealer_hand_value >= 17):
			r = tellReward(player_hand_value, is_ace_card, dealer_hand_value)
			reward_dict[config_key] = r
		else:
			for i in range(1,11):
				if(i == 10):
					r += probability_face_card * reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value+10, probability_face_card)
					reward_dict[config_key] = r
				elif(i == 1):
					r += ((1-probability_face_card)/9) * reward_player_calculate(player_hand_value, 1, dealer_hand_value+11, probability_face_card)
					reward_dict[config_key] = r
				else:
					r += ((1-probability_face_card)/9) * reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value+i, probability_face_card)
					reward_dict[config_key] = r
		return(r)

def tellReward(player_hand_value, is_ace_card, dealer_hand_value):
	if(dealer_hand_value > 21):
		if(player_hand_value == 21):
			return 1.5
		elif(player_hand_value < 21):
			return 1
	elif(dealer_hand_value == 21):
		if(is_ace_card == 1):
			return -1
		else:
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
	print("\t")
	for j in range(1,11):
		print(str(i)+" "+str(j)+" "+str(rewardPlayer(i,j, 0.37)))