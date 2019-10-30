import numpy as np
from pprint import pprint
import pandas as pd

class P2:

    def __init__(self):
        self.n_vertex=0
        self.n_edge=0
        self.type_graph=''
        self.edge_matrix = None
        self.node_source=''

    def read_input(self):
        df = pd.read_csv('input_graph_1.txt', delimiter=' ', header=None)
        n = df.values
        return n

    def parse_input(self, i):
        self.n_vertex = int(i[0,0])
        self.n_edge = int(i[0,1])
        self.type_graph = str(i[0,2])
        self.edge_matrix = i[1:1+self.n_edge,:]
        if len(i) == self.n_edge + 2:
            self.node_source = i[-1,0]
        else:
            self.node_source = self.edge_matrix[0,0]

    def print_info(self):
        _info={
            'no_of_vertex': self.n_vertex,
            'no_of_edges': self.n_edge,
            'type_graph': self.type_graph,
            'edge_matrix': self.edge_matrix,
            'node_source': self.node_source
        }
        pprint(_info)

if __name__ == '__main__':
    p=P2()
    i=p.read_input()
    p.parse_input(i)
    p.print_info()
    # print(p.edge_matrix.shape)


