from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Union
from submissions.submission import Submission
import json
from networkx import Graph, MultiGraph

class GraphABC(ABC):
    _QUESTION_NODE_ARGS = {
        'shape':'box',
        'fontcolor':'white',
        'style':'filled',
        'fillcolor':'black'
    }

    _STUDENT_NODE_ARGS = {
        'shape': 'circle',
    }

    def __init__(self, submissions:List[Submission]=None) -> None:
        self._submissions = submissions

    @abstractmethod
    def to_graph(self) -> Union[Graph, MultiGraph]:
        pass