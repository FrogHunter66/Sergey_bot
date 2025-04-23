# def rotate_matrix(matrix, n):
#     rotated_matrix = [[0] * n for _ in range(n)]
#
#     for i in range(n):
#         for j in range(n):
#             rotated_matrix[j][n - 1 - i] = matrix[i][j]
#
#     return rotated_matrix
#
#
# n, m = map(int, input().split())
# matrix = [list(map(int, input().split())) for _ in range(n)]
#
# rotated_matrix = rotate_matrix(matrix, n)
#
# for row in rotated_matrix:
#     print(" ".join(map(str, row)))

s = 'asdfasdf\nasdfas'
s1 = '123'
l1 = list(map(str, s1.split("\n")))
print(int(l1))