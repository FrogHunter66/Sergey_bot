# def x0(x, left, mid, right):
#     if x[0] == 1959:
#         return right
#     elif x[0] == 1990:
#         return mid
#     elif x[0] == 2006:
#         return left
#
#
# def x1(x, left, right):
#     if x[1] == 1991:
#         return right
#
#     elif x[1] == 1982:
#         return left
#
#
# def x2(x, left, right):
#     if x[2] == 'TEA':
#         return right
#     elif x[2] == 'JULIA':
#         return left
#
#
# def x3(x, left, right):
#     if x[3] == 1986:
#         return left
#
#     elif x[3] == 1995:
#         return right
#
#
# def x4(x, left, mid, right):
#     if x[4] == 'MIRAH':
#         return right
#     elif x[4] == 'JULIA':
#         return mid
#     elif x[4] == 'RUST':
#         return left
#
#
# def main(x):
#     return x3(x, x2(x, x0(x, 0, x1(x, 1, 2), 3), x4(x, x0(x, 4, 5, 6), x1(x, 7, 8), 9)), 10)


def main(x):
    t1 = int(x[0][1], 16)
    t2 = int(x[1][1], 16) << 6
    t3 = int(x[2][1], 16) << 11
    t4 = int(x[3][1], 16) << 19

    result = t1 | t2 | t3 | t4

    return result

print(main([("N1", 18), ('N2', 27), ("N3", 13), ("N4", 31)]))
# def maim(s):
#     st = int(s)
#     t1 = hex(st & 0b111111)
#     t2 = hex(st>>6 & 0b111111)
#     t3 = hex(st>>13 & 0b11)
#     t4 = hex(st>>16 & 0b11)
#     print(t1, t2, t3, t4)
#
# main([])