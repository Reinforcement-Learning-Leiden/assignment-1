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

        color = board.BLUE if is_max else board.RED
        # begin reverse iteration step
        # this only happens IF we get to the target hexagon which is a border of the corresponding color
        if board.border(color, u):
            S = []
            if prev[u] or u == source:
                while u:
                    S.insert(0, u)
                    u = prev[u]
            print(f"S IS: {S}")
            return float(len(S))
        # end reverse iteration step

        neighbors = board.get_neighbors(u)

        for v in neighbors:
            if v in Q: # Only check neighbours that are also in "Q"
                len_u_v = 0 if board.is_color(v, color) else 1 # this isn't working as intended i think...
                alt = dist[u] + len_u_v
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
        dist.pop(u) # This is to ensure that the keys in "dist" match the ones in "Q"
    
    return dist, prev

def minimax(board: HexBoard, depth: int, is_max: bool) -> float:

    if depth == 0 or board.is_game_over():
        return simple_dijkstra(board, (1,1), is_max)

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

hb = HexBoard(11)
hb.place((1,1), hb.BLUE)
hb.place((2,1), hb.RED)
hb.place((4, 0), hb.BLUE)
hb.print()
S = simple_dijkstra(hb, (0, 10), True) # use True for BLUE eval, False for RED eval
print(S)

