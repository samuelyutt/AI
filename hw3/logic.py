class Literal():
    def __init__(self, positive, position):
        self.positive = positive
        self.position = position

    def __eq__(self, other):
        return self.positive == other.positive and self.position == other.position

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return ('' if self.positive else '-') + str(self.position)

class Clause():
    def __init__(self, literals):
        self.literals = literals

    def __eq__(self, other):
        if not len(self.literals) == len(other.literals):
            return False
        for l in self.literals:
            if l not in other.literals:
                return False
        return True

    def __gt__(self, other):
        # Return True when self is stricter than other
        if not len(self.literals) < len(other.literals):
            return False
        for l in self.literals:
            if l not in other.literals:
                return False
        return True

    def __ge__(self, other):
        if not len(self.literals) <= len(other.literals):
            return False
        for l in self.literals:
            if l not in other.literals:
                return False
        return True

    def __repr__(self):
        ret = ''
        for l in self.literals:
            ret += (' v ' + str(l)) if ret else str(l)
        return '(' + ret + ')'

class CNF():
    def __init__(self, clauses):
        self.clauses = clauses

    def __repr__(self):
        ret = ''
        for c in self.clauses:
            ret += (', \n    ' + str(c)) if ret else str(c)
        return ret

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    a = Literal(True, (5, 3))
    b = Literal(False, (2, 4))
    c = Literal(True, (6, 13))
    d = Literal(False, (2, 1))
    e = Literal(True, (7, 0))

    clause1 = Clause([a, b, c])
    clause2 = Clause([a, b, c, d])
    clause3 = Clause([a, b, c, d, e])

    cnf = CNF([clause1, clause2, clause3])

    print(clause1 < clause2)
    print(clause3 < clause1)
    print(clause1 < clause2)
    print(cnf)
