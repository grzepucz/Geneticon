import math


def bohachevsky_formula(x1, x2):
    return (x1 ** 2) + (2 * (x2 ** 2)) - (0.3 * math.cos(3 * math.pi * x1)) - (0.4 * math.cos(4 * math.pi * x2))


def booth_formula(x1, x2):
    return (x1 + 2 * x2 - 7) ** 2 + (2 * x1 + x2 - 5) ** 2


def get_formula_by_name(name):
    if name == 'Bohachevsky':
        return bohachevsky_formula
    if name == 'Booth':
        return booth_formula
