from typing import List
from .submission import Submission
from _collections_abc import list_iterator
import json
from datetime import datetime, timedelta
from typing import Dict, Set, Any

class SubmissionList:
    def __init__(self, submissions:List[Submission], clean=True, compute_spent=True) -> None:
        self._submissions = submissions

        self._submissions.sort()

        if clean:
            self._clean()

        if compute_spent:
            self._compute_spent()

    @classmethod
    def from_json(cls, json_file:str) -> 'SubmissionList':
        submissions = []

        with open(json_file) as file:
            content = json.load(file)

        for s in content:
            submission = Submission(s['id_student'], s['id_question'], s['result'], s['timestamp'], s['time'])
            submissions.append(submission)

        return cls(submissions)
    
    def __len__(self) -> int:
        return len(self._submissions)
    
    def __iter__(self) -> list_iterator:
        return iter(self._submissions)
    
    def __getitem__(self, index) -> Submission:
        return self._submissions[index]
    
    def _clean(self) -> None:
        submissions = []

        student_questions = {}
        for submission in self._submissions:
            if submission.student not in student_questions:
                student_questions[submission.student] = set()

            if submission.question not in student_questions[submission.student]:
                submissions.append(submission)

            if submission.result:
                student_questions[submission.student].add(submission.question)

        self._submissions = submissions

    def _group_submissions(self) -> Dict[Any, 'SubmissionList']:
        grouped_ = {}
        for submission in self._submissions:
            if submission.student not in grouped_:
                grouped_[submission.student] = []
            
            grouped_[submission.student].append(submission)

        grouped = {}
        for student in grouped_:
            grouped[student] = SubmissionList(grouped_[student], clean=False, compute_spent=False)

        return grouped
    
    def _compute_spent(self) -> None:
        computed_submissions = []

        grouped = self._group_submissions()

        for _, submissions in grouped.items():
            it1 = iter(submissions)
            it2 = iter(submissions)

            submission = next(it2)
            submission.spent = submission.time
            computed_submissions.append(submission)

            while ((submission_prev := next(it1, None)) is not None) and ((submission := next(it2, None)) is not None):
                timestamp_prev = datetime.fromtimestamp(submission_prev.timestamp)
                timestamp = datetime.fromtimestamp(submission.timestamp)

                long_time = abs(timestamp - timestamp_prev) > timedelta(days=1)

                if long_time:
                    submission.spent = submission.time
                else:
                    submission.spent = submission.time - submission_prev.time

                computed_submissions.append(submission)

        computed_submissions.sort()

        self._submissions = computed_submissions

    def get_students(self) -> Set[Any]:
        return list(set([submission.student for submission in self._submissions]))
    
    def get_questions(self) -> Set[Any]:
        return list(set([submission.question for submission in self._submissions]))
    
    def student_questions(self) -> Dict[Any, Set[Any]]:
        data = {}

        for submission in self._submissions:
            if submission.student not in data:
                data[submission.student] = set()

            if submission.result:
                data[submission.student].add(submission.question)

        for student in data:
            data[student] = list(data[student])

        return data
    
    def student_question_times(self) -> Dict[Any, Dict[Any, int]]:
        data = {}

        grouped = self._group_submissions()
        student_questions = self.student_questions()

        for student, submissions in grouped.items():
            if student not in data:
                data[student] = {}
            
            for question in student_questions[student]:
                data[student][question] = 0

            for submission in submissions:
                if submission.question in data[student]:
                    data[student][submission.question] += submission.spent

        return data
    
    def student_submission_types(self) -> Dict[Any, Set[int]]:
        data = {}

        for submission in self._submissions:
            if submission.student not in data:
                data[submission.student] = []

            data[submission.student].append(int(submission.result))

        return data