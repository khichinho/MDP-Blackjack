# Calculate win score of player. lose score of dealer using MDP like process.

# make a class here or whatever

# function for returning reward of player after stand state.
# called in Player Black Jack MDP

#TODO: Handle doubling on player side

#TODO: Input probability

reward_dict = {}

def rewardPlayer(player_hand_value, dealer_first_card, probability_face_card, is_blackjack):
	if(dealer_first_card == 1):
		return(reward_player_calculate(player_hand_value, True, 11, probability_face_card, is_blackjack, 1))
	else:
		return(reward_player_calculate(player_hand_value, False, dealer_first_card, probability_face_card, is_blackjack, 1))

#is_ace_card == True (if ace is treated as 11)
#else False
def reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value, probability_face_card, is_blackjack, num_cards):

	r = 0
	config_key = (player_hand_value, is_ace_card, dealer_hand_value, is_blackjack, num_cards)

	if config_key in reward_dict:
		return reward_dict[config_key]
	else:
		if(dealer_hand_value > 21):
			if(is_ace_card == True):
				return(reward_player_calculate(player_hand_value,False,dealer_hand_value-10, probability_face_card, is_blackjack, num_cards))
			else:
				r = tellReward(player_hand_value, is_ace_card, dealer_hand_value, is_blackjack, num_cards)
				reward_dict[config_key] = r
		elif(dealer_hand_value >= 17):
			r = tellReward(player_hand_value, is_ace_card, dealer_hand_value, is_blackjack, num_cards)
			reward_dict[config_key] = r
		else:
			for i in range(1,11):
				if(i == 10):
					r += probability_face_card * reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value+10, probability_face_card, is_blackjack, num_cards+1)
					reward_dict[config_key] = r
				elif(i == 1):
					r += ((1-probability_face_card)/9) * reward_player_calculate(player_hand_value, True, dealer_hand_value+11, probability_face_card, is_blackjack, num_cards+1)
					reward_dict[config_key] = r
				else:
					r += ((1-probability_face_card)/9) * reward_player_calculate(player_hand_value, is_ace_card, dealer_hand_value+i, probability_face_card, is_blackjack, num_cards+1)
					reward_dict[config_key] = r
		return(r)

def tellReward(player_hand_value, is_ace_card, dealer_hand_value, is_blackjack, num_cards):
	if(dealer_hand_value > 21):
		if(is_blackjack == True):
			return 1.5
		else:
			return 1
	elif(dealer_hand_value == 21):
		if(player_hand_value == 21):
			if(is_blackjack == True):
				if(is_ace_card == True and num_cards == 2):
					return 0
				else:
					return 1.5
			elif(is_blackjack == False):
				if(is_ace_card == True and num_cards == 2):
					return -1
				else:
					return 0
		else:
			return -1
	elif(dealer_hand_value < 21):
		if(player_hand_value == 21):
			if(is_blackjack == True):
				return 1.5
			else:
				return 1
		elif(player_hand_value > dealer_hand_value):
			return 1
		elif(player_hand_value == dealer_hand_value):
			return 0
		elif(player_hand_value < dealer_hand_value):
			return -1

if __name__ == "__main__":
	for i in range(2,22):
		print("\t")
		for j in range(1,11):
			print(str(i)+" "+str(j)+" "+str(rewardPlayer(i,j, 0.37, False)))
	
	print("\t")
	for j in range(1,11):
			print(str(21)+" "+str(j)+" "+str(rewardPlayer(21,j, 0.37, True)))