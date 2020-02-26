from hex_skeleton import HexBoard
import copy

import numpy as np

# global vars
_board_size: int = 6
_INF: float = 99999.0

# initialize board with size n
_board = HexBoard(_board_size)

# NOTE: THE AI SHOULD START WITH A RANDOM MOVE, OR MAYBE JUST A SET MOVE

def simple_dijkstra(board: HexBoard, source, is_max):
    
    Q = set()
    V_set = board.get_all_vertices()
    dist = {}
    dist_clone = {} # I made a clone of dist to retain the information in dist
    prev = {}
    for v in V_set:
        dist[v] = np.inf
        dist_clone[v] = np.inf # clone
        prev[v] = None
        Q.add(v)
    dist[source] = 0
    dist_clone[source] = dist[source] # clone

    while len(Q) != 0:
        u = min(dist, key=dist.get)
        Q.remove(u)

        color = board.BLUE if is_max else board.RED

        neighbors = board.get_neighbors(u)

        for v in neighbors:
            if v in Q: # Only check neighbours that are also in "Q"
                len_u_v = 0 if board.is_color(v, color) else 1 # this isn't working as intended i think...
                alt = dist[u] + len_u_v
                if alt < dist[v]:
                    dist[v] = alt
                    dist_clone[v] = dist[v]
                    prev[v] = u
        # We pop "u" from the distance dict to ensure that the keys match the ones in "Q"
        dist.pop(u) # This is also why we need the clone, or else we'll return an empty dict
    
    return dist_clone, prev

def get_shortest_path(board: HexBoard, distances, color):
    """Gets the shortest path to a border and returns the length as score"""
    borders = board.get_borders(color)
    # print(f"ALL BORDERS: {borders}")
    shortest = np.inf
    for border in borders:
        # print(f"Dist for current border {border} is: {distances[border]}")
        if distances[border] < shortest:
            shortest = distances[border]
        # print(f"Current shortest: {shortest}")
    return shortest

def dijkstra_eval(board: HexBoard):
    """
    Checks the best path from every possible source (e.g. L to R for blue) and
    then returns the best evaluation score of the board based on the most
    efficient source
    """
    best_eval_score = -np.inf
    for i in range(board.get_board_size()):
        blue_source = (0, i)
        red_source = (i, 0)
        blue_dists, _ = simple_dijkstra(board, blue_source, True)
        red_dists, _ = simple_dijkstra(board, red_source, False)

        blue_score = get_shortest_path(board, blue_dists, board.BLUE)
        red_score = get_shortest_path(board, red_dists, board.RED)

        eval_score = red_score - blue_score

        if eval_score > best_eval_score:
            best_eval_score = eval_score

    return best_eval_score

def _update_board(board: HexBoard, l_move, is_max: bool) -> HexBoard:
    board = copy.deepcopy(board) # I think this was the problem with the minimax core, it was using a reference instead of a deep copy
    color = board.BLUE if is_max else board.RED
    board.place(l_move, color)
    return board


def dummy_eval() -> float:
    return 5.0


def alphabeta(board: HexBoard, depth: int, alpha: float, beta: float, is_max: bool) -> float:
    board.print()
    if depth == 0 or board.is_game_over():
        # board.print()
        return dijkstra_eval(board)

    legals = board.get_move_list()
    if legals:

        if is_max:
            g: float = -_INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = max(g, alphabeta(updated_board,
                                     depth-1, alpha, beta, is_max=False))

                alpha = max(alpha, g)
                if beta <= alpha:
                    break

        else:
            g: float = _INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = min(g, alphabeta(updated_board,
                                     depth-1, alpha, beta, is_max=True))

                beta = min(beta, g)
                if beta <= alpha:
                    break

        return g
    
    else:
        return dijkstra_eval(board)

## UNCOMMENT BELOW IF YOU WANT TO START THE GAME IN A FIXED STATE
# _board.place((1,1), _board.BLUE)
# _board.place((0,1), _board.RED)

eval_score = alphabeta(board=_board, depth=3, alpha=-np.inf, beta=np.inf, is_max=True)
print(eval_score)
