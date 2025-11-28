class Proposition:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def set_value(self, value):
        if self.value != value: 
            self.value = value
            print(f"{self.name} = {self.value}")

    def get_value(self):
        return self.value
    
    def __eq__(self, other):
        return isinstance(other, Proposition) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

class Formula:
    def __eq__(self, other): raise NotImplementedError
    def __repr__(self): raise NotImplementedError

class Not(Formula):
    def __init__(self, operand):
        self.operand = operand
    
    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand
    
    def __hash__(self):
        return hash(("not", self.operand))

    def __repr__(self):
        return f"(¬{self.operand})"

class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, And) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(("and", self.left, self.right))

    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Or) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(("or", self.left, self.right))

    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class Implication(Formula):
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"({self.antecedent} => {self.consequent})"

def forward_chaining(knowledge_base):    
    known_facts = []
    
    for item in knowledge_base:
        if not isinstance(item, Implication):
            known_facts.append(item)
            if isinstance(item, Proposition):
                item.set_value(True)
            elif isinstance(item, Not) and isinstance(item.operand, Proposition):
                item.operand.set_value(False)

    new_inference = True
    while new_inference:
        new_inference = False 
        
        for rule in knowledge_base:
            if isinstance(rule, Implication):
                antecedente_en_bc = rule.antecedent in known_facts
                consecuente_ya_sabido = rule.consequent in known_facts
                
                if antecedente_en_bc and not consecuente_ya_sabido:
                    if isinstance(rule.consequent, Proposition):
                        rule.consequent.set_value(True)                    
                    knowledge_base.append(rule.consequent)
                    known_facts.append(rule.consequent)
                    
                    new_inference = True
                    
A = Proposition("A")
B = Proposition("B")
C = Proposition("C")
D = Proposition("D")
E = Proposition("E")
F = Proposition("F")
G = Proposition("G")
H = Proposition("H")
I = Proposition("I")

r1 = Implication(A, And(E, B))
r2 = Implication(And(E, B), A)
r3 = Implication(And(And(A, B), C), D)
r4 = Implication(And(And(A, D), E), G)
r5 = Implication(And (And(B, D), F), H)
r6 = Implication(And(And(C, D), G), I)


BC = [
    A, D,
    r1, r2,r3,r4,r5,r6  
]

print(f"Hechos iniciales en BC: {[x for x in BC if not isinstance(x, Implication)]}\n")
forward_chaining(BC)
print(f"Estado final:")
print(f"A: {A.get_value()}")
print(f"B: {B.get_value()}")
print(f"C: {C.get_value()}")
print(f"D: {D.get_value()}")
print(f"E: {E.get_value()}")
print(f"F: {F.get_value()}")
print(f"G: {G.get_value()}")
print(f"H: {H.get_value()}")
print(f"I: {I.get_value()}")

#base de conocimiento final
print(BC)