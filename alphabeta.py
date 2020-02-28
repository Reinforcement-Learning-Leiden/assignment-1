from hex_skeleton import HexBoard
import copy
import time

import numpy as np

# global vars
_board_size: int = 5
_INF: float = 99999.0

# initialize board with size n
_board = HexBoard(_board_size)

# NOTE: THE AI SHOULD START WITH A RANDOM MOVE, OR MAYBE JUST A SET MOVE
# NOTE: THE AI DOES NOT KNOW HOW TO MAKE THE FINISHING BLOW YET

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
                len_u_v = -1 if board.is_color(v, color) else 1 # this isn't working as intended i think...
                ### BLOCK TO MAKE AI MORE AGGRESSIVE ###
                if board.border(color, v): # If there is a move that reaches the border in the simulation
                    if board.check_win(color): # And it results in a win
                        len_u_v = -2 # Make that move more valuable
                ### END OF AGGRO BLOCK ###
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

#TODO: (CODE CLEANUP) Make update board take a color as param instead of an is_max bool?
def _update_board(board: HexBoard, l_move, is_max: bool) -> HexBoard:
    """
    Makes a deep copy of the board and updates the board state on that copy.
    This makes it so that we don't need to use an undo move function.
    The reason for using deepcopy is because python passes objects by reference
    if you use the "=" operator
    """
    board = copy.deepcopy(board) # I think this was the problem with the minimax core, it was using a reference instead of a deep copy
    color = board.BLUE if is_max else board.RED
    board.place(l_move, color)
    return board


def dummy_eval() -> float:
    return np.random.randint(0, 10)

def alphabeta_move(board:HexBoard, depth:int, is_max:bool, show_AI=False):
    """
    Set is_max to True for BLUE player, and False for RED player.
    You can set the depth to whatever you want really, just don't go too deep it'll take forever.
    Set show_AI to True if you want to see it's scoring process
    """
    start_time=time.time()
    legal_moves = board.get_move_list()
    best_score = -np.inf
    best_move = None
    for move in legal_moves:
        sim_board = _update_board(board, move, is_max)
        if sim_board.check_win(sim_board.BLUE if is_max else sim_board.RED): # KILLER MOVE: If we find a move in the simulation that wins, make that move no matter what
            if show_AI: print(f"KILLER MOVE FOUND: {move}")
            best_move = move
            best_score = np.inf
            break
        score = alphabeta(sim_board, depth=depth, alpha=-np.inf, beta=np.inf, is_max=is_max) # For some reason performs better if you use is_max=False
        if show_AI: print(f"CURRENT SCORE: {score} for MOVE: {move}")
        if score > best_score:
            best_score = score
            best_move = move
    if show_AI: print(f"BEST MOVE: {best_move} with BEST SCORE: {best_score}")
    if depth==3:    HexBoard.dTime+=time.time()-start_time
    if depth==4:    HexBoard.d4Time+=time.time()-start_time

    return best_move
############################################################################
#move with random eval#
def alphabeta_moveR(board:HexBoard, depth:int, is_max:bool, show_AI=False):
    """
    Set is_max to True for BLUE player, and False for RED player.
    You can set the depth to whatever you want really, just don't go too deep it'll take forever.
    Set show_AI to True if you want to see it's scoring process
    """
    start_time=time.time()
    legal_moves = board.get_move_list()
    best_score = -np.inf
    best_move = None
    for move in legal_moves:
        sim_board = _update_board(board, move, is_max)
        if sim_board.check_win(sim_board.BLUE if is_max else sim_board.RED): # KILLER MOVE: If we find a move in the simulation that wins, make that move no matter what
            if show_AI: print(f"KILLER MOVE FOUND: {move}")
            best_move = move
            best_score = np.inf
            break
        score = alphabetaRandom(sim_board, depth=depth, alpha=-np.inf, beta=np.inf, is_max=is_max) # For some reason performs better if you use is_max=False
        if show_AI: print(f"CURRENT SCORE: {score} for MOVE: {move}")
        if score > best_score:
            best_score = score
            best_move = move
    if show_AI: print(f"BEST MOVE: {best_move} with BEST SCORE: {best_score}")
    HexBoard.rTime += time.time() - start_time
    return best_move
###########################################################################################
### alphabeta with Dijkstra evaluation ###
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
                    HexBoard.cutoffs+=1
                    break

        else:
            g: float = _INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = min(g, alphabeta(updated_board,
                                     depth-1, alpha, beta, is_max=True))

                beta = min(beta, g)
                if beta <= alpha:
                    HexBoard.cutoffs+=1
                    break
    
        return g
    
    else:
        print("NO MORE LEGAL MOVES LEFT")
        return dijkstra_eval(board)

#######################################################################################
### AlphaBeta with random evaluation ###
def alphabetaRandom(board: HexBoard, depth: int, alpha: float, beta: float, is_max: bool) -> float:
    # board.print()
    if depth == 0 or board.is_game_over():
        return dummy_eval()

    legals = board.get_move_list()
    if legals:

        if is_max:
            g: float = -_INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = max(g, alphabetaRandom(updated_board,
                                     depth - 1, alpha, beta, is_max=False))

                alpha = max(alpha, g)
                if beta <= alpha:
                    HexBoard.rCutoffs += 1
                    break

        else:
            g: float = _INF

            for move in legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                g = min(g, alphabetaRandom(updated_board,
                                     depth - 1, alpha, beta, is_max=True))

                beta = min(beta, g)
                if beta <= alpha:
                    HexBoard.rCutoffs += 1
                    break

        return g

    else:
        print("NO MORE LEGAL MOVES LEFT")
        return dummy_eval()
#########################################################################################



## UNCOMMENT BELOW IF YOU WANT TO START THE GAME IN A FIXED STATE
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


#### ITERATIVE DEPENING AND TRANSPOSITION TABLES

import time
import random


class TranspositionTable:
    BLUE = 1
    RED = 2
    EMPTY = 3

    # TOASK: color needed?
    def __init__(self,board,board_size):
        self.board_size = board_size
        self.zobTable = [[[random.randint(1, 2 ** 64 - 1) for i in range(2)] for j in range(self.board_size)] for k in
                         range(self.board_size)]
        #self.tbl_size = 2 ** 20  # experimental, can be changed
        self.dict = {}


    ### ZOBRIST HASHING

    def indexing(self, piece):
        ''' mapping colors to a particular number'''
        if (piece == self.BLUE):
            return 1
        if (piece == self.RED):
            return 2
        else:
            return -1

    # each time a move is made on our board, whether during game play or alpha beta search we simply update the Zobrist Hash:
    def computeHash(self, board, board_size):
        h = 0
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != self.EMPTY:
                    piece = self.indexing(board[i][j])
                    h ^= self.zobTable[i][j][piece]
        print("in hash function ", h)
        board.print()
        return h

    def store(self, board,board_size, heuristic_val, depth, bestmove):
        print("in store function ")
        self.hashValue = self.computeHash(board,board_size)
        self.dict[self.hashValue] = {"board":board, "val": heuristic_val,"depth":depth,"bm":bestmove}

    def lookup(self, board,board_size, depth):
        print("in lookup function ")
        hit = False
        hash_v = self.computeHash(board,board_size)
        if hash_v in self.dict:
            hit = True
            print("lookup true",hash_v, hit, self.dict)
            return hit, self.dict[hash_v]["val"], self.dict[hash_v]["bm"]
        return hit
    
# ERROR WAS HERE, JUST PASSING AND DOING NOTHING
def time_is_up(seconds: int):
    t = time.time()
    while not time.time() - t >= seconds:
        pass
    #print(time.time(), t, time.time() - t)
    return True


def iterative_deepening(board: HexBoard, alpha: float, beta: float, is_max: bool, max_seconds:int = 5):
    d = 1
    itd1 = 0.0
    try:
        t = time.time()
        while not time.time() - t >= max_seconds:
            # wait
            print("inside iterative deepening while", '0000000', time.time())
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(alphabeta_Id, board, d, alpha, beta, is_max)
                itd1 = future.result()
                print(itd1)
            #itd1 = alphabeta_Id(board, d, alpha, beta, is_max)
            #release
            print("inside iterative deepening while", '1111111', time.time())
            d = d+1
            print("inside iterative deepening while", '2222222')
        print("inside iterative deepening", d)
    except:
        print("error in iterative deepening")
    return itd1

transposition_table = TranspositionTable(_board,_board_size)

# dic = {hashvalue:{board,val,depth,bm,}}
dic_of_class = {}

def very_simple(depth):
    print("inside very siiiiiiiimple", depth)


def alphabeta_Id(board: HexBoard, depth: int, alpha: float, beta: float, is_max: bool) -> float:
    # board.print()
    print("in alphabeta_Id000000000")
    try:
        (hit, g, ttbm) = transposition_table.lookup(board,board.get_board_size(),depth)
        print("in alphabeta_Id", hit, g, ttbm)
    except Exception as e:  #
        print('Exception in running lookup function: ' + str(e))
    if hit():
        return g

    if depth == 0 or board.is_game_over():
        g =  dijkstra_eval(board)
        bm = ()

    legals = board.get_move_list()
    if legals:
        if is_max:
            g: float = -_INF

            for move in ttbm+legals:
                updated_board: HexBoard = _update_board(board, move, is_max) # y do we make the move first?
                gc = alphabeta_Id(updated_board, depth-1,alpha,beta,is_max)
                if gc > g:
                    bm = updated_board
                    g = gc

                alpha = max(alpha, g)
                if beta <= alpha:
                    break

        else: # if is_max False
            g: float = _INF

            for move in ttbm+legals:
                updated_board: HexBoard = _update_board(board, move, is_max)
                gc = alphabeta_Id(updated_board, depth - 1, alpha, beta, is_max)
                if gc < g:
                    bm = updated_board
                    g = gc

                beta = min(beta, g)
                if beta <= alpha:
                    break
        transposition_table.store(updated_board,updated_board.get_board_size(),g,depth,bm)
        return g

    else:
        print("NO MORE LEGAL MOVES LEFT")
        return dijkstra_eval(board)



# the function with iterative deepening
def alphabeta_move_Id(board: HexBoard, is_max: bool, show_AI=False): #, depth: int
    """
    Set is_max to True for BLUE player, and False for RED player.
    You can set the depth to whatever you want really, just don't go too deep it'll take forever.
    Set show_AI to True if you want to see it's scoring process
    """
    legal_moves = board.get_move_list()
    print("num of legal moves", len(legal_moves))
    best_score = -np.inf
    best_move = None
    for move in legal_moves:
        sim_board = _update_board(board, move, is_max)
        if sim_board.check_win(
                sim_board.BLUE if is_max else sim_board.RED):  # KILLER MOVE: If we find a move in the simulation that wins, make that move no matter what
            if show_AI: print(f"KILLER MOVE FOUND: {move}")
            best_move = move
            best_score = np.inf
            break
        #thread = threading.Thread(target=iterative_deepening, kwargs=dict(board = sim_board,alpha=-np.inf,beta = np.inf, is_max = is_max))
        #thread.start()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(iterative_deepening, sim_board, alpha=-np.inf, beta=np.inf,
                          is_max=is_max)
            score = future.result()
            print("score ",score)
        # wait here for the result to be available before continuing
        #thread.join()
        #score = iterative_deepening(sim_board, alpha=-np.inf, beta=np.inf,
        #                 is_max=is_max)  # For some reason performs better if you use is_max=False
        if show_AI: print(f"ID CURRENT SCORE: {score} for MOVE: {move}")
        if score > best_score:
            best_score = score
            best_move = move
    if show_AI: print(f"BEST MOVE_ID: {best_move} with BEST SCORE: {best_score}")
    return best_move



