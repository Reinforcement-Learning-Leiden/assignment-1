from hex_skeleton import HexBoard
from hexagon import Hexagon

import numpy as np

class Graph:
    def __init__(self, board: HexBoard):
        self.board = board
        self.vertices = [Hexagon(coord, board) for coord in self.board.get_move_list()]
        
        # for coord in self.board.get_move_list():
        print(f"COORDS: {[v.coords for v in self.vertices]}")
        #     self.vertices.append(Hexagon(coord, board))
        
    def calculate_all_neighbors(self):
        for hexagon in self.vertices:
            neighbor_coords = self.board.get_neighbors(hexagon.coords)
            hexagon.get_neighbour_hexagons(neighbor_coords)

    def calculate_neighbors(self, hexagon: Hexagon):
        """Only calculate neighbours of a specific hexagon"""
        neighbor_coords = self.board.get_neighbors(hexagon.coords)
        hexagon.get_neighbour_hexagons(neighbor_coords)
    
    def find_shortest_path_from(self, from_hexagon: Hexagon, perspective):
        # TODO: properly implement Dijkstra first
        pass


    def dijkstra(self, start_vertex: Hexagon, perspective):
        # TODO: properly implement this
        # note: path_len_fs means Path Length from Start like in the resource
        current_vertices = self.vertices
        start_vertex.path_len_fs = 0 # Set the start vertex's path length to 0
        start_vertex.path_verts_fs.append(start_vertex)
        current_vertex: Hexagon = start_vertex
        print(f"CURRENT VERTEX: {current_vertex.coords}")
        print(f"ALL CURRENT VERTICES: {[v.coords for v in current_vertices]}")
        while current_vertex:
            current_vertices.remove(current_vertex)
            self.calculate_neighbors(current_vertex)
            filtered_neighbors = list(filter(lambda x: x.path_len_fs == np.inf, current_vertex.neighbors))
            for neighbor in filtered_neighbors:
                weight = 0.0 if neighbor.color == perspective else 1.0
                t_new_weight = current_vertex.path_len_fs + weight
                if t_new_weight < neighbor.path_len_fs:
                    neighbor.path_len_fs = t_new_weight
                    neighbor.path_verts_fs = current_vertex.path_verts_fs
                    neighbor.path_verts_fs.append(neighbor)
            if not current_vertices or len(current_vertices) == 0:
                return
            else:
                current_vertex = min(current_vertices, key=lambda x: x.path_len_fs)
                print(f"AAAAAH {current_vertex}")

    def print_vertices(self):
        for hexagon in self.vertices:
            print(hexagon.coords)
        
