from networkx import Graph
from .students_digraph import StudentsDiGraph
from pandas import DataFrame

class StudentsGraph(StudentsDiGraph):
    def __init__(self, data: DataFrame, filtering_parameter: float = None) -> None:

        self.__digraph = StudentsDiGraph(data=data)
        
        if filtering_parameter is not None:
            self.__digraph = self.__digraph.filter(filtering_parameter)

        self.__graph = Graph()
        self.__add_nodes()
        self.__add_edges()

    @classmethod
    def from_attemps(cls, attemps: DataFrame, filtering_parameter: float = None) -> 'StudentsGraph':
        digraph = StudentsDiGraph.from_attemps(attemps=attemps)
        return cls(data=digraph.solved, filtering_parameter=filtering_parameter)
    
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