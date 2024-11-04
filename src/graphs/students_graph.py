from networkx import Graph
from networkx import write_gexf
from .students_digraph import StudentsDiGraph
from pandas import DataFrame
from pandas import read_csv

class StudentsGraph():
    def __init__(self, attemps:DataFrame=None, filtering_parameter:float=None) -> None:

        self.__digraph = StudentsDiGraph(attemps=attemps)
        
        if filtering_parameter is not None:
            self.__digraph = self.__digraph.filter(filtering_parameter)

        self.__graph = Graph()
        self.__add_nodes()
        self.__add_edges()
    
    @property
    def solved(self) -> DataFrame:
        return self.__digraph.solved

    def __add_nodes(self) -> None:
        for node, data in self.__digraph.graph.nodes(data=True):
            self.__graph.add_node(node, **data)
    
    def __add_edges(self) -> None:
        for u in self.__digraph.graph:
            for v in self.__digraph.graph:

                if u == v:
                    continue

                if self.__digraph.graph.has_edge(u, v) and self.__digraph.graph.has_edge(v, u):
                    self.__graph.add_edge(u, v, weight=len(set(self.solved.loc[u, 'exercise_ids']) & set(self.solved.loc[v, 'exercise_ids'])))

    @property
    def graph(self) -> Graph:
        return self.__graph