import numpy as np
from pprint import pprint
import pandas as pd
import sys

class Vertex:
    def __init__(self, n='', p=None, dfs=sys.maxsize):
        self.name=n
        self.parent=p
        self.distance_from_source=dfs

class Edge:
    def __init__(self, fv=None, tv=None, w=None):
        self.from_vertex=fv
        self.to_vertex=tv
        self.weight=w

class Graph:
    def get_vertex_by_name(self, n=''):
        v=None
        if n:
            for _v in self.vertices:
                if _v.name == n:
                    v=_v
                    break
        return v

    def __init__(self, nv, ne, tg, em, ns):
        self.vertices=[]
        self.edges=[]
        vertex_name_list=[]
        for row in em:
            fv_name=str(row[0])
            tv_name=str(row[1])
            fv = None
            tv = None
            if fv_name not in vertex_name_list:
                vertex_name_list.append(fv_name)
                fv=Vertex(n=fv_name)
                self.vertices.append(fv)
            else:
                fv = self.get_vertex_by_name(n=fv_name)
            if tv_name not in vertex_name_list:
                vertex_name_list.append(tv_name)
                tv=Vertex(n=tv_name)
                self.vertices.append(tv)
            else:
                tv = self.get_vertex_by_name(n=tv_name)
            w=int(row[2])
            if tg == 'D':
                e=Edge(fv=fv, tv=tv, w=w)
                self.edges.append(e)
            else:
                e1=e=Edge(fv=fv, tv=tv, w=w)
                self.edges.append(e1)
                e2=e=Edge(fv=tv, tv=fv, w=w)
                self.edges.append(e2)

class P2:

    def __init__(self):
        self.n_vertex=0
        self.n_edge=0
        self.type_graph=''
        self.edge_matrix = None
        self.node_source=''

    def read_input(self, file_name=''):
        df = pd.read_csv(file_name, delimiter=' ', header=None)
        n = df.values
        return n

    def parse_input(self, i):
        self.n_vertex = int(i[0,0])
        self.n_edge = int(i[0,1])
        self.type_graph = str(i[0,2])
        self.edge_matrix = i[1:1+self.n_edge,:]
        if len(i) == self.n_edge + 2:
            ns_name=i[-1,0]
        else:
            ns_name= self.edge_matrix[0,0]
        self.node_source = Vertex(n=ns_name, dfs=0)

    def print_info(self):
        _info={
            'no_of_vertex': self.n_vertex,
            'no_of_edges': self.n_edge,
            'type_graph': self.type_graph,
            'edge_matrix': self.edge_matrix,
            'node_source_name': str(self.node_source.name) if self.node_source and self.node_source.name else ''
        }
        pprint(_info)

    def find_shortest_path(self, verbose=False):
        g=Graph(
            self.n_vertex,
            self.n_edge,
            self.type_graph,
            self.edge_matrix,
            self.node_source
        )
        if verbose:
            for v in g.vertices:
                print(v.name)
            print('-----------------------------------------------------------')
            for e in g.edges:
                print(str(e.from_vertex.name) + "---" + str(e.to_vertex.name) + ":" + str(e.weight))

if __name__ == '__main__':
    #input text file
    input_file_name='input_graph_1.txt'

    #worker for project 2
    p=P2()
    i=p.read_input(file_name=input_file_name)
    p.parse_input(i)
    # p.print_info()

    # find shortest path
    p.find_shortest_path(verbose=True)


