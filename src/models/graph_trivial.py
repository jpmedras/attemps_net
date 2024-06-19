from models.graph_abc import GraphABC
from networkx import MultiGraph

class GraphTrivial(GraphABC):
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> MultiGraph:
        g = MultiGraph()

        for s in self._subs:
            student_node = student_prefix+str(s.student)
            question_node = question_prefix+str(s.question)

            g.add_node(student_node, **self._student_node_args)
            g.add_node(question_node, **self._question_node_args)

            g.add_edge(student_node,
                       question_node,
                       color='green' if s.result else 'red',
                       sign='+' if s.result else '-',
                       time=s.time,
                       label=f'{str(s.result)}, {s.time}')

        return g