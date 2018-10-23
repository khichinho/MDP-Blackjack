# State and Transition class here.


class Transition:
    
    def init(self, probability, action, state_rep):
        # has params
        # probability: float
        # action: char
        # state_rep: three tuple of int

        self.probability = probability
        self.action = action
        self.state_rep = state_rep


    def make_transitions(self, rep_first, rep_second, dealers_first_car):
        # Consider all action possiblities
        
        # ACTION HIT

        # loop over all card possiblities
        for card_possiblity in xrange(1, 11):
            # hard values
            if rep_first == 0:
            
            # soft values, Ace + something
            else if rep_first == 1 & rep_second != 1:

            #duplicates
            else:



class State:
    def init(self, rep_first, rep_second, dealers_first_car):
        self.rep_first = rep_first
        self.rep_second = rep_second
        self.dealers_first_car = dealers_first_car
        # TODO: correct to make goal states bust and states after stop.
        # the states that inherent reward.
        self.transitions = make_transitions(rep_first, rep_second, dealers_first_car)

# initialize all states for the game here.
class Markov:
    def init():
