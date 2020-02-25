from hex_skeleton import HexBoard

import numpy as np

# global vars
_board_size: int = 11
_INF: float = 99999.0

# initialize board with size n
_board = HexBoard(_board_size)

def _update_board(board: HexBoard, l_move, is_max: bool) -> HexBoard:
    color = board.BLUE if is_max else board.RED
    board.place(l_move, color)
    return board

def dummy_eval() -> float:
    return np.random.randint(0, 10)
    
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

        ## IGNORE THE CODE BELOW, IT DOESN'T WORK PROPERLY AT THE MOMENT
        # begin reverse iteration step
        # this happens when we get to a border of the corresponding color (i.e. we connect the sides)
        # if board.border(color, u):
        #     S = []
        #     path_length = 0
        #     if prev[u] or u == source:
        #         while u:
        #             if not board.is_color(u, color):
        #                 path_length += 1
        #             S.insert(0, u)
        #             u = prev[u]
        #     print(f"S for color {color} IS: {S}")
        #     print(f"Path length when accounting for already marked hexagons: {path_length}")
        #     return path_length, S # You can also optionally return "S" if you also want to store the path
        # # end reverse iteration step

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



## YOU CAN UNCOMMENT THE CODE BELOW IF YOU WANT TO USE THE DEPRECATED REVERSE ITERATION CODE
# def smart_eval(board: HexBoard) -> float:
#     legals = board.get_move_list()
#     print(f"LEGAL MOVES: {legals}")
#     blue_path_length, path = simple_dijkstra(board, random.choice(legals), True)
#     red_path_length, path = simple_dijkstra(board, random.choice(legals), False)
#     score = blue_path_length - red_path_length
#     return float(score)


def minimax(board: HexBoard, depth: int, is_max: bool) -> float:

    if depth == 0 or board.is_game_over():
        # board.print() # For some reason it doesn't break the loop here
        return dijkstra_eval(board)

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


# Minimax Test Code
eval_score = minimax(_board, 4, True)
print(f"Eval score: {eval_score}")

# # Debug Code for eval
# hb = HexBoard(4)
# # hb.place((2,0), hb.RED)
# hb.place((1, 1), hb.BLUE)
# hb.place((2,1), hb.BLUE)
# hb.place((3, 1), hb.BLUE)
# hb.print()
# for i in range(_board_size):
#     path_lengths, path = simple_dijkstra(hb, (0, i), True) # use True for BLUE eval, False for RED eval
#     print(f"FOR 0,{i} : {path_lengths}")
# # print(path)

# eval_score = dijkstra_eval(hb) # always returns final eval score for BLUE
# print(eval_score)