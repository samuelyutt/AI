class Literal():
    def __init__(self, position, positive = True):
        self.positive = positive
        self.position = position

    def __neg__(self):
        return Literal(self.position, not self.positive)

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

    def __lt__(self, other):
        if not len(other.literals) < len(self.literals):
            return False
        for l in other.literals:
            if l not in self.literals:
                return False
        return True

    def __le__(self, other):
        if not len(other.literals) <= len(self.literals):
            return False
        for l in other.literals:
            if l not in self.literals:
                return False
        return True

    def __repr__(self):
        ret = ''
        for l in self.literals:
            ret += (' v ' + str(l)) if ret else str(l)
        return '(' + ret + ')'

    def is_empty(self):
        return len(self.literals) == 0

    def is_single_literal(self):
        if len(self.literals) == 1:
            return True
        return False

    def is_safe(self):
        if len(self.literals) == 1:
            return not self.literals[0].positive
        return False


if __name__ == '__main__':
    # Examples
    a = Literal((5, 3))
    b = -Literal((2, 4))
    c = Literal((6, 13))
    d = -Literal((2, 1))
    e = Literal((7, 0))

    clause1 = Clause([a, b, c])
    clause2 = Clause([a, b, c, d])
    clause3 = Clause([a, b, c, d, e])
    clause4 = Clause([a, b, c, d, e])

    print(clause1 < clause2)
    print(clause3 < clause1)
    print(clause1 < clause2)
    print(clause1 < clause4)
    print(clause1 > clause4)
