from models.graph_abc import GraphABC
from networkx import Graph

class GraphStudents(GraphABC):
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
        g = Graph()

        student_questions = {}

        for s in self._subs:
            if s.student not in student_questions:
                student_questions[s.student] = []
            
            if s.result:
                student_questions[s.student].append(s.question)
        
        for student_u in student_questions:
            student_node_u = student_prefix + str(student_u)

            for student_v in student_questions:
                student_node_v = student_prefix + str(student_v)
                
                if student_u != student_v:
                    weight = len(set(student_questions[student_u]) & set(student_questions[student_v]))

                    if not g.has_node(student_node_u):
                        g.add_node(student_node_u, Size=len(student_questions[student_u]))

                    if not g.has_node(student_node_v):
                        g.add_node(student_node_v, Size=len(student_questions[student_v]))

                    if weight > 0 and not g.has_edge(student_node_u, student_node_v):
                        g.add_edge(student_node_u,
                                student_node_v,
                                Label=f'{weight}')
                    
        return g