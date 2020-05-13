import copy, itertools
from board import Board
from logic import Literal, Clause, CNF

class Agent():
    def __init__(self):
        self.KB0 = []
        self.KB = []

    def new_hint(self, position, hint, b):
        around_unmarked = b.around_unmarked_position(position)
        around_marked_mine = b.around_marked_mine_position(position)
        m = len(around_unmarked) 
        n = hint - len(around_marked_mine)
        if n == m:
            for au in around_unmarked:
                new_clause = Clause( [Literal(au)] )
                if new_clause not in self.KB:
                    self.KB.append(new_clause)
        elif n == 0:
            for au in around_unmarked:
                new_clause = Clause( [-Literal(au)] )
                if new_clause not in self.KB:
                    self.KB.append(new_clause)
        elif m > n > 0:
            all_positive = list(itertools.combinations(around_unmarked, m-n+1))
            all_negative = list(itertools.combinations(around_unmarked, n+1))
            # print(position)
            for comb in all_positive:
                literals = []
                for au in comb:
                    literals.append(Literal(au))
                new_clause = Clause(literals)
                if new_clause not in self.KB:
                    self.KB.append(new_clause)
                # print(new_clause)
            for comb in all_negative:
                literals = []
                for au in comb:
                    literals.append(-Literal(au))
                new_clause = Clause(literals)
                if new_clause not in self.KB:
                    self.KB.append(new_clause)
        else:
            print('Something is wrong')
            print(position, hint, m, n, len(around_unmarked), len(around_marked_mine))

    def matching(self, clause_a, clause_b):
        # Check for duplication or subsumption first
        # Keep only the more strict clause.
        if clause_a <= clause_b:
            try:
                self.KB.remove(clause_a)
            except:
                pass
        elif clause_a >= clause_b:
            try:
                self.KB.remove(clause_b)
            except:
                pass
        else:
            co_literal_count = 0
            new_clause = copy.deepcopy(clause_a)
            for l in clause_b.literals:
                co_literal = -l
                if co_literal in new_clause.literals:
                    new_clause.literals.remove(co_literal)
                    co_literal_count += 1
                elif l not in new_clause.literals:
                    new_clause.literals.append(l)

            if co_literal_count == 1:
                # Only one pair of complementary literals:
                try:
                    self.KB.remove(clause_a)
                    self.KB.remove(clause_b)
                except:
                    pass
                if new_clause not in self.KB:
                    self.KB.append(new_clause)
                    if len(new_clause.literals) == 1:
                        print(clause_a, clause_b, new_clause)
            else:
                # No or more than one pairs of complementary literals
                # Do nothing
                pass

    def take_action(self, b):
        while len(self.KB):
            for c in self.KB:
                if c.is_single_literal():
                    # Single-lateral clause in the KB
                    # Mark this cell as safe or mined
                    clause = c

                    # Move that clause to KB0
                    self.KB.remove(c)
                    self.KB0.append(clause)
                    
                    # Process the matching of that clause to all the remaining clauses in the KB
                    for remain_c in self.KB:
                        # print(remain_c, clause)
                        self.matching(remain_c, clause)

                    if clause.is_safe():
                        # This cell is safe
                        return clause.literals[0].position
                    else:
                        b.mark_mine(clause.literals[0].position)

                
            for comb in list(itertools.combinations(self.KB, 2)):
                if len(comb[0].literals) <= 2 and len(comb[1].literals) <= 2:
                    if comb[0] in self.KB and comb[1] in self.KB:
                        self.matching(comb[0], comb[1])
            # for c in self.KB:
            #     print(c)
            # for i in range(len(self.KB)):
            #     for j in range(i, len(self.KB)):
            #         print(i, j)
            #         if len(self.KB[i].literals) <= 2 and len(self.KB[j].literals) <= 2:
            #             self.matching(self.KB[i], self.KB[j])
            # print('Iter')
        print('I can only guess')
        return None
                


        