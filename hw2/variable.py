class Variable():
    def __init__(self, position):
        self.position = position
        
class Assigned_Variable(Variable):
    def __init__(self, position, assignment):
        super(Assigned_Variable, self).__init__(position)
        self.assignment = assignment

class Unassigned_Variable(Variable):
    def __init__(self, position):
        super(Unassigned_Variable, self).__init__(position)
        self.domain = [0, 1]


if __name__ == '__main__':
    pass
    
    
