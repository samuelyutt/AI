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

    def new_hint(self, position, hint, b):
        # around_unmarked = b.around_position(position)
        # m = len(around_unmarked) 
        # n = hint

        around_unmarked = b.around_unmarked_position(position)
        around_marked_mine = b.around_marked_mine_position(position)
        m = len(around_unmarked) 
        n = hint - len(around_marked_mine)
        
        if n == m:
            # Insert the m single-literal positive clauses to the KB
            for au in around_unmarked:
                new_clause = Clause( [Literal(au)] )
                self.add_clause_to_KB(new_clause)
        elif n == 0:
            # Insert the m single-literal negative clauses to the KB
            for au in around_unmarked:
                new_clause = Clause( [-Literal(au)] )
                self.add_clause_to_KB(new_clause)
        elif m > n > 0:
            # General cases
            # Generate CNF clauses and add them to the KB
            all_positive = list(itertools.combinations(around_unmarked, m-n+1))
            all_negative = list(itertools.combinations(around_unmarked, n+1))
            # print('new', position, hint, m, n)
            for comb in all_positive:
                literals = []
                for au in comb:
                    literals.append(Literal(au))
                new_clause = Clause(literals)
                self.add_clause_to_KB(new_clause)
                # print(new_clause)
            for comb in all_negative:
                literals = []
                for au in comb:
                    literals.append(-Literal(au))
                new_clause = Clause(literals)
                self.add_clause_to_KB(new_clause)
                # print(new_clause)
        else:
            # For debugging
            print('Something is wrong')
            print(position, hint, m, n, len(around_unmarked), len(around_marked_mine))

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
        # new_clause, co_literal_count = self.resolution(moved_clause, remain_clause)
        # changed = False
        # if co_literal_count:
        #     changed = True
        # if moved_clause.literals[0] in new_clause.literals:
        #     new_clause.literals.remove(moved_clause.literals[0])
        #     changed = True
        # if changed:
        #     self.remove_clause_from_KB(remain_clause)
        #     self.add_clause_to_KB(new_clause)

        reduntent_clause = None
        add_clause = None
        
        literal = moved_clause.literals[0]
        co_literal = -moved_clause.literals[0]

        if co_literal in remain_clause.literals:
            # print(1, moved_clause, remain_clause, co_literal)
            new_clause = copy.deepcopy(remain_clause)
            # self.remove_clause_from_KB(remain_clause)
            reduntent_clause = remain_clause
            new_clause.literals.remove(co_literal)
            # self.add_clause_to_KB(new_clause)
            add_clause = new_clause
            # print(1, moved_clause, remain_clause, co_literal)
        elif literal in remain_clause.literals:
            # self.remove_clause_from_KB(remain_clause)
            reduntent_clause = remain_clause
            # print(2, moved_clause, remain_clause)

        return reduntent_clause, add_clause



    def pairwise_matching(self, clause_a, clause_b):
        # Check for duplication or subsumption first
        # Keep only the more strict clause.
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
        while len(self.KB):
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
                    else:
                        return Action('mark_mine', clause.literals[0].position)

                    has_single_literal = True


            # for c0 in self.KB0:
            #     for c in self.KB:
            #         tmp_clause, co_literal_count = self.resolution(c, c0)
            #         if c.is_empty():
            #             self.remove_clause_from_KB(c)
            #             continue
            #         elif tmp_clause > c:
            #             self.remove_clause_from_KB(c)
            #             self.add_clause_to_KB(tmp_clause)
            #             continue

            if not has_single_literal:
                # Apply pairwise matching of the clauses in the KB
                # Only match clause pairs where one clause has only at most two literals  
                tmp_KB = list(self.KB)
                matching_clauses = []
                for c in self.KB:
                    if len(c.literals) <= 2:
                        matching_clauses.append(c)
                for comb in list(itertools.combinations(matching_clauses, 2)):
                    if comb[0] in self.KB and comb[1] in self.KB:
                        self.pairwise_matching(comb[0], comb[1])
                if tmp_KB == self.KB:
                    return Action('give_up')


        return Action('done')
                


        