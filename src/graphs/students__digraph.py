from networkx import DiGraph
from pandas import DataFrame
from typing import Dict, Set, Any

class StudentsDiGraph():
    def __init__(self, attemps:DataFrame=None) -> None:
        
        self.__attemps = attemps
        self.__solved = self.__compute_solved_exercise_ids()

        self.__graph = DiGraph()
        self.__add_nodes()
        self.__add_edges()

    def __compute_solved_exercise_ids(self):
        data = []
        for student_id, group in self.__attemps.groupby('student_id'):
            data.append(
                {
                    'student_id': student_id,
                    'exercise_ids': group.loc[group['is_correct'] == True, 'exercise_id'].unique().tolist()
                }  
            )

        df = DataFrame(data)
        df = df.set_index('student_id')

        return df
    
    def __add_nodes(self) -> None:
        for student_u, solved_exercise_ids in self.__solved.iterrows():
            if not self.__graph.has_node(student_u):
                self.__graph.add_node(student_u, size=len(solved_exercise_ids['exercise_ids']))
    
    def __add_edges(self):
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
    
    def filter(self, k:float) -> 'StudentsDiGraph':
        graph = DiGraph()

        for u, data in self.graph.nodes(data=True):
            graph.add_node(u, **data)

        for u, v, data in self.graph.edges(data=True):
            if data['weight'] >= k:
                graph.add_edge(u, v, **data)

        self.__graph = graph

        return self