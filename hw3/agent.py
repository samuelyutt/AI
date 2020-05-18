import time
import copy, itertools
from board import Action, Board
from logic import Literal, Clause

class Agent():
    def __init__(self):
        self.KB0 = []
        self.KB = []

    def add_clause_to_KB(self, new_clause):
        if not new_clause.is_empty():
            # Do resolution of the new clause with all the clauses in KB0
            for c in self.KB0:
                tmp_clause, co_literal_count = self.resolution(new_clause, c)
                if tmp_clause > new_clause:
                    new_clause = tmp_clause
            
            # Check for identication and subsumption with all the clauses in KB
            is_useable = not (new_clause.is_empty())
            reduntents = []
            for c in self.KB:
                if not is_useable:
                    break
                if new_clause <= c:
                    is_useable = False
                if new_clause > c:
                    reduntents.append(c)
            if is_useable:
                self.KB.append(new_clause)

            for r in reduntents:
                self.remove_clause_from_KB(r)

    def remove_clause_from_KB(self, clause):
        try:
            self.KB.remove(clause)
        except:
            pass

    def global_constraint(self, b):
        # print('Appling global constraint')
        unmarked, marked_mine = b.global_constraint_check()
        # if len(unmarked) > 10 or b.mines - len(marked_mine) > 5:
        #     print('Cannot apply global constraint')
        # else:
        self.gen_clause(unmarked, marked_mine, b.mines)

    def new_hint(self, position, hint, b):
        around_unmarked = b.around_unmarked_position(position)
        around_marked_mine = b.around_marked_mine_position(position)
        self.gen_clause(around_unmarked, around_marked_mine, hint)
        

    def gen_clause(self, unmarked, marked_mine, hint):
        m = len(unmarked) 
        n = hint - len(marked_mine)
        
        if n == m:
            # Insert the m single-literal positive clauses to the KB
            for au in unmarked:
                new_clause = Clause( [Literal(au)] )
                self.add_clause_to_KB(new_clause)
        elif n == 0:
            # Insert the m single-literal negative clauses to the KB
            for au in unmarked:
                new_clause = Clause( [-Literal(au)] )
                self.add_clause_to_KB(new_clause)
        elif m > n > 0:
            # General cases
            # Generate CNF clauses and add them to the KB
            all_positive = list(itertools.combinations(unmarked, m-n+1))
            all_negative = list(itertools.combinations(unmarked, n+1))

            for comb in all_positive:
                literals = []
                for au in comb:
                    literals.append(Literal(au))
                new_clause = Clause(literals)
                self.add_clause_to_KB(new_clause)

            for comb in all_negative:
                literals = []
                for au in comb:
                    literals.append(-Literal(au))
                new_clause = Clause(literals)
                self.add_clause_to_KB(new_clause)

        else:
            # For debugging
            # print('Something is wrong')
            # print(position, hint, m, n, len(unmarked), len(marked_mine))
            pass

    def resolution(self, clause_a, clause_b):
        co_literal_count = 0
        new_clause = Clause([])
        for l in clause_a.literals:
            literal = l
            new_clause.literals.append(literal)
        for l in clause_b.literals:
            literal = l
            co_literal = -l
            if co_literal in new_clause.literals:
                new_clause.literals.remove(co_literal)
                co_literal_count += 1
            elif literal not in new_clause.literals:
                new_clause.literals.append(literal)
        return new_clause, co_literal_count
    
    def remain_literals_matching(self, moved_clause, remain_clause):
        reduntent_clause = None
        add_clause = None
        
        literal = moved_clause.literals[0]
        co_literal = -moved_clause.literals[0]

        if co_literal in remain_clause.literals:
            new_clause = copy.deepcopy(remain_clause)
            reduntent_clause = remain_clause
            new_clause.literals.remove(co_literal)
            add_clause = new_clause
        elif literal in remain_clause.literals:
            reduntent_clause = remain_clause

        return reduntent_clause, add_clause

    def pairwise_matching(self, clause_a, clause_b):
        # Check for duplication or subsumption first
        # Keep only the more strict clause.
        if len(clause_a.literals) > 2 and len(clause_b.literals) > 2:
            return
        if not (clause_a in self.KB and clause_b in self.KB):
            return

        if clause_a <= clause_b:
            self.remove_clause_from_KB(clause_a)
            return
        elif clause_a >= clause_b:
            self.remove_clause_from_KB(clause_b)
            return
        
        # Do resolution
        new_clause, co_literal_count = self.resolution(clause_a, clause_b)

        if co_literal_count == 1:
            # Only one pair of complementary literals:
            self.remove_clause_from_KB(clause_a)
            self.remove_clause_from_KB(clause_b)
            self.add_clause_to_KB(new_clause)
        else:
            # No or more than one pairs of complementary literals
            # Do nothing
            pass

    def take_action(self, b):
        # Make a query
        no_action_count = 0
        
        while len(self.KB):
            if no_action_count == 3:
                return Action('give_up')
            has_single_literal = False
            
            for c in self.KB:
                if c.is_single_literal():
                    # Single-lateral clause in the KB
                    # Mark this cell as safe or mined
                    clause = c

                    # Move that clause to KB0
                    self.remove_clause_from_KB(clause)
                    self.KB0.append(clause)
                    
                    # Process the matching of that clause to all the remaining clauses in the KB
                    reduntents = []
                    adds = []
                    for remain_c in self.KB:
                        reduntent_clause, add_clause = self.remain_literals_matching(clause, remain_c)
                        if reduntent_clause:
                            reduntents.append(reduntent_clause)
                        if add_clause:
                            adds.append(add_clause)
                    for r in reduntents:
                        self.remove_clause_from_KB(r)
                    for a in adds:
                        self.add_clause_to_KB(a)


                    if clause.is_safe():
                        return Action('query', clause.literals[0].position)
                        no_action_count = 0
                    else:
                        return Action('mark_mine', clause.literals[0].position)
                        no_action_count = 0

                    has_single_literal = True

            if not has_single_literal:
                no_action_count += 1

                # tmp_KB = list(self.KB)

                # Apply pairwise matching of the clauses in the KB
                # Only match clause pairs where one clause has only at most two literals
                for comb in list(itertools.combinations(self.KB, 2)):
                    if comb[0] in self.KB and comb[1] in self.KB:
                        self.pairwise_matching(comb[0], comb[1])

                # if tmp_KB == self.KB:
                #     # self.global_constraint(b)
                #     if tmp_KB == self.KB:
                #         return Action('give_up')


            # if len(self.KB) == 0:
            #     unmarked, marked_mine = global_constraint_check
            #     if len(unmarked):
            #         self.global_constraint(b)

        return Action('done')
                


        