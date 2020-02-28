from hex_skeleton import HexBoard
import copy
from priority_queue import PriorityQueue

import numpy as np

# global vars
_board_size: int = 5
_INF: float = 99999.0

# initialize board with size n
_board = HexBoard(_board_size)

# NOTE: THE AI SHOULD START WITH A RANDOM MOVE, OR MAYBE JUST A SET MOVE
# NOTE: THE AI DOES NOT KNOW HOW TO MAKE THE FINISHING BLOW YET


def simple_dijkstra(board: HexBoard, source, is_max):

    Q = PriorityQueue()
    # V_set = board.get_all_vertices()
    V_set = board.get_move_list()
    dist = {}
    # dist_clone = {}  # I made a clone of dist to retain the information in dist
    prev = {}
    for v in V_set:
        # if v != source:
        dist[v] = np.inf
        # dist_clone[v] = np.inf  # clone
        prev[v] = None
        Q.add_task(task=v, priority=dist[v])  # add task with prio
    dist[source] = 0
    # dist_clone[source] = dist[source]  # clone

    while len(Q.pq) != 0:
        # u = min(dist, key=dist.get)
        u = Q.extract_min()

        color = board.BLUE if is_max else board.RED

        neighbors = board.get_neighbors(u[2])  # Get last value of u

        for v in neighbors:
            if v in Q.pq:  # Only check neighbours that are also in "Q"
                len_u_v = -1 if board.is_color(v, color) else 1
                ### BLOCK TO MAKE AI MORE AGGRESSIVE ###
                # If there is a move that reaches the border in the simulation
                # if board.border(color, v):
                #     if board.check_win(color):  # And it results in a win
                #         len_u_v = -2  # Make that move more valuable
                ### END OF AGGRO BLOCK ###
                alt = dist[u] + len_u_v
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    Q.add_task(v, alt)

    return dist, prev


def get_shortest_path(board: HexBoard, distances, color):
    """Gets the shortest path to a border and returns the length as score"""
    borders = board.get_borders(color)
    filtered_borders = list(
        filter(lambda x: x in board.get_move_list(), borders))
    # print(f"ALL BORDERS: {borders}")
    shortest = np.inf
    for border in filtered_borders:
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

# TODO: (CODE CLEANUP) Make update board take a color as param instead of an is_max bool?


def _update_board(board: HexBoard, l_move, is_max: bool) -> HexBoard:
    """
    Makes a deep copy of the board and updates the board state on that copy.
    This makes it so that we don't need to use an undo move function.
    The reason for using deepcopy is because python passes objects by reference
    if you use the "=" operator
    """
    board = copy.deepcopy(
        board)  # I think this was the problem with the minimax core, it was using a reference instead of a deep copy
    color = board.BLUE if is_max else board.RED
    board.place(l_move, color)
    return board


def dummy_eval() -> float:
    return np.random.randint(0, 10)


def alphabeta_move(board: HexBoard, depth: int, is_max: bool, show_AI=False):
    """
    Set is_max to True for BLUE player, and False for RED player.
    You can set the depth to whatever you want really, just don't go too deep it'll take forever.
    Set show_AI to True if you want to see it's scoring process
    """
    legal_moves = board.get_move_list()
    best_score = -np.inf
    best_move = None
    for move in legal_moves:
        sim_board = _update_board(board, move, is_max)
        # KILLER MOVE: If we find a move in the simulation that wins, make that move no matter what
        if sim_board.check_win(sim_board.BLUE if is_max else sim_board.RED):
            if show_AI:
                print(f"KILLER MOVE FOUND: {move}")
            best_move = move
            best_score = np.inf
            break
        # For some reason performs better if you use is_max=False
        score = alphabeta(sim_board, depth=depth, alpha=-
                          np.inf, beta=np.inf, is_max=is_max)
        if show_AI:
            print(f"CURRENT SCORE: {score} for MOVE: {move}")
        if score > best_score:
            best_score = score
            best_move = move
    if show_AI:
        print(f"BEST MOVE: {best_move} with BEST SCORE: {best_score}")
    return best_move


def alphabeta(board: HexBoard, depth: int, alpha: float, beta: float, is_max: bool) -> float:
    # board.print()
    if depth == 0 or board.is_game_over():
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
        print("NO MORE LEGAL MOVES LEFT")
        return dijkstra_eval(board)

# UNCOMMENT BELOW IF YOU WANT TO START THE GAME IN A FIXED STATE
# _board.place((1,1), _board.BLUE)
# _board.place((0,2), _board.RED)

# eval_score = alphabeta(board=_board, depth=4, alpha=-np.inf, beta=np.inf, is_max=True)
# print(eval_score)

# b = HexBoard(5)
# b.place((1,1), b.BLUE)
# b.place((0,0), _board.RED)
# b.place((3,1), b.BLUE)
# b.place((0,1), _board.RED)
# b.place((2,4), b.BLUE)
# b.place((0,2), _board.RED)
# b.place((4,1), b.BLUE)
# b.place((0,4), b.RED)
# b.place((0,3), b.BLUE)
# b.place((1,4), b.RED)
# b.place((1,2), b.BLUE)
# b.print()
# a = dijkstra_eval(b)
# print(a)
# move = alphabeta_move(b, depth=4)
# print(move)
