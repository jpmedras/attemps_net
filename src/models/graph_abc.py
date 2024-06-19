from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Union
from models.submission import Submission
from networkx import Graph, MultiGraph

class GraphABC(ABC):
    _question_node_args = {
        'shape':'box',
        'fontcolor':'white',
        'style':'filled',
        'fillcolor':'black'
    }

    _student_node_args = {
        'shape': 'circle',
    }

    def __init__(self, submissions:List[Submission]=None) -> None:
        self._subs = []

        student_questions = {}
        for sub in submissions:
            if sub.student not in student_questions:
                student_questions[sub.student] = set()

            if sub.result:
                if sub.question not in student_questions[sub.student]:
                    self._subs.append(sub)
                
                student_questions[sub.student].add(sub.question)
            else:
                self._subs.append(sub)
        
        self._subs.sort()

    @abstractmethod
    def to_graph(self) -> Union[Graph, MultiGraph]:
        pass