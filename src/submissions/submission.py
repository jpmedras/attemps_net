from typing import Any
from pandas import Series

class Submission:
    def __init__(self, student_id:Any, exercise_id:Any, result:int, timestamp:int, beginning_timestamp_diff:int) -> None:
        self._student_id = student_id
        self._exercise_id = exercise_id
        self._correct = (result == 1)
        self._timestamp = timestamp
        self._beginning_timestamp_diff = beginning_timestamp_diff

    def __str__(self) -> str:
        return f"{self.student_id}->{self.exercise_id}: {self.correct} ({self.spent_time} | {self.beginning_timestamp_diff}) [{self.lesson_id} : {self.timestamp}]"

    def __repr__(self) -> str:
        return f"Submission({self.student_id}, {self.exercise_id}, {int(self.correct)}, {self.timestamp}, {self.beginning_timestamp_diff})"

    @property
    def student_id(self) -> Any:
        return self._student_id
    
    @property
    def exercise_id(self) -> Any:
        return self._exercise_id
    
    @property
    def correct(self) -> bool:
        return self._correct
    
    @property
    def timestamp(self) -> int:
        return self._timestamp
    
    @property
    def beginning_timestamp_diff(self) -> int:
        return self._beginning_timestamp_diff
    
    @property
    def lesson_id(self) -> int:
        return self._lesson_id
    
    @lesson_id.setter
    def lesson_id(self, value:int):
        self._lesson_id = value
    
    @property
    def spent_time(self) -> int:
        return self._spent_time
    
    @spent_time.setter
    def spent_time(self, value:int):
        self._spent_time = value
    
    def __lt__(self, other:"Submission") -> bool:      
        return ((self.timestamp) < (other.timestamp))
    
    def __eq__(self, other:"Submission") -> bool:
        return ((self.timestamp) == (other.timestamp))
    
    def to_series(self) -> Series:
        d = {
            'timestamp': self.timestamp,
            'student_id': self.student_id,
            'exercise_id': self.exercise_id,
            'correct': self.correct,
            'beginning_timestamp_diff': self.beginning_timestamp_diff,
            'lesson_id': self.lesson_id
        }
        
        return Series(d)