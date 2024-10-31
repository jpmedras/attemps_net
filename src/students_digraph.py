from networkx import DiGraph
from pandas import DataFrame
from typing import Dict, Set, Any

class StudentsDiGraph():
    def __init__(self, attemps:DataFrame=None) -> None:
        
        self.__attemps = attemps

        self.__exercises = self.__student_exercises()

        self.__graph = DiGraph()
        self.__add_nodes()
        self.__add_edges()

    def __student_exercises(self) -> Dict[Any, Set[Any]]:
        exercises = {}

        for index, row in self.__attemps.iterrows():
            if row['student_id'] not in exercises:
                exercises[row['student_id']] = set()
            
            if row['is_correct']:
                exercises[row['student_id']].add(row['exercise_id'])

        return exercises
    
    @property
    def exercises(self) -> Dict[Any, Set[Any]]:
        return self.__exercises

    def __add_nodes(self) -> None:
        for student_u in self.__exercises:
            if not self.__graph.has_node(student_u):
                self.__graph.add_node(student_u, size=len(self.__exercises[student_u]))
    
    def __add_edges(self):
        for u, neighbors_u in self.__exercises.items():
            for v, neighbors_v in self.__exercises.items():

                if u == v:
                    continue

                if len(neighbors_u) > 0:
                    overlap = len(neighbors_u & neighbors_v) / len(neighbors_u)

                    if overlap > 0:
                        self.__graph.add_edge(u, v, weight=overlap)

    @property
    def graph(self) -> DiGraph:
        return self.__graph
    
    def filter(self, k:float) -> 'StudentsDiGraph':
        graph = DiGraph()

        for u, v, data in self.graph.edges(data=True):
            if data['weight'] >= k:
                graph.add_edge(u, v, **data)

        self.__graph = graph

        return self