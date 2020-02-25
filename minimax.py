from hex_skeleton import HexBoard
from graph import Graph

import numpy as np

# probably have to do this better later
from hexagon import Hexagon
# Remove when refactoring

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
    return np.random.randint(0, 10)

def dijkstra_eval(board: HexBoard, is_max: bool):
    # TODO finish implementing dijkstra in graph class
    color = board.BLUE if is_max else board.RED
    graph = Graph(board)
    from_hex = Hexagon((0,1), board)
    return graph.dijkstra(from_hex, is_max)

def minimax(board: HexBoard, depth: int, is_max: bool) -> float:

    if depth == 0 or board.is_game_over():
        # return dummy_eval()
        return dijkstra_eval(board, is_max)

    legals = board.get_move_list()
    if legals:

        if is_max:
            g: float = -_INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = max(g, minimax(updated_board, depth-1, not is_max))

        else:
            g: float = _INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = min(g, minimax(updated_board, depth-1, not is_max))

        return g


final = minimax(_board, 4, True)
print(final)
