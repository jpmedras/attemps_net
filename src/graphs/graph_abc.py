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
        self._submissions = []

        student_questions = {}
        for sub in submissions:
            if sub.student not in student_questions:
                student_questions[sub.student] = set()

            if sub.result:
                if sub.question not in student_questions[sub.student]:
                    self._submissions.append(sub)
                
                student_questions[sub.student].add(sub.question)
            else:
                self._submissions.append(sub)
        
        self._submissions.sort()

    @classmethod
    def from_json(cls, json_file:str) -> 'GraphABC':
        submissions = []

        with open(json_file) as file:
            content = json.load(file)

        for s in content:
            submission = Submission(s['id_student'], s['id_question'], s['result'], s['timestamp'], s['time'])
            submissions.append(submission)

        return cls(submissions)

    @abstractmethod
    def to_graph(self) -> Union[Graph, MultiGraph]:
        pass