import Markov
import Dealer
import sys

class Dp_solver:
    def __init__(self, fcp):
        self.fcp = fcp
        self.to_solve_mdp = Markov.Markov(fcp)
        self.val_act_dict = {}

    def solve_state(self, rep_first, rep_second, dealer_fc, is_first):
        if (rep_first, rep_second, dealer_fc, is_first) in self.val_act_dict:
            return self.val_act_dict[(rep_first, rep_second, dealer_fc, is_first)][0]
        
        state_got = self.to_solve_mdp.states[(rep_first, rep_second, dealer_fc, is_first)]
        H_value = 0.0
        S_value = 0.0
        P_value = 0.0
        D_value = 0.0

        for trans in state_got.transitions:
            if trans.action == 'H':
                H_value += trans.probability*self.solve_state(*trans.state_rep)
            elif trans.action == 'S':
                S_value += trans.probability*self.solve_state(*trans.state_rep)
            elif trans.action == 'P':
                P_value += trans.probability*self.solve_state(*trans.state_rep)
            elif trans.action == 'D':
                D_value += 2*trans.probability*self.solve_state(*trans.state_rep)

        max_value = max([H_value, S_value, P_value, D_value])

        if max_value == H_value:
            best_action = 'H'
        elif max_value == S_value:
            best_action = 'S'
        elif max_value == P_value:
            best_action = 'P'
        else:
            best_action = 'D'
        
        # set in dict
        self.val_act_dict[(rep_first, rep_second, dealer_fc, is_first)] = (max_value, best_action)
        # return value
        return max_value

    def solve_mdp(self):
        # 'G' is action stating its absorbing goal state 
        # Stand Goal states
        for player_hv in xrange(2, 22):
            for dfc in xrange(1, 11):
                self.val_act_dict[(11, player_hv, dfc, False)] = (Dealer.rewardPlayer(player_hv, dfc, self.fcp, False), 'G')

        # Black Jack
        for dfc in xrange(1, 11):
            self.val_act_dict[(11, 21, dfc, True)] = (Dealer.rewardPlayer(21, dfc, self.fcp, True), 'G')

        # Bust
        self.val_act_dict[(21, 0, 0, False)] = -1.0

        # first hard values
        for hard_value in xrange(2, 22):
            for dfc in xrange(1, 11):
                # self.val_act_dict[(0, hard_value, dfc, True)] = 
                self.solve_state(0, hard_value, dfc, True)
        
        # first soft values
        for soft_value in xrange(2, 10):
            for dfc in xrange(1, 11):
                # self.val_act_dict[(1, soft_value, dfc, True)] = 
                self.solve_state(1, soft_value, dfc, True)
        
        # duplicates
        for dup in xrange(1, 11):
            for dfc in xrange(1, 11):
                self.val_act_dict[(dup, dup, dfc, True)] = 0.0
                prev_val = 0.0
                curr_val = 1.0
                epsilon = 0.001
                # self.val_act_dict[(dup, dup, dfc, True)] = 
                while not(-epsilon < (curr_val-prev_val) < epsilon):
                    prev_val = curr_val
                    curr_val = self.solve_state(dup, dup, dfc, True)
    
    def output_first_move_policy(self):
        pass

if __name__ == "__main__":
    mdp = Dp_solver(float(sys.argv[1]))
    mdp.output_first_move_policy()
