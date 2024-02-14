from math import log


def main(z, y, x):
    first_part = 98 * (36 * y - 42 * (x ** 2)) ** 2 - z ** 5 / 2
    second = (log(1 + 56 * x ** 2 + 82 * z ** 3, 10)) ** 7
    third = (log(z ** 2 + 68 * (y ** 3), 10)) ** 4
    return first_part + (second / 52 * (third - 41 * (abs(x)) ** 6)) ** 0.5


print(type(main(0.43, 0.01, 0.56)))