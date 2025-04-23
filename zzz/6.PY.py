from collections import deque

HORSE_MOVES = [
    (-2, -1), (-1, -2), (1, -2), (2, -1),
    (2, 1), (1, 2), (-1, 2), (-2, 1)
]
KING_MOVES = [
    (-1, -1), (0, -1), (1, -1), (1, 0),
    (1, 1), (0, 1), (-1, 1), (-1, 0)
]


def find_min_moves(n, board, start, end):
    queue = deque([(start, 'K')])
    visited = {
        'K': {start},
        'G': set()
    }
    dist = 0
    while queue:
        dist += 1
        for _ in range(len(queue)):
            (current_i, current_j), state = queue.popleft()

            moves = HORSE_MOVES if state == 'K' else KING_MOVES

            for di, dj in moves:
                i, j = current_i + di, current_j + dj

                if not (0 <= i < n and 0 <= j < n):
                    continue

                if (i, j) == end:
                    return dist

                new_state = state
                if board[i][j] == 'K':
                    new_state = 'K'
                elif board[i][j] == 'G':
                    new_state = 'G'

                if (i, j, new_state) in visited[new_state]:
                    continue

                queue.append(((i, j), new_state))
                visited[new_state].add((i, j))
    return -1


def main():
    n = int(input())
    board = []
    start = end = None
    for i in range(n):
        row = input().strip()
        board.append(row)
        if "S" in row:
            start = (i, row.index("S"))
        elif "F" in row:
            end = (i, row.index("F"))

    result = find_min_moves(n, board, start, end)
    print(result)


if __name__ == "__main__":
    main()
