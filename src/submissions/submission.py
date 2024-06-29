from typing import Any

class Submission:
    def __init__(self, student:Any, question:Any, result:int, timestamp:int, time:int) -> None:
        self._student = student
        self._question = question
        self._result = result == 1
        self._timestamp = timestamp
        self._time = time
        self._spent = None

    @property
    def student(self) -> Any:
        return self._student
    
    @property
    def question(self) -> Any:
        return self._question
    
    @property
    def result(self) -> bool:
        return self._result
    
    @property
    def timestamp(self) -> int:
        return self._timestamp
    
    @property
    def time(self) -> int:
        return self._time
    
    @property
    def spent(self) -> int:
        return self._spent
    
    @spent.setter
    def spent(self, value:int) -> int:
        self._spent = value
    
    def __repr__(self) -> str:
        return f"Submission({self.student}, {self.question}, {int(self.result)}, {self.timestamp}, {self.time})"
    
    def __lt__(self, other) -> bool:
        return (self.timestamp < other.timestamp)