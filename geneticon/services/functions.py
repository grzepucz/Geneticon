import math


def BohachevskyFormula(x1, x2):
    return (x1 ** 2) + (2 * (x2 ** 2)) - (0.3 * math.cos(3 * math.pi * x1)) - (0.4 * math.cos(4 * math.pi * x2))


def BoothFormula(x1, x2):
    return (x1 + 2 * x2 - 7) ** 2 + (2 * x1 + x2 - 5) ** 2
