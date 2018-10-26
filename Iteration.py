import Markov
import Dealer
import sys

class Dp_solver:
    def __init__(self, fcp):
        self.fcp = fcp
        self.to_solve_mdp = Markov.Markov(fcp)
        self.val_act_dict = {}

    def solve_state(self, rep_first, rep_second, dealer_fc, is_first):
        # handle non splittable dup aces
        if rep_first == rep_second and rep_first == 1 and not is_first:
            return max([self.solve_state(0, 2, dealer_fc, False), self.solve_state(0, 12, dealer_fc, False)])

        # dont want this in duplicate 
        if rep_first != rep_second:
            if (rep_first, rep_second, dealer_fc, is_first) in self.val_act_dict:
                return self.val_act_dict[(rep_first, rep_second, dealer_fc, is_first)][0]
        
        # but still want (11, 11, ., .)
        if rep_first == 11:
            if (rep_first, rep_second, dealer_fc, is_first) in self.val_act_dict:
                return self.val_act_dict[(rep_first, rep_second, dealer_fc, is_first)][0]
        
        state_got = self.to_solve_mdp.states[(rep_first, rep_second, dealer_fc, is_first)]
        H_value = 0.0
        S_value = 0.0
        P_except_same_value = 0.0
        P_same_count = 0.0
        P_value = 0.0
        D_value = 0.0

        # dont let impossible move be picked over negative possible ones
        H_possible = False
        S_possible = False
        P_possible = False
        D_possible = False

        for trans in state_got.transitions:
            if trans.action == 'H':
                H_possible = True
                H_value += trans.probability*self.solve_state(*trans.state_rep)
            elif trans.action == 'S':
                S_possible = True
                S_value += trans.probability*self.solve_state(*trans.state_rep)
            elif trans.action == 'P':
                P_possible = True
                if trans.state_rep[0] == trans.state_rep[1] and is_first == trans.state_rep[3]:
                    P_except_same_value += trans.probability
                else:
                    P_except_same_value += trans.probability*self.solve_state(*trans.state_rep)
            elif trans.action == 'D':
                D_possible = True
                D_value += 2*trans.probability*self.solve_state(*trans.state_rep)
        
        P_value = P_except_same_value/(1-P_same_count)

        max_from_list = []
        if H_possible:
            max_from_list.append(H_value)
        if S_possible:
            max_from_list.append(S_value)
        if D_possible:
            max_from_list.append(D_value)
        if P_possible:
            max_from_list.append(P_value)

        max_value = max(max_from_list)

        if max_value == D_value and D_possible:
            best_action = 'D'
        elif max_value == P_value and P_possible:
            best_action = 'P'
        elif max_value == H_value and H_possible:
            best_action = 'H'
        else:
            best_action = 'S'
        
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

        # Black Jacks
        for dfc in xrange(1, 11):
            self.val_act_dict[(11, 21, dfc, True)] = (Dealer.rewardPlayer(21, dfc, self.fcp, True), 'G')

        # Bust
        self.val_act_dict[(21, 0, 0, False)] = (-1.0, 'G')

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
                if dup == 1:
                # self.val_act_dict[(dup, dup, dfc, True)] = (0.0, 'N')
                    prev_val = 0.0
                    curr_val = 1.0
                    epsilon = 0.1
                    max_divergence = 15
                    # self.val_act_dict[(dup, dup, dfc, True)] = 
                    while not(-epsilon < (curr_val-prev_val) < epsilon):
                        prev_val = curr_val
                        curr_val = self.solve_state(dup, dup, dfc, True)
                        if (curr_val-prev_val > max_divergence):
                            break
                else:
                    curr_val = self.solve_state(dup, dup, dfc, True)
                
    
    def output_first_move_policy(self):
        output_file = open("policy.txt", 'w')
        
        # hard values
        for hard_value in xrange(5, 20):
            output_file.write(str(hard_value))
            output_file.write("\t")
            for dfc in xrange(2, 12):
                if dfc == 11:
                    dfc = 12
                output_file.write(self.val_act_dict[(0, hard_value, dfc%11, True)][1])
                if dfc != 12:
                    output_file.write(" ")
            output_file.write("\n")
        
        # soft values
        for soft_value in xrange(2, 10):
            output_file.write("A")
            output_file.write(str(soft_value))
            output_file.write("\t")
            for dfc in xrange(2, 12):
                if dfc == 11:
                    dfc = 12
                output_file.write(self.val_act_dict[(1, soft_value, dfc%11, True)][1])
                if dfc != 12:
                    output_file.write(" ")
            output_file.write("\n")

        for dup in xrange(2, 11):
            output_file.write(str(dup))
            output_file.write(str(dup))
            output_file.write("\t")
            for dfc in xrange(2, 12):
                if dfc == 11:
                    dfc = 12
                output_file.write(self.val_act_dict[(dup, dup, dfc%11, True)][1])
                if dfc != 12:
                    output_file.write(" ")
            output_file.write("\n")
        
        # dup aces
        output_file.write("A")
        output_file.write("A")
        output_file.write("\t")
        for dfc in xrange(2, 12):
            if dfc == 11:
                dfc = 12
            output_file.write(self.val_act_dict[(1, 1, dfc%11, True)][1])
            if dfc != 12:
                output_file.write(" ")

        

if __name__ == "__main__":
    mdp = Dp_solver(float(sys.argv[1]))
    # mdp = Dp_solver(4.0/13)
    mdp.solve_mdp()
    mdp.output_first_move_policy()
