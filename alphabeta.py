from hex_skeleton import HexBoard

import numpy as np

# global vars
_board_size: int = 3
_INF: float = 99999.0

# initialize board with size n
_board = HexBoard(_board_size)


def _update_board(board: HexBoard, l_move, is_max: bool) -> HexBoard:
    color = board.BLUE if is_max else board.RED
    board.place(l_move, color)
    return board


def dummy_eval() -> float:
    return 5.0


def alphabeta(board: HexBoard, depth: int, alpha: float, beta: float, is_max: bool) -> float:
    if depth == 0 or board.is_game_over():
        return dummy_eval()

    legals = board.get_move_list()
    if legals:

        if is_max:
            g: float = -_INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = max(g, alphabeta(updated_board,
                                     depth-1, alpha, beta, not is_max))

                alpha = max(alpha, g)
                if beta <= alpha:
                    break

        else:
            g: float = _INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = min(g, alphabeta(updated_board,
                                     depth-1, alpha, beta, not is_max))

                beta = min(beta, g)
                if beta <= alpha:
                    break

        return g


final = alphabeta(board=_board, depth=4, alpha=1.0, beta=1.0, is_max=True)
print(final)
