from models.graph_abc import GraphABC
from networkx import Graph

class GraphQuestions(GraphABC):
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
        g = Graph()

        question_students = {}

        for s in self._subs:
            if s.question not in question_students:
                question_students[s.question] = []

            if s.result:
                question_students[s.question].append(s.student)
        
        for question_u in question_students:
            question_node_u = question_prefix + str(question_u)

            for question_v in question_students:
                question_node_v = question_prefix + str(question_v)
                
                if question_u != question_v:
                    weight = len(set(question_students[question_u]) & set(question_students[question_v]))

                    if not g.has_node(question_node_u):
                        g.add_node(question_node_u, size=len(question_students[question_u]))

                    if not g.has_node(question_node_v):
                        g.add_node(question_node_v, size=len(question_students[question_v]))

                    if weight > 0 and not g.has_edge(question_node_u, question_node_v):
                        g.add_edge(question_node_u,
                                question_node_v,
                                label=f'{weight}')
                    
        return g