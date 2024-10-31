from networkx import Graph
from networkx import write_gexf
from typing import Dict, Set, Any
from students_digraph import StudentsDiGraph
from pandas import DataFrame

from pandas import read_csv

class StudentsGraph():
    def __init__(self, attemps:DataFrame=None, k:float=None) -> None:

        self.__digraph = StudentsDiGraph(attemps=attemps)
        
        if k is not None:
            self.__digraph = self.__digraph.filter(k)

        self.__graph = Graph()
        self.__add_nodes()
        self.__add_edges()
    
    @property
    def exercises(self) -> Dict[Any, Set[Any]]:
        return self.__digraph.exercises

    def __add_nodes(self) -> None:
        for node, data in self.__digraph.graph.nodes(data=True):
            self.__graph.add_node(node, **data)
    
    def __add_edges(self):
        for u in self.__digraph.graph:
            for v in self.__digraph.graph:

                if u == v:
                    continue

                if self.__digraph.graph.has_edge(u, v) and self.__digraph.graph.has_edge(v, u):
                    self.__graph.add_edge(u, v, weight=len(self.exercises[u] & self.exercises[v]))

    @property
    def graph(self) -> Graph:
        return self.__graph
    
if __name__ == "__main__":
    df = read_csv(filepath_or_buffer='data/2023_module1.csv')
    graph = StudentsGraph(df).graph
    write_gexf(graph, path='data/2023.gexf')