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

    BC = [Impl(A,And(B,E)),Impl(And(B,E),A),
        Impl((And(And(A,B),C))D),Impl((And(And(A,D),E))G),
        ]
    stuff = chaining(BC)
    for item in stuff:
        item.print()