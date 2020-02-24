from hex_skeleton import HexBoard
from hexagon import Hexagon

class Graph:
    def __init__(self, board: HexBoard):
        self.board = board
        self.vertices = []
        
        for coord in self.board.get_move_list():
            self.vertices.append(Hexagon(coord, board))
        
    def find_shortest_path(self):
        # TODO: properly implement Dijkstra
        pass

    def dijkstra(self):
        # TODO: properly implement this
        pass

    def print_vertices(self):
        for hexagon in self.vertices:
            print(hexagon.coords)
        
