def rotate_matrix_in_place(n, direction, matrix):
    operations = list()

    if direction == "L":
        for i in range(n // 2):
            for j in range(i, n - i - 1):
                operations.extend([
                    [[i, j], [j, n - i - 1]],
                    [(j, n - i - 1), (n - i - 1, n - j - 1)],
                    [(n - i - 1, n - j - 1), (n - j - 1, i)]
                ])


    elif direction == "R":
        for i in range(n // 2):
            for j in range(i, n - i - 1):
                operations.extend([
                    [[i, j], [n - j - 1, i]],
                    [(j, n - i - 1), (n - i - 1, n - j - 1)],
                    [(n - i - 1, n - j - 1), (n - j - 1, i)]
                ])
    return operations

def print_res(operations):
    print(len(operations))
    for op in operations:
        (x1, y1), (x2, y2) = op
        print(f"{x1} {y1} {x2} {y2}")


n, direction = input().split()
n = int(n)
matrix = [list(map(int, input().split())) for _ in range(n)]

print_res(rotate_matrix_in_place(n, direction, matrix))



