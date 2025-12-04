from practica4 import *

if __name__ == "__main__":

    phi = Proposition("p")
    kappa = Proposition("k")

    A = Proposition("A")
    B = Proposition("B")
    C = Proposition("C")
    D = Proposition("D")
    E = Proposition("E")
    F = Proposition("F")
    G = Proposition("G")
    H = Proposition("H")
    I = Proposition("I")

    BC = [Impl(And(A,C),E),
          Impl(B,C),
          Impl(And(D,B),F),
          Impl(C,D),
          B
          ]
    
    stuff = chaining(BC)
    BC_original = set(BC)
    print("-----------------------------")
    print("El otro ejemplo: BC original:")
    for item in BC_original:
        item.print()
    BC_resultado = set(stuff) - BC_original
    print("Added:")
    for item in BC_resultado:
        item.print()
    es_completo(BC,[A,B,C,D,E,F])