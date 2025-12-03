from itertools import product

class Formula:

    def __init__(self):
        pass
    def print(self):
        pass
    def to_string(self):
        pass
    def get_value(self):
        pass

class Proposition(Formula):

    def __init__(self,p1,value=None):
        self.p1 = p1
        self.value = value
        
    def print(self):
        print(self.p1)

    def to_string(self):
        return self.p1
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
    
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
    
    def get_value(self):
        return (self.p1.get_value() and self.p2.get_value())

class Or(Formula):

    def __init__(self,p1:Formula,p2:Formula):
        self.p1 = p1
        self.p2 = p2

    def print(self):
        print(f"({self.p1.to_string()} or {self.p2.to_string()})")
    
    def to_string(self):
        return f"({self.p1.to_string()} or {self.p2.to_string()})"
    
    def get_value(self):
        return (self.p1.get_value() or self.p2.get_value())

class Not(Formula):

    def __init__(self,p1:Formula):
        self.p1 = p1

    def print(self):
        print(f"(not {self.p1.to_string()})")
    
    def to_string(self):
        return f"not {self.p1.to_string()}"
    
    def get_value(self):
        return not self.p1.get_value()

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
    
    def get_value(self):
        return ((not self.p1.get_value()) or self.p2.get_value())



def chaining(BC):
    proposiciones = set()
    implicaciones = list()
    BCnew = list(BC)
    
    for formula in BC:
        if isinstance(formula,Impl):
            implicaciones.append(formula)
        else:
            proposiciones.add(formula.to_string())

    hay_nueva_proposicion = True

    while(hay_nueva_proposicion):
        hay_nueva_proposicion = False
        for i in range(0,len(implicaciones)):
            necesarias = evaluar_proposiciones(implicaciones[i].head())

            if(necesarias is not None and necesarias.issubset(proposiciones)):
                proposiciones.add(implicaciones[i].tail().to_string())
                hola = set()
                separar_and(implicaciones[i].tail(), hola)
                for prop in hola:
                    BCnew.append(prop)
                    proposiciones.add(prop.to_string())
                implicaciones.pop(i)                
                hay_nueva_proposicion = True
                break
    return BCnew
                

def separar_and(formula, proposiciones):
    if not isinstance(formula,And) and formula is not None:
        print("Adding proposition:", formula.to_string())
        proposiciones.add(formula)
    else:
        separar_and(formula.get_p1(), proposiciones)
        separar_and(formula.get_p2(), proposiciones)
        for prop in proposiciones:
            prop.print()
    

def evaluar_proposiciones(formula):
    if isinstance(formula,And):
        proposiciones_p1 = evaluar_proposiciones(formula.get_p1())
        proposiciones_p2 = evaluar_proposiciones(formula.get_p2())
        return proposiciones_p1.union(proposiciones_p2)
    else:
        return {formula.to_string()}
    
def es_completo(bc, variables):

    derivados_objetos = chaining(bc)

    proposiciones_derivadas = set()
    for f in derivados_objetos:
        if isinstance(f, Proposition):
            proposiciones_derivadas.add(f.to_string())
            
    print(f"Es cierto segun el encadenamiento: {proposiciones_derivadas}")

    # Obtenemos lo que es cierto, por defecto decimos que todo es cierto
    consecuencias_logicas = set(v.to_string() for v in variables)
    
    # Combinaciones de valores para las variables
    rangos = [range(2) for _ in variables]
    hay_modelos_validos = False
    
    for combinacion in product(*rangos):
        # Asignamos los valores a las variables
        for i, val in enumerate(combinacion):
            variables[i].set_value(bool(val))
            
        # Verificamos si la BC es verdadera bajo esta asignación (flitramos filas de la tabla)
        es_modelo_valido = True
        for formula in bc:
            if not formula.get_value():
                es_modelo_valido = False
                break
        
        # Si la BC es verdadera (es un modelo válido), miramos qué variables son verdaderas
        if es_modelo_valido:
            hay_modelos_validos = True
            vars_verdaderas_en_modelo = set()
            for v in variables:
                if v.get_value():
                    vars_verdaderas_en_modelo.add(v.to_string())
            
            # La intersección mantiene solo las variables que son TRUE en TODOS los modelos válidos encontrados hasta ahora
            consecuencias_logicas = consecuencias_logicas.intersection(vars_verdaderas_en_modelo)

    # aqui miramos si hay modelos validos, si no los hay la BC es mala, consideramos que es completo porque no deriva nada
    if not hay_modelos_validos:
        print("La base de conocimiento es contradictoria (siempre falsa).")
        return True

    print(f"La lógica dicta que es verdad: {consecuencias_logicas}")

    # Comparamos lo que es logicamente cierto con lo que derivamos
    faltantes = consecuencias_logicas - proposiciones_derivadas
    
    if len(faltantes) > 0:
        print(f"INCOMPLETO. El algoritmo no pudo derivar: {faltantes}")
        return False
    else:
        print("COMPLETO. El algoritmo derivó todas las consecuencias lógicas.")
        return True

A = Proposition("Llueve")
B = Proposition("Nieva")
C = Proposition("Mojado")

es_completo([Impl(Or(A,B),C), A],[A,B,C])

