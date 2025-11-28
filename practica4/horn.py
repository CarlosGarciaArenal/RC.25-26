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
    
    def get_p1(self):
        return self.p1
    
    def get_p2(self):
        return self.p2

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


##La idea que le dije a Alex, tener un conjunto de proposiciones e ir mirando las implicaciones. La cosa es si son varios ands de proposiciones
## que para eso esta la funcion auxiliar que te las devuelve en un set. Se podria usar tambien para si el tail son ands de proposiciones, pero no estoy seguro
## si estaria bien eso porque no seria una clausula de Horn. 
def chainingv2(BC):
    proposiciones = set()
    implicaciones = list()
    BCnew = list(BC)
    
    for formula in BC:
        if isinstance(formula,Proposition):
            proposiciones.add(formula.to_string())
        elif isinstance(formula,Impl):
            implicaciones.append(formula)

    hay_nueva_proposicion = True

    while(hay_nueva_proposicion):
        hay_nueva_proposicion = False
        for i in range(0,len(implicaciones)):

            necesarias = evaluar_proposiciones(implicaciones[i].head())

            if(necesarias is not None and necesarias.issubset(proposiciones)):
                nuevas = evaluar_proposiciones(implicaciones[i].tail())
                if (nuevas is None):
                    BCnew.append(implicaciones[i].tail())
                else:
                    for proposicion in nuevas:
                        BCnew.append(Proposition(proposicion))
                        proposiciones.add(proposicion)

                implicaciones.pop(i)
                hay_nueva_proposicion = True
                break

    return BCnew
                
            

def evaluar_proposiciones(formula):
    if isinstance(formula,Proposition):
        return {formula.to_string()}
    if isinstance(formula,And):
        proposiciones_p1 = evaluar_proposiciones(formula.get_p1())
        proposiciones_p2 = evaluar_proposiciones(formula.get_p2())
        if(proposiciones_p1 is not None and proposiciones_p2 is not None):
            return proposiciones_p1.union(proposiciones_p2)
        else:
            return None
    else:
        return None

                
