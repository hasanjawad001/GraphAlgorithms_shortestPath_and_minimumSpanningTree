import numpy as np
from pprint import pprint
import pandas as pd
import sys

class Vertex:
    def __init__(self, n='', p=None, dfs=sys.maxsize, r=0):
        self.name=n
        self.parent=p
        self.distance_from_source=dfs
        self.rank=r

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

    def __init__(self, nv, ne, tg, em, ns, t):
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
                if fv_name == ns.name:
                    fv = ns
                else:
                    fv = Vertex(n=fv_name)
                self.vertices.append(fv)
            else:
                fv = self.get_vertex_by_name(n=fv_name)
            if tv_name not in vertex_name_list:
                vertex_name_list.append(tv_name)
                if tv_name == ns.name:
                    tv=ns
                else:
                    tv=Vertex(n=tv_name)
                self.vertices.append(tv)
            else:
                tv = self.get_vertex_by_name(n=tv_name)
            # print(row[2])
            w=int(row[2])
            if tg == 'D':
                e=Edge(fv=fv, tv=tv, w=w)
                self.edges.append(e)
            else:
                if t=='mst':
                    e1=Edge(fv=fv, tv=tv, w=w)
                    self.edges.append(e1)
                else:
                    e1=Edge(fv=fv, tv=tv, w=w)
                    self.edges.append(e1)
                    e2=Edge(fv=tv, tv=fv, w=w)
                    self.edges.append(e2)

    def get_adjacent(self, v=None):
        l=[]
        if v:
            v_name=v.name
            for e in self.edges:
                if e.from_vertex.name == v_name:
                    v_adjacent = e.to_vertex
                    l.append(v_adjacent)
        return l

    def get_edge_from_vertices(self, fv=None, tv=None):
        edge=None
        for e in self.edges:
            if e.from_vertex.name==fv.name and e.to_vertex.name == tv.name:
                edge=e
                break
        return edge

class P2:
    def __init__(self, type=None):
        self.n_vertex=0
        self.n_edge=0
        self.type_graph='' # directed/undirected
        self.edge_matrix = None
        self.node_source=''
        self.type=type

    def read_input(self, file_name=''):
        df = pd.read_csv(file_name, delimiter=' ', header=None)
        n = df.values
        return n

    def parse_input(self, i):
        self.n_vertex = int(i[0,0])
        self.n_edge = int(i[0,1])
        self.type_graph = str(i[0,2]) if i[0,2] else 'U'
        self.edge_matrix = i[1:1+self.n_edge,:]
        if len(i) == self.n_edge + 2:
            ns_name=i[-1,0]
        else:
            ns_name= self.edge_matrix[0,0]
        self.node_source = Vertex(n=ns_name, dfs=0)
        if self.type == 'sp':
            print('Source Node: %s'%(ns_name))

    def print_info(self):
        _info={
            'no_of_vertex': self.n_vertex,
            'no_of_edges': self.n_edge,
            'type_graph': self.type_graph,
            'edge_matrix': self.edge_matrix,
            'node_source_name': str(self.node_source.name) if self.node_source and self.node_source.name else ''
        }
        pprint(_info)

    def extract_min(self, q=[]):
        u=q[0]
        min_distance_from_source = sys.maxsize
        for vertex in q:
            dfs = vertex.distance_from_source
            if dfs < min_distance_from_source:
                u=vertex
                min_distance_from_source=dfs
        u_name=u.name if u.name else ''
        if u_name:
            for elem in q:
                if elem.name == u_name:
                    q.remove(elem)
                    break
        return u, q

    def relax(self, graph=None, u=None, v=None):
        e=graph.get_edge_from_vertices(fv=u, tv=v)
        if e:
            for v_v in graph.vertices:
                if v_v.name == v.name:
                    for v_u in graph.vertices:
                        if v_u.name == u.name:
                            if int(v_v.distance_from_source) > int(v_u.distance_from_source) + int(e.weight):
                                v_v.distance_from_source = int(v_u.distance_from_source) + int(e.weight)
                                v_v.parent = v_u
        return graph

    def print_path_and_cost(self, graph=None):
        snode = None
        for v in graph.vertices:
            if v.name==self.node_source.name:
                snode=v
                break
        for n in graph.vertices:
            dnode = n
            dcost = str(n.distance_from_source)
            dpath = str(dnode.name)
            parentnode=dnode.parent
            while parentnode is not None:
                dpath = str(parentnode.name) + " -> " + str(dpath)
                parentnode = parentnode.parent
            print('Node: %s, Cost: %s, Path: %s'%(dnode.name, dcost, dpath))

    def apply_algo(self, name='', graph=None):
        from copy import copy
        if name=='dijkstra' and graph:
            s=[]
            q= copy(graph.vertices)
            while len(q) != 0:
                u, q = self.extract_min(q=q)
                s.append(u)
                adjacency_list = graph.get_adjacent(v=u)
                for v in adjacency_list:
                    graph=self.relax(graph=graph, u=u, v=v)
            self.print_path_and_cost(graph=graph)
            return []
        elif name=='mst_kruskal' and graph:
            a = []
            r=1
            for v in graph.vertices:
                v.parent=v
                v.rank=r
                r+=1
            sorted_edge_list = sorted(graph.edges, key=lambda item: item.weight)
            for e in sorted_edge_list:
                if e.from_vertex.parent.name != e.to_vertex.parent.name:
                    a.append(e)
                    e.to_vertex.parent = e.from_vertex.parent
            return a

    def find_shortest_path(self, verbose=False):
        g=Graph(self.n_vertex, self.n_edge, self.type_graph, self.edge_matrix, self.node_source, self.type)
        self.apply_algo(name='dijkstra', graph=g)

    def find_mst(self, verbose=False):
        g=Graph(self.n_vertex, self.n_edge, self.type_graph, self.edge_matrix, self.node_source, self.type)
        a=self.apply_algo(name='mst_kruskal', graph=g)
        total_cost = 0
        for e in a:
            print(str(e.from_vertex.name) + " -> " + str(e.to_vertex.name))
            total_cost += int(e.weight)
        print('total cost: %s'%(total_cost))


if __name__ == '__main__':
    print("=============================================================================================================")
    print("SHORTEST PATH ALGORITHM")
    print()
    #input text files
    file_list = ['dijkstra_graph_1.txt', 'dijkstra_graph_2.txt', 'dijkstra_graph_3.txt', 'dijkstra_graph_4.txt']
    # file_list = ['input_graph_4.txt']
    for file in file_list:
        input_file_name=file
        #worker for project 2
        p=P2(type='sp')
        i=p.read_input(file_name=input_file_name)
        p.parse_input(i)
        # p.print_info()

        # find shortest path
        p.find_shortest_path(verbose=False)
        print('END of File (%s) -----------------------------------------------'%(file))
        print()
    print()
    print()
    print("=============================================================================================================")
    print("MINIMUM SPANNING TREE (KRUSKAL)")
    print()
    #input text files
    file_list = ['mst_graph_1.txt', 'mst_graph_2.txt', 'mst_graph_3.txt', 'mst_graph_4.txt']
    # file_list = ['mst_graph_4.txt']
    for file in file_list:
        input_file_name=file
        #worker for project 2
        p=P2(type='mst')
        i=p.read_input(file_name=input_file_name)
        p.parse_input(i)
        # # p.print_info()

        # find mst
        p.find_mst(verbose=False)
        print('END of File (%s) -----------------------------------------------'%(file))
        print()


