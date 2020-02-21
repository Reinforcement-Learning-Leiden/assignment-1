from hex_skeleton import HexBoard

import numpy as np

# global vars
N: int = 3
INF: float = 99999.0

# initialize board with size n
board = HexBoard(N)


def _update_board(board: HexBoard, l_move, is_max: bool) -> HexBoard:
    color = board.BLUE if is_max else board.RED
    board.place(l_move, color)
    return board


def dummy_eval() -> float:
    return 5.0


def minimax(board: HexBoard, depth: int, is_max: bool) -> float:
    if depth == 0 or board.is_game_over():
        return dummy_eval()

    legals = board.get_move_list()
    if legals:

        if is_max:
            g: float = -INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = max(g, minimax(updated_board, depth-1, not is_max))

        else:
            g: float = INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = min(g, minimax(updated_board, depth-1, not is_max))

        return g


final = minimax(board, 4, True)
print(final)
