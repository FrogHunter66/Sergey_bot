def find_max_mushrooms(n, grid):
    current_dp = [0] * 3
    previous_dp = [0] * 3

    for col in range(3):
        if grid[-1][col] == "C":
            previous_dp[col] = 1

    for row in range(n - 2, -1, -1):
        for col in range(3):
            if grid[row][col] == "W":
                current_dp[col] = 0

            else:
                max_mushrooms_from_next_row = 0
                for neighbor_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if grid[row + 1][neighbor_col] != "W":
                        max_mushrooms_from_next_row = max(max_mushrooms_from_next_row, previous_dp[neighbor_col])

                current_dp[col] = max_mushrooms_from_next_row + (1 if grid[row][col] == "C" else 0)
        previous_dp, current_dp = current_dp, previous_dp

    return max(previous_dp)


def go_for_a_walk():
    n = int(input())
    grid = [input().strip() for _ in range(n)]
    max_mushrooms = find_max_mushrooms(n, grid)
    print(max_mushrooms)


if __name__ == "__main__":
    go_for_a_walk()