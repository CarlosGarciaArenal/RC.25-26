from itertools import product


"""
Clase Variable
name: string que indica el nombre de la variable, por ejemplo "A"
cardinality: entero que indica la cardinalidad de la variable.
values: retorna una lista de tuplas de las posibles combinaciones. Por ejemplo
        para cardinality = 3, retornará [("A",0),("A",1),("A",2)]
"""
class Variable:

    def __init__(self,name,cardinality):
        self.name = name
        self.cardinality = cardinality
        self.values = set()
        for i in range(0,cardinality):
            self.values.add((name,i))

    def get_name(self):
        return self.name

    def get_values(self):
        return self.values
    
    def get_cardinality(self):
        return self.cardinality
    

"""
Clase factor. Se emplea un mapa donde:
- Las llaves son conjuntos. Cada conjunto representa una asignación
  conjunta de variables, por ejemplo a0 b1 c0. Cada instancia
  queda representada como una tupla, por ejemplo ("A",0),("B",1),("C",0)
  Por lo tanto, una llave puede ser por ejemplo:
  frozenset({("A",0),("B",1),("C",0)}) representando a0 b1 c0.
- El valor es el valor flotante de la asignación. Por ejemplo 0.06.
"""



class Factor:
    """
    Crea un factor. Puede tener una asignación ya existente
    o comenzar vacío. También vamos a tener un set que simplemente
    contiene las variables que para la multiplicación será útil.
    """
    def __init__(self,asignaciones=None,variables=None):
        if asignaciones:
            self.asignaciones = asignaciones
        else:
            self.asignaciones = {}
        if variables:
            self.variables = variables
        else:
            self.variables = set()

    def add_new_asignacion(self,fila,valor):
        self.asignaciones[fila] = valor

    def add_to_asignacion(self,fila,valor):
        self.asignaciones[fila] += valor

    def get_value(self,fila):
        return self.asignaciones[fila]

    def get_asignaciones(self):
        return self.asignaciones
    
    def get_variables_name(self):
        return {var.get_name() for var in self.variables}

    def get_variables(self):
        return {var for var in self.variables}

    def show_factor(self):
        print(self.asignaciones)

    def get_inverse(self):
        for key in self.asignaciones.keys():
            self.asignaciones[key] = 1 / self.asignaciones[key]

    def filter_by_given_values(self, given_values):
        list = []
        for key in self.asignaciones.keys():
            if given_values.issubset(key):
                list.append((key, self.asignaciones[key]))
        return list

"""
Aplica la marginalización de una variable dada a un factor.
"""
def marginalize(factor,variable):
    variable_values = variable.get_values()                         #ejemplo: {("B",0),("B",1)}
    tau = Factor(None, factor.get_variables() - {variable})  #Creamos el nuevo factor sin la variable a marginalizar
    for asignacion in factor.get_asignaciones().keys():             #ejemplo: {("A",0),("B",0),("C",0)}
        new_asignacion = frozenset(asignacion - variable_values)    #ejemplo: {("A",0),("C",0)}
        # A partir de aqui comprobamos el mapa del nuevo factor. Si por ejemplo {("A",0),("C",0)}
        # no estaba, se anhade con el valor de {("A",0),("B",0),("C",0)}. Si ya existe {("A",0),("C",0)},
        # significa que ya se anhadió el valor de {("A",0),("B",0),("C",0)} previamente y el de ahora se trata de
        # una nueva asignación, por ejemplo {("A",0),("B",1),("C",0)}, por lo que sumamos el valor al ya existente.
        if new_asignacion not in tau.get_asignaciones():
            tau.add_new_asignacion(new_asignacion,factor.get_value(asignacion))
        else:
            tau.add_to_asignacion(new_asignacion,factor.get_value(asignacion))
    return tau
        # n = numero de filas.
        # m = numero de tuplas de cada fila. Si aumenta m, también aumenta n.
        # Tenemos el for de cada fila, O(n)
        # Por cada fila hay operaciones de mapas O(1) y la operacion
        # new_asignacion = frozenset(asignacion - variable_values).
        # Esta operación consiste en iterar sobre cada elemento en asignacion y comprobar
        # si está en variable_values. Si no está ahí, lo anhade y si sí está no lo anhade.
        # Supuestamente el comprobar si está en variable_values es O(1). Se itera sobre asignacion,
        # luego O(m*1) = O(m)
        # Complejidad O(n*m), pero a medida que crecen:
        # n = 8, m = 3
        # n = 15, m = 4
        # n = 31, m = 5
        # Además esto es asumiendo cardinalidad de 2, pero si aumenta la cardinalidad
        # se aumenta aun más n y mientras m sigue igual.
        # n >> m, se puede considerar lineal O(n)


def factor_product_itertools(factor1,factor2):
    variables_factor1 = factor1.get_variables() 
    variables_factor2 = factor2.get_variables()
    variables_finales = list(variables_factor1.union(variables_factor2))

    rangos = [range(var.get_cardinality()) for var in variables_finales]
    asignaciones_finales = []
    
    for combinacion in product(*rangos):  ## Este for es para sacar todas las asignaciones, saca todas las combinaciones de las cardinalidades
        asignacion = frozenset(
            (variables_finales[i].get_name(), combinacion[i]) for i in range(len(variables_finales))) ## Aqui se le asigna a cada variable su numero para la tupla
        asignaciones_finales.append(asignacion)

    resultado = Factor(None, variables_finales)
    variables_factor1 = factor1.get_variables_name()
    variables_factor2 = factor2.get_variables_name()
    for asignacion in asignaciones_finales:
        key_factor1 = []
        key_factor2 = []

        for tupla in asignacion:
            variable = tupla[0]
      
            if variable in variables_factor1:
                key_factor1.append(tupla)
             
            
            if variable in variables_factor2:
                key_factor2.append(tupla)
    
    
        key_factor1 = frozenset(set(key_factor1))
        key_factor2 = frozenset(set(key_factor2))

        if len(key_factor1) == 0 or len(key_factor2) == 0:
            continue

        valor_factor1 = factor1.get_value(key_factor1)
        valor_factor2 = factor2.get_value(key_factor2)

        resultado.add_new_asignacion(asignacion, valor_factor1 * valor_factor2)

    return resultado


def get_factors_with_variable(factors,variable):
    sublist = [] # Factores que contienen la variable
    remaining = [] # Factores que no contienen la variable
    
    for factor in factors:
        if variable in factor.get_variables_name():
            sublist.append(factor)
        else:
            remaining.append(factor)
    return sublist, remaining

def inferencia_marginal_itertools(order,factors):
    factor_list = factors
    for i in order:
        sublist, factor_list = get_factors_with_variable(factor_list,i.get_name())
        res = sublist[0]
        for j in range(1,len(sublist)):
            res = factor_product_itertools(res,sublist[j])
        tau = marginalize(res,i)
        factor_list.append(tau)
    factor = factor_list[0]
    for i in range(1, len(factor_list)):
        factor = factor_product_itertools(factor, factor_list[i])
    return factor


def inferencia_condicional_itertools(factors, numerator_order, denominator_order):
    numerator = inferencia_marginal_itertools(numerator_order, factors)
    denominator = inferencia_marginal_itertools(denominator_order, [numerator])
    denominator.get_inverse()
    return factor_product_itertools(numerator, denominator)


if __name__ == "__main__":
    A = Variable("A", 2)
    B = Variable("B", 3)
    C = Variable("C", 2)
    D = Variable("D", 3)
    E = Variable("E", 2)
    F = Variable("F", 3)

    asignaciones = {}
    valores = [0.6, 0.4]
    i = 0
    for a in range(0,A.get_cardinality()):
        key = frozenset({(A.get_name(), a)})
        asignaciones[key] = valores[i]
        i += 1
    phi1 = Factor(asignaciones, {A})

    asignaciones = {}
    valores = [0.4, 0.4, 0.2]
    i = 0
    for b in range(0,B.get_cardinality()):
        key = frozenset({(B.get_name(), b)})
        asignaciones[key] = valores[i]
        i += 1
    phi2 = Factor(asignaciones, {B})

    asignaciones = {}
    valores = [0.8, 0.6, 0.2, 0.4]
    i = 0
    for c in range(0,C.get_cardinality()):
        for a in range(0, A.get_cardinality()):
            key = frozenset({(C.get_name(), c), (A.get_name(), a)})
            asignaciones[key] = valores[i]
            i += 1
    phi3 = Factor(asignaciones, {A, C})

    asignaciones = {}
    valores = [0.6, 0.6, 0.4, 0.4, 0.4, 0.6]
    i = 0
    for e in range(0,E.get_cardinality()):
        for b in range(0, B.get_cardinality()):
            key = frozenset({(B.get_name(), b), (E.get_name(), e)})
            asignaciones[key] = valores[i]
            i += 1
    phi4 = Factor(asignaciones, {B, E})

    asignaciones = {}
    valores = [0.8, 0.7, 0.6, 0.7, 0.5, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.3, 0.1, 0.1, 0.2, 0.2, 0.3, 0.4]
    i = 0
    for d in range(0,D.get_cardinality()):
        for a in range(0, A.get_cardinality()):
            for b in range(0, B.get_cardinality()):
                key = frozenset({(A.get_name(), a), (B.get_name(), b), (D.get_name(), d)})
                asignaciones[key] = valores[i]
                i += 1
    phi5 = Factor(asignaciones, {A, B, D})

    asignaciones = {}
    valores = [0.6, 0.5, 0.4, 0.5, 0.3, 0.1, 0.2, 0.3, 0.3, 0.2, 0.3, 0.4, 0.2, 0.2, 0.3, 0.3, 0.4, 0.5]
    i = 0
    for f in range(0,F.get_cardinality()):
        for c in range(0, C.get_cardinality()):
            for d in range(0, D.get_cardinality()):
                key = frozenset({(F.get_name(), f), (C.get_name(), c), (D.get_name(), d)})
                asignaciones[key] = valores[i]
                i += 1
    phi5 = Factor(asignaciones, {C, D, F})

    factor_list = [phi1, phi2, phi3, phi4, phi5]
    num_order = [A,B]
    den_order = [E]

    print(inferencia_condicional_itertools(factor_list, num_order, den_order).filter_by_given_values(frozenset([("C", 1), ("D", 1), ("F", 1)])))
