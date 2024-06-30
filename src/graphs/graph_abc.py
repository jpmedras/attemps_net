from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Union
from submissions.submission import Submission
from pygraphviz import AGraph
from networkx import Graph, MultiGraph

class GraphABC(ABC):
    def __init__(self, submissions:List[Submission]=None) -> None:
        self._submissions = submissions

    @abstractmethod
    def to_graph(self) -> Union[AGraph, Graph, MultiGraph]:
        pass