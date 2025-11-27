from horn import *

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

    BC = [Impl(And(A,D),E),
          Impl(And(B,E),A),
          Impl((And(And(A,B),C)), D),
          Impl((And(And(A,D),E)), G),
          Impl((And(And(B,D),F)), H),
          Impl((And(And(C, E),G)), I),
          A, D
          ]
    
    stuff = chainingv2(BC)
    BC_original = set(BC)
    print("BC original:")
    for item in BC_original:
        item.print()
    BC_resultado = set(stuff) - BC_original
    print("Added:")
    for item in BC_resultado:
        item.print()