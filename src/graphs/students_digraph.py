from networkx import DiGraph
from pandas import DataFrame

class StudentsDiGraph():
    def __init__(self, data:DataFrame) -> None:

        # if data.columns != ['student_id', 'exercise_ids']:
        #     raise Exception('')
        
        self.__solved = data

        self.__graph = DiGraph()
        self.__add_nodes()
        self.__add_edges()

    @classmethod
    def from_attemps(cls, attemps:DataFrame) -> 'StudentsDiGraph':
        data = []
        for student_id, group in attemps.groupby('student_id'):
            data.append(
                {
                    'student_id': student_id,
                    'exercise_ids': group.loc[group['is_correct'] == True, 'exercise_id'].unique().tolist()
                }  
            )

        df = DataFrame(data)
        df = df.set_index('student_id')

        return cls(df)
    
    def __add_nodes(self) -> None:
        for student_u, solved_exercise_ids in self.__solved.iterrows():
            if not self.__graph.has_node(student_u):
                self.__graph.add_node(student_u, size=len(solved_exercise_ids['exercise_ids']))
    
    def __add_edges(self) -> None:
        for u, neighbors_u in self.__solved.iterrows():
            for v, neighbors_v in self.__solved.iterrows():

                if u == v:
                    continue

                if len(neighbors_u['exercise_ids']) > 0 and len(neighbors_v['exercise_ids']) > 0:
                    overlap = len(set(neighbors_u['exercise_ids']) & set(neighbors_v['exercise_ids'])) / len(neighbors_u['exercise_ids'])

                    if overlap > 0:
                        self.__graph.add_edge(u, v, weight=overlap)

    @property
    def solved(self) -> DataFrame:
        return self.__solved

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