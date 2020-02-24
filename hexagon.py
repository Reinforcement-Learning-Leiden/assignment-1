from hex_skeleton import HexBoard
import numpy as np

# Structure to store info for each hexagon

class Hexagon:
    def __init__(self, coordinate, board: HexBoard):
        self.coords = coordinate
        self.board = board
        
        self.path_len_fs = np.inf
        self.path_verts_fs: [Hexagon] = [] # A list of hexagons
        self.neighbors: [Hexagon] = []

    # Not sure if this method is super useful here, maybe replace to Graph class
    def get_neighbour_hexagons(self, list_of_neighbor_coords):
        for coord in list_of_neighbor_coords:
            self.neighbors.append(Hexagon(coord, self.board))
        return self.neighbors
