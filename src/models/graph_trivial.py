from models.graph_abc import GraphABC
from networkx import MultiGraph

class GraphTrivial(GraphABC):
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> MultiGraph:
        g = MultiGraph()

        for s in self._subs:
            student_node = student_prefix+str(s.student)
            question_node = question_prefix+str(s.question)

            g.add_node(student_node, shape='circle')
            g.add_node(question_node, shape='box', style='filled', fillcolor='red')

            g.add_edge(student_node,
                       question_node,
                       sign='+' if s.result else '-',
                       time=s.time,
                       label=f'{str(s.result)}, {s.time}')

        return g