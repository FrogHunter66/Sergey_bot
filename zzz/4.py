from collections import deque

HORSE = "K"
KING = "G"

class ChessBoard:
    def __init__(self, n, board):
        self.n = n
        self.board = board

    def get_moves(self, row, col, current_figure):
        moves = []

        if current_figure == HORSE:
            # Список возможных ходов

            horse_moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]
            # Проверяем каждый ход, чтобы он не выходил за пределы
            for r, c in horse_moves:
                if 0 <= r < self.n and 0 <= c < self.n:
                    new_figure = self.board[r][c]
                    if new_figure == HORSE or new_figure == KING:
                        new_figure = new_figure
                    else:
                        new_figure = HORSE
                    moves.append((r, c, new_figure))

        elif current_figure == KING:
            # Список возможных ходов

            king_moves = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
                (row + 1, col + 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row - 1, col - 1)
            ]
            # Проверяем каждый ход, чтобы он не выходил за пределы
            for r, c in king_moves:
                if 0 <= r < self.n and 0 <= c < self.n:
                    new_figure = self.board[r][c]
                    if new_figure == HORSE or new_figure == KING:
                        new_figure = new_figure
                    else:
                        new_figure = KING
                    moves.append((r, c, new_figure))

        return moves


def bfs_min_moves(board, start, end):
    queue = deque()
    visited = set()
    start_row, start_col = start
    end_row, end_col = end
    queue.append((start_row, start_col, HORSE, 0))
    visited.add((start_row, start_col, HORSE))
    while queue:
        row, col, current_figure, moves = queue.popleft()
        if (row, col) == (end_row, end_col):
            return moves
        possible_moves = board.get_moves(row, col, current_figure)
        for new_row, new_col, new_figure in possible_moves:
            if (new_row, new_col, new_figure) not in visited:
                visited.add((new_row, new_col, new_figure))
                queue.append((new_row, new_col, new_figure, moves + 1))
    return -1


def find_index(board, symbol, n):
    for i in range(n):
        for j in range(n):
            if board[i][j] == symbol:
                return i, j
    return None

def game():
    n = int(input())
    board = []
    for _ in range(n):
        board.append(input().strip())
    start_r, start_c = map(str, find_index(board, "S", n))
    finish_r, finish_c = map(str, find_index(board, "F", n))
    chess_board = ChessBoard(n, board)
    result = bfs_min_moves(chess_board, (start_r, start_c), (finish_r, finish_c))
    print(result)


if __name__ == '__main__':
    game()
