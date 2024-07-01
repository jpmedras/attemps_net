from graphs.graph_abc import GraphABC
from networkx import Graph
from typing import Dict, Set
from typing import Any

class SimpleGraph(GraphABC):
    def _student_neighbors(self) -> Dict[Any, Set[Any]]:
        neighbors = {}

        for s in self._submissions:
            if s.student not in neighbors:
                neighbors[s.student] = set()
            
            if s.result:
                neighbors[s.student].add(s.question)

        return neighbors
    
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
        G = Graph()

        student_neighbors = self._student_neighbors()

        for student, neighbors in student_neighbors.items():
            student_node = student_prefix+str(student)
            G.add_node(student_node, category='student')

            for neighbor in neighbors:
                question_node = question_prefix+str(neighbor)
                G.add_node(question_node, category='question')

                G.add_edge(student_node,
                            question_node,
                            )

        return G