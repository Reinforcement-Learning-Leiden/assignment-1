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
    return np.random.randint(0, 10)
    
def simple_dijkstra(board: HexBoard, source, is_max):
    
    Q = set()
    V_set = board.get_all_vertices()
    dist = {}
    prev = {}
    for v in V_set:
        dist[v] = np.inf
        prev[v] = None
        Q.add(v)
    dist[source] = 0

    while len(Q) != 0:
        u = min(dist, key=dist.get)
        # print(f"U IS: {u}")
        Q.remove(u)

        neighbors = board.get_neighbors(u)
        color = board.BLUE if is_max else board.RED
        
        for v in neighbors:
            if v in Q: # Only check neighbours that are also in "Q"
                len_u_v = 1 if board.is_color(v, color) else 0 # this isn't working as intended i think...
                alt = dist[u] + len_u_v
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
        dist.pop(u) # This is to ensure that the keys in "dist" match the ones in "Q"
    
    return dist, prev

def minimax(board: HexBoard, depth: int, is_max: bool) -> float:

    if depth == 0 or board.is_game_over():
        # return dummy_eval()
        # return dijkstra_eval(board, is_max)
        return simple_dijkstra(board, (0, 1), is_max)

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


# final = minimax(_board, 4, True)
# print(final)

hb = HexBoard(3)
hb.place((1,1), hb.BLUE)
hb.print()

dist, prev = simple_dijkstra(hb, (1,1), False)
print(dist)

