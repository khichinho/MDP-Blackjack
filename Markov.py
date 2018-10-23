# State and Transition class here.


class Transition:

    def init(self, probability, action, state_rep):
        # has params
        # probability: float
        # action: char
        # state_rep: four tuple of 3 int and 1 bool

        self.probability = probability
        self.action = action
        self.state_rep = state_rep

    def make_transitions(self, rep_first, rep_second, dealers_first_card, fcp):
        # TODO: Assumed fcp is float
        trans_list_to_return = []
        # Consider all action possiblities
   
        # ACTION HIT

        # loop over all card possiblities
        for card_possiblity in xrange(1, 11):

            # hard values
            if rep_first == 0:
                # ace comes for a hand containing no ace previously
                if card_possiblity == 1:
                    if rep_second <= 9:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (1, rep_second, dealers_first_card, False)))
                    else:
                        # consider that ace = 1.
                        if rep_second <= 20:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                            (0, rep_second+1, dealers_first_card, False)))
                        else:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                            (21, 0, 0, False)))
                # any non face non ace card
                elif 2 <= card_possiblity <= 9:
                    if rep_second+card_possiblity > 21:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (21, 0, 0, False)))
                    else:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (0, rep_second+card_possiblity, dealers_first_card, False)))
                # face card
                else:
                    if rep_second+card_possiblity > 21:
                        trans_list_to_return.append(Transition(fcp, 'H', 
                        (21, 0, 0, False)))
                    else:
                        trans_list_to_return.append(Transition(fcp, 'H', 
                        (0, rep_second+card_possiblity, dealers_first_card, False)))
           
            # soft values, Ace + something
            elif rep_first == 1 & rep_second != 1:
                
                # ace comes for a hand containing exactly 1 ace previously
                if card_possiblity == 1:
                    # consider that ace = 1.
                    if rep_second <= 8:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (1, rep_second+1, dealers_first_card, False)))
                    else:
                        # only rep_second is from 2 to 9 where rep_first is 1. 
                        # So this only handle rep_second == 9.
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (11, 21, dealers_first_card, False)))
               
                # any non face non ace card
                elif 2 <= card_possiblity <= 9:
                    if rep_second+card_possiblity <= 9:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (1, rep_second+card_possiblity, dealers_first_card, False)))
                    else:
                        

            #duplicates
            else:



class State:
    def init(self, rep_first, rep_second, dealers_first_card, is_first, is_goal, face_card_probability):
        self.rep_first = rep_first
        self.rep_second = rep_second
        self.dealers_first_card = dealers_first_card

        self.is_first = is_first
        
        self.is_goal = is_goal
        # TODO: correct to make goal states bust and states after stop.
        # the states that inherent reward.
        self.transitions = []
        # absorbing goals can't get out of goal
        if !(is_goal):
            self.transitions = make_transitions(rep_first, rep_second, dealers_first_card, face_card_probability)

# initialize all states for the game here.
class Markov:
    def init(self, face_card_probability):
