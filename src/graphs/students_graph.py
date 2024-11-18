from networkx import Graph
from .students_digraph import StudentsDiGraph
from pandas import DataFrame

class StudentsGraph(StudentsDiGraph):
    def __init__(self, solving_df: DataFrame, filtering_parameter: float = None) -> None:

        self.__digraph = StudentsDiGraph(solving_df=solving_df)
        
        if filtering_parameter is not None:
            self.__digraph = self.__digraph.filter(filtering_parameter)

        self.__graph = Graph()
        self.__graph.name = 'G'

        self.__add_nodes()
        self.__add_edges()

    def __add_nodes(self) -> None:
        self.__graph.add_nodes_from(self.__digraph.graph.nodes(data=True))
    
    def __add_edges(self) -> None:
        for u, data_u in self.__digraph.graph.nodes(data=True):
            for v, data_v in self.__digraph.graph.nodes(data=True):

                if u == v:
                    continue

                neighbors_u = set(data_u['neighborhood'])
                neighbors_v = set(data_v['neighborhood'])

                if self.__digraph.graph.has_edge(u, v) and self.__digraph.graph.has_edge(v, u):
                    self.__graph.add_edge(u, v, weight=len(neighbors_u & neighbors_v))

    @property
    def graph(self) -> Graph:
        return self.__graph