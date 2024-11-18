from networkx import DiGraph
from pandas import DataFrame

class StudentsDiGraph():
    def __init__(self, solving_df:DataFrame) -> None:
        # check
        # check_solving_df(solving_df):
                
        self.__solving_df = solving_df

        self.__graph = DiGraph()
        self.__graph.name = 'O'

        self.__add_nodes()
        self.__add_edges()
    
    def __add_nodes(self) -> None:
        for student_u, group in self.__solving_df.groupby(level='student_id'):
            if not self.__graph.has_node(student_u):
                self.__graph.add_node(
                    student_u,
                    size=len(group),
                    neighborhood=group.index.get_level_values('exercise_id').to_list()
                )
    
    def __add_edges(self) -> None:
        for u, data_u in self.__graph.nodes(data=True):
            for v, data_v in self.__graph.nodes(data=True):

                if u == v:
                    continue

                neighbors_u = set(data_u['neighborhood'])
                neighbors_v = set(data_v['neighborhood'])

                if len(neighbors_u) > 0 and len(neighbors_v) > 0:
                    neighborhood_intersection = neighbors_u & neighbors_v
                    overlap = len(neighborhood_intersection) / len(neighbors_u)

                    if overlap > 0:
                        self.__graph.add_edge(u, v, weight=overlap)

    @property
    def graph(self) -> DiGraph:
        return self.__graph
    
    def filter(self, parameter:float) -> 'StudentsDiGraph':
        graph = DiGraph()

        for u, data in self.graph.nodes(data=True):
            graph.add_node(u, **data)

        for u, v, data in self.graph.edges(data=True):
            if data['weight'] >= parameter:
                graph.add_edge(u, v, **data)

        self.__graph = graph

        return self