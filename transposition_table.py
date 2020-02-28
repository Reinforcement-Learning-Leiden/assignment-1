import time
import random
import numpy as np
from hex_skeleton import HexBoard


class TranspositionTable:
    BLUE = 1
    RED = 2
    EMPTY = 3

    ttCutoffs=0
    total_ttCutoffs=0
    ttTime=0

    # TOASK: color needed?
    def __init__(self, board: HexBoard):
        self.board = board
        self.zobTable = [[[random.randint(1, 2 ** 64 - 1) for i in range(2)] for j in range(self.board.size)] for k in
                         range(self.board.size)]
        # self.tbl_size = 2 ** 20  # experimental, can be changed
        self.dict = {}

    # ZOBRIST HASHING

    def indexing(self, piece):
        ''' mapping colors to a particular number'''
        if (piece == self.BLUE):
            return 1
        if (piece == self.RED):
            return 2
        else:
            return -1

    # each time a move is made on our board, whether during game play or alpha beta search we simply update the Zobrist Hash:
    def computeHash(self, board):
        h = 0
        for i, p in board.get_all_vertices():
            piece = self.indexing((i, p))
            h ^= self.zobTable[i][p][piece]
        # print("in hash function ", h)
        return h

    def store(self, board, heuristic_val, depth, bestmove):
        # print("in store function ")
        self.hashValue = self.computeHash(board)
        self.dict[self.hashValue] = {
            "board": self.board, "val": heuristic_val, "depth": depth, "bm": bestmove}

    def lookup(self, board, depth):
        # print("in lookup function ")
        hit = False
        hash_v = self.computeHash(board)
        if hash_v in self.dict and depth == self.dict[hash_v]["depth"]:
            if depth == self.dict[hash_v]["depth"]:
                hit = True
                # print("lookup true", hash_v, hit, self.dict)
                return hit, self.dict[hash_v]["val"], self.dict[hash_v]["bm"]
            # return ttbm regardless of depth matching
            return hit, self.dict[hash_v]["val"], self.dict[hash_v]["bm"]
        return hit, -np.inf, (0, 0)
