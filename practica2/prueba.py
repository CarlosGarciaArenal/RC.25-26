import numpy 

class Variable:
    name = None
    cardinality = None
    values = None

    def __init__(self,name,cardinality):
        self.name = name
        self.cardinality = cardinality
        for i in range(0,cardinality):
            self.values.append((name,i))

    def get_name(self):
        return self.name

    def get_values(self):
        return self.values
    
    def get_cardinality(self):
        return self.cardinality


class Factor:
    values = {}
    variables = set()
    def __init__(self,values,variables):
        self.values = values
        self.variables = variables

    def get_variables(self):
        return self.variables

    def marginalize(self,variable):
        variable_values = variable.get_values()
        factor_variables = list(self.variables.keys())
        for i in range (0,length(factor_variables)):
            # Iterar por cada fila.
            # Si contiene (B,?) (cualquier cosa en ?, siempre eliminar
            # la que se quiere marginalizar). Añadir a un nuevo dict
            # con todas las variables menos la marginalizada. Si ya existe
            # esa llave ya se creó y hay que sumarle el valor. ej a0 b0 c0, a0 b1 c0.
            # Nueva llave a0 c0 dos ocurrencias a sumar.

        tau = Factor(PLACEHOLDER_VALUES,self.get_variables - {variable.get_name()}) 

phi1 = Factor({(set(("A",0),("B",0)),0.1),
        (set(("A",0),("B",1)),0.2),
        (set(("A",1),("B",0)),0.3),
        (set(("A",1),("B",1)),0.4)},
        set("A","B"))

phi1.marginalize(Variable("B",2))



