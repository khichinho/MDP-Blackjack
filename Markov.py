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

    @classmethod
    def make_transitions(self, rep_first, rep_second, dealers_first_card, is_first, fcp):
        # TODO: Assumed fcp is float
        trans_list_to_return = []
        # Consider all action possiblities
   
        # ACTION HIT

        # loop over all card possiblities
        for card_possiblity in xrange(1, 11):

            # HARD VALUES
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
           
            # SOFT VALUES, Ace + something(except ace)
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
                    # ace soft value states only go till 9
                    if rep_second+card_possiblity <= 9:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (1, rep_second+card_possiblity, dealers_first_card, False)))
                    else:
                        # consider ace as 1 not bust a rational player wouldn't bust hiimself. 
                        # picking 11 as ace value
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (0, rep_second+card_possiblity+1, dealers_first_card, False)))
                
                # face card
                else:
                    # ace soft value states only go till 9
                    if rep_second+card_possiblity <= 9:
                        trans_list_to_return.append(Transition(fcp, 'H', 
                        (1, rep_second+card_possiblity, dealers_first_card, False)))
                    else:
                        # consider ace as 1 not bust a rational player wouldn't bust hiimself. 
                        # picking 11 as ace value
                        trans_list_to_return.append(Transition(fcp, 'H', 
                        (0, rep_second+card_possiblity+1, dealers_first_card, False)))

            # DUPLICATES
            elif rep_first == rep_second & 1 <= rep_first < 10:
                if card_possiblity == 1:
                    # aces after any duplicates
                    trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                    (1, rep_second+rep_first, dealers_first_card, False)))
                
                elif 2 <= card_possiblity <= 9:
                    # its duplicate aces
                    if rep_first == 1:
                        trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                        (1, rep_second+card_possiblity, dealers_first_card, False)))
                    # any other duplicates
                    else:
                        if rep_first+rep_second+card_possiblity <= 21:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                            (0, rep_first+rep_second+card_possiblity, dealers_first_card, False)))
                        
                        #bust
                        else:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'H', 
                            (21, 0, 0, False)))
                
                # face card
                else:
                    if rep_first+rep_second+card_possiblity <= 21:
                        trans_list_to_return.append(Transition(fcp, 'H', 
                        (0, rep_first+rep_second+card_possiblity, dealers_first_card, False)))
                    
                    #bust
                    else:
                        trans_list_to_return.append(Transition(fcp, 'H', 
                        (21, 0, 0, False)))

        # ACTION STAND

        # when players stands, calculate the value of hand and chain to goal state 
        # probability = 1 no chances after stand.
        if rep_first == 1:
            # rational agent would want to bust itself and get highest value possible.
            if rep_second == 1:
                # option 1 consider both aces 1. value = 2
                # option 2 consider both 11. value = 22. bust
                # option 3 consider 1 and 11. value = 12. rational agent will choose higher for more chance of win
                trans_list_to_return.append(Transition(1, 'S', 
                (11, 12, dealers_first_card, False)))
            
            elif rep_second + 11 > 21:
                trans_list_to_return.append(Transition(1, 'S', 
                (11, rep_second+1, dealers_first_card, False)))
            
            # rep_sceond >= 1. case where ace+something ace being 11 bust already considered.
            # what is only left is ace = 11 doesn't bust
            else:
                trans_list_to_return.append(Transition(1, 'S', 
                (11, rep_second+11, dealers_first_card, False)))
            
        elif rep_first == 0:
            # busting should be handle in hit case. here rep_first+rep_second <= 21 always.
            trans_list_to_return.append(Transition(1, 'S', 
            (11, rep_first+rep_second, dealers_first_card, False)))

        # for duplicates basically.
        # could even write else here because other states will most probably not violate these condition. just a precaution
        elif 2 <= rep_first <= 10:
            if 2 <= rep_second <= 10:
                trans_list_to_return.append(Transition(1, 'S', 
                (11, rep_first+rep_second, dealers_first_card, False)))
                # no other case possible for this representation of states
        
        # ACTION SPLIT
        # here you can get twice the reward so 2 Transitions appended to list for every case

        # possible only in X, X, dealer_card, True state. don't need to check is first still.
        if is_first:
            # first splitable Ace duplicates
            if rep_first == 1:
                if rep_second == 1:
                    # generate cards that will come after split
                    for card_possiblity1 in xrange(1, 11):
                        for card_possiblity2 in xrange(1, 11):
                                # exception rule applies here.
                                # cant resplit, cant get blackjack on splits
                                # gets only 1 additional card
                                # can double down though. didn't find any rule against this. 

                            if card_possiblity1 == 1:
                                if card_possiblity2 == 1:
                                    # made to non first non splittable ace duplicates.
                                    temp_trans_var = Transition(((1-fcp)/9)**2, 'P', 
                                    (0, 12, dealers_first_card, False))
                                    # hand 1
                                    trans_list_to_return.append(temp_trans_var)
                                    # hand 2
                                    trans_list_to_return.append(temp_trans_var)

                                elif 2 <= card_possiblity2 <= 9:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (0, 12, dealers_first_card, False)))
                                    #  hand 2
                                    if card_possiblity2 + 11 > 21:
                                        trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                        (0, card_possiblity2+11, dealers_first_card, False)))

                                # face card
                                else:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (1, 1, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (1, card_possiblity2, dealers_first_card, False)))

                            elif 2 <= card_possiblity1 <= 9:
                                if card_possiblity2 == 1:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (1, card_possiblity1, dealers_first_card, False)))
                                    #  hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (1, 1, dealers_first_card, False)))

                                elif 2 <= card_possiblity2 <= 9:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (1, card_possiblity1, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (1, card_possiblity2, dealers_first_card, False)))
                                
                                else:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (1, card_possiblity1, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (0, 21, dealers_first_card, False)))

                            # card1 face card
                            else:
                                if card_possiblity2 == 1:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (0, 21, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (1, 1, dealers_first_card, False)))
                                    
                                elif 2 <= card_possiblity2 <= 9:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (0, 21, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)*fcp, 'P', 
                                    (1, card_possiblity2, dealers_first_card, False)))

                                else:
                                    # hand 1
                                    trans_list_to_return.append(Transition(fcp**2, 'P', 
                                    (0, 21, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(fcp**2, 'P', 
                                    (0, 21, dealers_first_card, False)))
                
            elif 2 <= rep_first <= 9:
                if 2 <= rep_second <= 9:
                    for card_possiblity1 in xrange(1, 11):
                        for card_possiblity2 in xrange(1, 11):
                            pc1 = (1-fcp)/9
                            pc2 = (1-fcp)/9
                            if card_possiblity1 == 10:
                                pc1 = fcp
                            if card_possiblity2 == 10:
                                pc2 = fcp
                            
                            # all these transitions have is_first true because double down allowed afer spliting.
                            if card_possiblity1 == 1:
                                if card_possiblity2 == 1:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (1, rep_first, dealers_first_card, True)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (1, rep_second, dealers_first_card, True)))

                                elif 2 <= card_possiblity2 <= 10:
                                    # hand 1
                                    trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                    (1, rep_first, dealers_first_card, True)))
                                    # hand 2
                                    # split possible
                                    if card_possiblity2 == rep_second:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_second, rep_second, dealers_first_card, True)))
                                    # hand 2 makes hard value
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_second+card_possiblity2, dealers_first_card, True)))
                            
                            if 2 <= card_possiblity1 <= 10:
                                if card_possiblity2 == 1:
                                    # hand 1
                                    if card_possiblity1 == rep_first:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_first, rep_first, dealers_first_card, True)))
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_first+card_possiblity1, dealers_first_card, True)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                    (1, rep_second, dealers_first_card, True)))

                                elif 2 <= card_possiblity2 <= 10:
                                    # hand 1
                                    if card_possiblity1 == rep_first:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_first, rep_first, dealers_first_card, True)))
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_first+card_possiblity1, dealers_first_card, True)))
                                    # hand 2
                                    # split possible
                                    if card_possiblity2 == rep_second:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_second, rep_second, dealers_first_card, True)))
                                    # hand 2 makes hard value
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_second+card_possiblity2, dealers_first_card, True)))

            elif rep_first == 10:
                if rep_second == 10:
                    for card_possiblity1 in xrange(1, 11):
                        for card_possiblity2 in xrange(1, 11):
                            pc1 = (1-fcp)/9
                            pc2 = (1-fcp)/9
                            if card_possiblity1 == 10:
                                pc1 = fcp
                            if card_possiblity2 == 10:
                                pc2 = fcp
                            
                            if card_possiblity1 == 1:
                                if card_possiblity2 == 1:
                                    # hand 1
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (11, 21, dealers_first_card, False)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(((1-fcp)/9)**2, 'P', 
                                    (11, 21, dealers_first_card, False)))

                                elif 2 <= card_possiblity2 <= 10:
                                    # hand 1
                                    trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                    (11, 21, dealers_first_card, False)))
                                    # hand 2
                                    # split possible
                                    if card_possiblity2 == rep_second:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_second, rep_second, dealers_first_card, True)))
                                    # hand 2 makes hard value
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_second+card_possiblity2, dealers_first_card, True)))
                            
                            if 2 <= card_possiblity1 <= 10:
                                if card_possiblity2 == 1:
                                    # hand 1
                                    if card_possiblity1 == rep_first:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_first, rep_first, dealers_first_card, True)))
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_first+card_possiblity1, dealers_first_card, True)))
                                    # hand 2
                                    trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                    (11, 21, dealers_first_card, False)))

                                elif 2 <= card_possiblity2 <= 10:
                                    # hand 1
                                    if card_possiblity1 == rep_first:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_first, rep_first, dealers_first_card, True)))
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_first+card_possiblity1, dealers_first_card, True)))
                                    # hand 2
                                    # split possible
                                    if card_possiblity2 == rep_second:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (rep_second, rep_second, dealers_first_card, True)))
                                    # hand 2 makes hard value
                                    else:
                                        trans_list_to_return.append(Transition(pc1*pc2, 'P', 
                                        (0, rep_second+card_possiblity2, dealers_first_card, True)))

        # ACTION DOUBLE DOWN

        # only possible on first move or after split
        if is_first:
            for card_possiblity in xrange(1, 11):

                # HARD VALUES
                if rep_first == 0:
                    # ace comes for a hand containing no ace previously
                    if card_possiblity == 1:
                        if rep_second + 11 <= 21:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second+11, dealers_first_card, False)))
                        elif rep_second + 1 <= 21:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second+1, dealers_first_card, False)))
                        else:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (21, 0, 0, False)))
                    # any non face non ace card
                    elif 2 <= card_possiblity <= 9:
                        if rep_second+card_possiblity > 21:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (21, 0, 0, False)))
                        else:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second+card_possiblity, dealers_first_card, False)))
                    # face card
                    else:
                        if rep_second+card_possiblity > 21:
                            trans_list_to_return.append(Transition(fcp, 'D', 
                            (21, 0, 0, False)))
                        else:
                            trans_list_to_return.append(Transition(fcp, 'D', 
                            (11, rep_second+card_possiblity, dealers_first_card, False)))
            
                # SOFT VALUES, Ace + something(except ace)
                elif rep_first == 1 & rep_second != 1:
                    
                    # ace comes for a hand containing exactly 1 ace previously
                    if card_possiblity == 1:
                        # consider that ace = 1.
                        if rep_second + 11 + 1 <= 21:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second + 12, dealers_first_card, False)))
                        elif rep_second + 1 + 1 <= 21:
                            # only rep_second is from 2 to 9 where rep_first is 1. 
                            # So this only handle rep_second == 9.
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second + 2, dealers_first_card, False)))
                        else:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (21, 0, 0, False)))
                    # any non face non ace card
                    elif 2 <= card_possiblity <= 9:
                        # ace soft value states only go till 9
                        if rep_second+card_possiblity+11 <= 21:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second+card_possiblity+11, dealers_first_card, False)))
                        elif rep_second+card_possiblity+1 <= 21:
                            # consider ace as 1 not bust a rational player wouldn't bust hiimself. 
                            # picking 11 as ace value
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (11, rep_second+card_possiblity+1, dealers_first_card, False)))
                        else:
                            trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                            (21, 0, 0, False)))
                    # face card
                    else:
                        if rep_second+card_possiblity+11 <= 21:
                            trans_list_to_return.append(Transition(fcp, 'D', 
                            (11, rep_second+card_possiblity+11, dealers_first_card, False)))
                        elif rep_second+card_possiblity+1 <= 21:
                            trans_list_to_return.append(Transition(fcp, 'D', 
                            (11, rep_second+card_possiblity+1, dealers_first_card, False)))
                        else:
                            trans_list_to_return.append(Transition(fcp, 'D', 
                            (21, 0, 0, False)))
                # DUPLICATES
                elif rep_first == rep_second & 1 <= rep_first < 10:
                    pc = (1-fcp)/9
                    if card_possiblity == 10:
                        pc = fcp
                    
                    if card_possiblity == 1:
                        # aces after any duplicates
                        if rep_first == 1:
                            if rep_second+11+1 <= 21:
                                trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                                (11, rep_second+11+1, dealers_first_card, False)))
                            elif rep_second+1+1 <= 21:
                                trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                                (11, rep_second+rep_first+1, dealers_first_card, False)))
                            else:
                                trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                                (21, 0, 0, False)))
                        else:
                            if rep_second+11+rep_first <= 21:
                                trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                                (11, rep_second+11+rep_first, dealers_first_card, False)))
                            elif rep_second+1+rep_first <= 21:
                                trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                                (11, rep_second+1+rep_first, dealers_first_card, False)))
                            else:
                                trans_list_to_return.append(Transition((1-fcp)/9, 'D', 
                                (21, 0, 0, False)))
                    elif 2 <= card_possiblity <= 10:
                        if rep_first == 1:
                            if rep_second+11+card_possiblity <= 21:
                                trans_list_to_return.append(Transition(pc, 'D', 
                                (11, rep_second+card_possiblity+11, dealers_first_card, False)))
                            elif rep_second+1+card_possiblity <= 21:
                                trans_list_to_return.append(Transition(pc, 'D', 
                                (11, rep_second+card_possiblity+1, dealers_first_card, False)))
                            else:
                                trans_list_to_return.append(Transition(pc, 'D', 
                                (21, 0, 0, False)))
                        else:
                            if rep_first+rep_second+card_possiblity <= 21:
                                trans_list_to_return.append(Transition(pc, 'H', 
                                (0, rep_first+rep_second+card_possiblity, dealers_first_card, False)))
                            else:
                                trans_list_to_return.append(Transition(pc, 'H', 
                                (21, 0, 0, False)))

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
        if (not(is_goal)):
            self.transitions = Transition.make_transitions(rep_first, rep_second, dealers_first_card, is_first, face_card_probability)

# initialize all states for the game here.
class Markov:
    def init(self, face_card_probability):
        # generate states
        # hard values first and non first
        self.states = {}
        for hard_value in xrange(2, 22):
            for dfc in xrange(11):
                self.states[(0, hard_value, dfc, True, False)] = State(0, hard_value, dfc, True, False, face_card_probability)
                self.states[(0, hard_value, dfc, False, False)] = State(0, hard_value, dfc, False, False, face_card_probability)
        
        # soft values
        for soft_value in xrange(2, 10):
            for dfc in xrange(11):
                self.states[(1, soft_value, dfc, True, False)] = State(1, soft_value, dfc, True, False, face_card_probability)
                self.states[(1, soft_value, dfc, False, False)] = State(1, soft_value, dfc, False, False, face_card_probability)
        
        # duplicates
        for dup in xrange(11):
            for dfc in xrange(11):
                self.states[(dup, dup, dfc, True, False)] = State(dup, dup, dfc, True, False, face_card_probability)

        # Goal states
        for player_hv in xrange(2, 22):
            for dfc in xrange(11):
                self.states[(11, player_hv, dfc, False, True)] = State(0, player_hv, dfc, False, True, face_card_probability)

        # Black Jack
        self.states[(11, 21, 0, False, True)] = State(11, 21, 0, False, True, face_card_probability)

        # Bust
        self.states[(21, 0, 0, False, True)] = State(21, 0, 0, False, True, face_card_probability)
     