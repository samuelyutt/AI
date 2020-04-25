class Variable():
    def __init__(self, position):
        self.position = position
        
class Assigned_Variable(Variable):
    def __init__(self, position, assignment):
        super(Assigned_Variable, self).__init__(position)
        self.assignment = assignment

class Unassigned_Variable(Variable):
    def __init__(self, position, b, heuristic):
        super(Unassigned_Variable, self).__init__(position)
        self.domain = [0, 1]
        self.degree = -1

        # Initial value of degree if need
        if heuristic != '':
            current = b.current_board()        
            around = b.around_position(self.position)
            degree = 0
            for a in around:
                if heuristic == 'degree' and current[a[0]][a[1]] > -1:
                    degree += 1
                elif heuristic == 'space' and current[a[0]][a[1]] == -1:
                    degree += 1
            self.degree = degree


if __name__ == '__main__':
    pass
    
    
