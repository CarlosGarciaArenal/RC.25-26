class Formula:

    def __init__(self):
        pass
    def print(self):
        pass
    def to_string(self):
        pass

class Proposition(Formula):

    def __init__(self,p1):
        self.p1 = p1
        
    def print(self):
        print(self.p1)

    def to_string(self):
        return self.p1
    
class And(Formula):

    def __init__(self,p1:Formula,p2:Formula):
        self.p1 = p1
        self.p2 = p2
    
    def print(self):
        print(f"({self.p1.to_string()} and {self.p2.to_string()})")
    
    def to_string(self):
        return f"({self.p1.to_string()} and {self.p2.to_string()})"

class Or(Formula):

    def __init__(self,p1:Formula,p2:Formula):
        self.p1 = p1
        self.p2 = p2

    def print(self):
        print(f"({self.p1.to_string()} or {self.p2.to_string()})")
    
    def to_string(self):
        return f"({self.p1.to_string()} or {self.p2.to_string()})"

class Not(Formula):

    def __init__(self,p1:Formula):
        self.p1 = p1

    def print(self):
        print(f"(not {self.p1.to_string()})")
    
    def to_string(self):
        return f"not {self.p1.to_string()}"

class Impl(Formula):

    def __init__(self,p1:Formula,p2:Formula):
        self.p1 = p1
        self.p2 = p2

    def print(self):
        print(f"({self.p1.to_string()} --> {self.p2.to_string()})")

    def to_string(self):
        return f"({self.p1.to_string()} --> {self.p2.to_string()})"
    
    def head(self):
        return self.p1

    def tail(self):
        return self.p2

def modus_ponens(rule,fact):
    if isinstance(rule,Impl) and rule.head().to_string() == fact.to_string():
        return rule.tail()


def chaining(BC):
    to_explore_formula1 = list(BC)
    BCnew = list(BC)

    while to_explore_formula1:
        formula1 = to_explore_formula1.pop()
        for formula2 in BCnew:
            item = modus_ponens(formula1,formula2)
            if item and item not in BCnew:
                BCnew.append(item)
                to_explore_formula1.append(item)

    return BCnew

