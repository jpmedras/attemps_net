from graphs.graph_abc import GraphABC
from pygraphviz import AGraph

class MultiGraph(GraphABC):
    _QUESTION_NODE_ARGS = {
        'shape':'box',
        'fontcolor':'white',
        'style':'filled',
        'fillcolor':'black'
    }

    _STUDENT_NODE_ARGS = {
        'shape': 'circle',
    }
    
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> AGraph:
        G = AGraph(strict=False, directed=True)

        for submission in self._submissions:
            student_node = student_prefix+str(submission.student)
            question_node = question_prefix+str(submission.question)

            if not G.has_node(student_node):
                G.add_node(student_node, **self._STUDENT_NODE_ARGS)

            if not G.has_node(question_node):
                G.add_node(question_node, **self._QUESTION_NODE_ARGS)

            G.add_edge(student_node,
                        question_node,
                        color='green' if submission.result else 'red',
                        sign='+' if submission.result else '-',
                        label=f'{submission.spent}')

        return G