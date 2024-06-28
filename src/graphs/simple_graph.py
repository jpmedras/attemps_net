from graphs.graph_abc import GraphABC
from networkx import Graph

class SimpleGraph(GraphABC):
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
        G = Graph()

        for s in self._submissions:
            student_node = student_prefix+str(s.student)
            question_node = question_prefix+str(s.question)

            G.add_node(student_node, **self._STUDENT_NODE_ARGS)
            G.add_node(question_node, **self._QUESTION_NODE_ARGS)

            G.add_edge(student_node,
                        question_node,
                        color='green' if s.result else 'red',
                        sign='+' if s.result else '-',
                        time=s.time,
                        label=f'{s.time}')

        return G