import numpy 

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
    def __init__(self,asignaciones=None):
        if asignaciones:
            self.asignaciones = asignaciones
        else:
            self.asignaciones = {}
    
    def add_new_asignacion(self,fila,valor):
        self.asignaciones[fila] = valor

    def add_to_asignacion(self,fila,valor):
        self.asignaciones[fila] += valor

    def get_value(self,fila):
        return self.asignaciones[fila]

    def get_asignaciones(self):
        return self.asignaciones
    
    def get_variables(self):
        # Tomamos una fila cualquiera
        # Por ejemplo:
        # {("A",0),("B",0),("C",0)} obtenemos {"A","B","C"}
        random_asignacion = next(iter(self.asignaciones.keys()))
        variables = set()
        for ele in random_asignacion: #O(m)
            variables.add(ele[0]) 
        return variables

    def show_factor(self):
        print(self.asignaciones)

    def get_inverse(self):
        for key in self.asignaciones.keys():
            self.asignaciones[key] = 1 / self.asignaciones[key]

"""
Aplica la marginalización de una variable dada a un factor.
"""
def marginalize(factor,variable):
    variable_values = variable.get_values()                         #ejemplo: {("B",0),("B",1)}
    tau = Factor()
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

def factor_product(factor1,factor2, variables_list):
    # factores vacios, no se va a dar nunca pero por si acaso
    if not factor1.get_asignaciones():
        return factor2
    if not factor2.get_asignaciones():
        return factor1
    
    variables1 = factor1.get_variables()  
    variables2 = factor2.get_variables()
    common_variables = variables1.intersection(variables2)

    factor_product = Factor()

    # Caso sin variables comunes, complejidad O(k^n1 * k^n2) = O(k^(n1+n2)) pero al no haber variables comunes no hay +1 del algoritmo de fuerza bruta, va a tener 
    # lo mismo que la marginalización
    if not common_variables:
        for asignacion1 in factor1.get_asignaciones().keys():         
            for asignacion2 in factor2.get_asignaciones().keys():     
                new_asignacion = frozenset(asignacion1.union(asignacion2)) 
                new_value = factor1.get_value(asignacion1) * factor2.get_value(asignacion2) 
                factor_product.add_new_asignacion(new_asignacion,new_value) 
        return factor_product
    
    # Caso con variables comunes, complejidad O(k^(n1+n2-r)) donde r es el numero de variables comunes
    # creo primero el mapa de factor_product con las posibles asignaciones
    # no quiero doble bucle porque sería O(k^(n1+n2))
    all_variables_names = variables1.union(variables2)
    
    variable_map = {var.get_name(): var for var in variables_list}
    all_variables = [variable_map[name] for name in all_variables_names]

    cardinalities = {}
    for var in all_variables:
        cardinalities[var.get_name()] = var.get_cardinality()
    num_asignaciones = 1
    for card in cardinalities.values():
        num_asignaciones *= card
    for i in range(0,num_asignaciones):
        new_asignacion = set()
        div = num_asignaciones
        for var in all_variables:
            div = div // cardinalities[var.get_name()]
            index = (i // div) % cardinalities[var.get_name()]
            new_asignacion.add((var.get_name(), index))
        factor_product.add_new_asignacion(frozenset(new_asignacion), 0.0)

    # quiero llenar los valores del mapa de forma lineal O(k^(n1+n2-r))
    for asignacion in factor_product.get_asignaciones().keys(): 
        # divido la asignacion en dos partes, una para cada factor
        asignacion1 = frozenset()
        asignacion2 = frozenset()
        for ele in asignacion:
            if ele[0] in variables1:
                asignacion1 = asignacion1.union({ele})
            if ele[0] in variables2:
                asignacion2 = asignacion2.union({ele})
        value1 = factor1.get_value(asignacion1)
        value2 = factor2.get_value(asignacion2)
        new_value = value1 * value2
        factor_product.add_new_asignacion(asignacion, new_value)
    return factor_product

def get_factors_with_variable(factors,variable):
    sublist = [] # Factores que contienen la variable
    remaining = [] # Factores que no contienen la variable
    
    for factor in factors:
        if variable in factor.get_variables():
            sublist.append(factor)
        else:
            remaining.append(factor)
    return sublist, remaining
                                                                           
def inferencia_marginal(order,factors):
    list = factors
    for i in order:
        sublist, list = get_factors_with_variable(list,i.get_name())
        res = sublist[0]
        for j in range(1,len(sublist)):
            res = factor_product(res,sublist[j])
        tau = marginalize(res,i)
        list.append(tau)
    factor = list[0]
    for i in range(1, len(list)):
        factor = factor_product(factor, list[i])
    return factor

def inferencia_condicional(factors, numerator_order, denominator_order):
    numerator = inferencia_marginal(numerator_order, factors)
    denominator = inferencia_marginal(denominator_order, [numerator])
    denominator.get_inverse()
    return factor_product(numerator, denominator)


A = Variable("A",3)
B = Variable("B", 2)
C = Variable("C", 3)
D = Variable("D", 2)
E = Variable("E", 2)

asignaciones = {}
valores = [0.3, 0.1, 0.7, 0.2, 0.4, 0.2, 0.2, 0.3, 0.3, 0.7, 0.1, 0.5]
i = 0
for a in range(0,A.get_cardinality()):
    for d in range(0,D.get_cardinality()):
        for e in range(0,E.get_cardinality()):
            key = frozenset({(A.get_name(), a),(D.get_name(), d),(E.get_name(), e)})
            asignaciones[key] = valores[i]
            i += 1
phi1 = Factor(asignaciones)

asignaciones = {}
valores = [0.7, 0.4, 0.1, 0.3, 0.6, 0.9]
i = 0
for b in range(0,B.get_cardinality()):
    for a in range(0,A.get_cardinality()):
        key = frozenset({(B.get_name(), b),(A.get_name(), a)})
        asignaciones[key] = valores[i]
        i += 1
phi2 = Factor(asignaciones)

asignaciones = {}
valores = [0.6, 0.3, 0.3, 0.4, 0.1, 0.3]
i = 0
for c in range(0,C.get_cardinality()):
    for e in range(0,E.get_cardinality()):
        key = frozenset({(C.get_name(), c),(E.get_name(), e)})
        asignaciones[key] = valores[i]
        i += 1
phi3 = Factor(asignaciones)

asignaciones = {}
valores = [0.8, 0.2]
i = 0
for e in range(0,E.get_cardinality()):
    key = frozenset({(E.get_name(), e)})
    asignaciones[key] = valores[i]
    i += 1
phi4 = Factor(asignaciones)

asignaciones = {}
valores = [0.6, 0.4]
i = 0
for d in range(0,D.get_cardinality()):
    key = frozenset({(D.get_name(), d)})
    asignaciones[key] = valores[i]
    i += 1
phi5 = Factor(asignaciones)

list = [phi1, phi2, phi3, phi4, phi5]
num_order = [B, C, D]
den_order = [A]

factor_product(phi1, phi4, [A, E, D]).show_factor()
#inferencia_condicional(list, num_order, den_order).show_factor()
            
"""A = Variable("A",2)
B = Variable("B",2)
C = Variable("C",2)
valores = [0.01,0.02,0.06,0.08,0.03,0.06,0.12,0.16]
asignaciones = {}
i = 0
for a in range(0,A.get_cardinality()):
    for b in range(0,B.get_cardinality()):
        for c in range(0,C.get_cardinality()):
            key = frozenset({(A.get_name(), a),(B.get_name(), b),(C.get_name(), c)})
            asignaciones[key] = valores[i]
            i += 1

print("-------------------------------------")
print("Factor phi1:")
phi1 = Factor(asignaciones)
phi1.show_factor()
print("-------------------------------------")
print("Aplicamos marginalización sobre phi1:")
print(f"Variable a marginalizar: {B.get_name()}")
print("Factor tao1:")
tau1 = marginalize(phi1,B)
tau1.show_factor()
print("-------------------------------------")

A = Variable("A",2)
B = Variable("B",2)
C = Variable("C",2)
valores = [0.1,0.2,0.3,0.4]
asignaciones1 = {}
asignaciones2 = {}
i = 0
for a in range(0,A.get_cardinality()):
    for b in range(0,B.get_cardinality()):
        key = frozenset({(A.get_name(), a),(B.get_name(), b)})
        asignaciones1[key] = valores[i]
        i += 1
i = 0
for b in range(0,B.get_cardinality()):
    for c in range(0,C.get_cardinality()):
        key = frozenset({(B.get_name(), b),(C.get_name(), c)})
        asignaciones2[key] = valores[i]
        i += 1
print("Factor phi1:")
phi1 = Factor(asignaciones1)
phi1.show_factor()
print("Factor phi2:")
phi2 = Factor(asignaciones2)
phi2.show_factor()
print("Producto:")
factor_product(phi1,phi2).show_factor()"""


