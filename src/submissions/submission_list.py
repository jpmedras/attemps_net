from collections.abc import MutableSequence
from typing import List
from .submission import Submission
import json
from datetime import datetime, timedelta
from pandas import DataFrame

class SubmissionList(MutableSequence):
    def __init__(self, submissions: List[Submission] = None, clean: bool = True, spent: bool = True) -> None:
        """
        Classe para manipular submissões, uma coleção de submissões. Ela permite limpar e computar valores úteis a partir dos dados.

        Argumentos:
        ---
        submissions: uma `list` com elementos do tipo `Submission` (uma lista de submissões).
        clean: define se as submissões serão "limpas". Se um estudante já resolveu um exercício, qualquer submissão nesse mesmo exercício enviada depois da primeira correta será ignorada.
        spent: define se o tempo gasto de cada submissão será computado. O tempo gasto é considerado como a diferença entre o tempo da submissão atual e da última, dentro do mesmo dia. Caso não hajam submissões anteriores no mesmo dia, considera-se o tempo desde o início.
        """

        if submissions is None:
            submissions = []

            clean = False
            spent = False
        
        if clean:
            submissions = self._clean(submissions)

        if spent:
            submissions = self._compute_lesson(submissions)
            submissions = self._compute_spent_time(submissions)
            
        self._submissions = sorted(submissions)
        
    def _clean(self, submissions) -> List[Submission]:
        """
        Limpa as submissões removendo aquelas que seguem a seguinte regra: caso um estudante já tenha resolvido um exercício (tenha ao menos uma submissão correta), qualquer submissão depois da primeira correta deve ser ignorada.
        """
        cleaned_submissions = []

        solved_exercises = {}
        for submission in submissions:
            if submission.student_id not in solved_exercises:
                solved_exercises[submission.student_id] = set()

            if submission.exercise_id not in solved_exercises[submission.student_id]:
                cleaned_submissions.append(submission)

            if submission.correct:
                solved_exercises[submission.student_id].add(submission.exercise_id)

        return sorted(cleaned_submissions)
    
    def _compute_lesson(self, submissions: List[Submission], days: int = 1) -> List[Submission]:
        """
        Computa o dia da submissão considerando as submissões do mesmo arquivo. Considera-se como dia, uma aula ou atividade. Caso o intervalo entre as submissões no arquivo seja maior ou igual ao definido, as submissões são classificadas como de dias diferentes.
        """
        computed_submissions = []
        
        it1 = iter(submissions)
        it2 = iter(submissions)
        next(it2)
        
        lesson_id = 0
        
        while ((submission := next(it1, None)) is not None) and ((submission_next := next(it2, None)) is not None):
            submission.lesson_id = lesson_id
            computed_submissions.append(submission)
            
            time = datetime.fromtimestamp(submission.timestamp)
            time_next = datetime.fromtimestamp(submission_next.timestamp)

            long_time = abs(time_next - time) > timedelta(days=days)

            if long_time:
                lesson_id += 1
                    
        submission.lesson_id = lesson_id
        computed_submissions.append(submission)
                        
        return sorted(computed_submissions)
    
    def _compute_spent_time(self, submissions: List[Submission]) -> List[Submission]:
        """
        Computa o tempo gasto para uma submissão. Para um mesmo dia, considera-se como tempo gasto, o intervalo entre uma submissão e a imediatamente anterior, se houver. Em caso de não haver submissões anteriores, considera-se o tempo gasto como o tempo desde o início.
        """
        computed_submissions = []

        grouped = {}
        for submission in submissions:
            if submission.student_id not in grouped:
                grouped[submission.student_id] = []
            
            grouped[submission.student_id].append(submission)


        for _, submissions in grouped.items():
            it1 = iter(submissions)
            it2 = iter(submissions)

            submission = next(it2)
            submission.spent_time = submission.beginning_timestamp_diff
            computed_submissions.append(submission)

            while ((submission_prev := next(it1, None)) is not None) and ((submission := next(it2, None)) is not None):
                changed_day = (submission_prev.lesson_id < submission.lesson_id)

                if changed_day:
                    submission.spent_time = submission.beginning_timestamp_diff
                else:
                    submission.spent_time = submission.beginning_timestamp_diff - submission_prev.beginning_timestamp_diff

                computed_submissions.append(submission)

        return sorted(computed_submissions)

    @classmethod
    def from_json(cls, filepath: str, student_prefix: str = None, exercise_prefix: str = None) -> None:
        """
        Extrai uma lista de submissões a partir de um arquivo JSON.
        """
        with open(filepath, 'r') as file:
            content = json.load(file)

        submissions = []
        for submission_dict in content:

            student_id = submission_dict['student_id']
            if student_prefix is not None:
                student_id = student_prefix + str(student_id)

            exercise_id = submission_dict['question_id']
            if exercise_prefix is not None:
                exercise_id = exercise_prefix + str(exercise_id)

            result = submission_dict['result']

            timestamp = submission_dict['timestamp']

            beginning_timestamp_diff = submission_dict['diff_from_start']

            submission = Submission(
                student_id=student_id,
                exercise_id=exercise_id,
                result=result,
                timestamp=timestamp,
                beginning_timestamp_diff=beginning_timestamp_diff
            )
            submissions.append(submission)

        return cls(submissions)
        
    def __str__(self) -> str:
        return f"{[str(submission) for submission in self._submissions]}"

    def __repr__(self) -> str:
        return f"SubmissionList({[submission for submission in self._submissions]})"
    
    def __iter__(self):
        return iter(self._submissions)
    
    def __getitem__(self, key:int) -> Submission:
        return self._submissions[key]
    
    def __setitem__(self, key:int, elem:Submission) -> None:
        self._submissions[key] = elem
        
        self._submissions = sorted(self._submissions)

    def __delitem__(self, key:int) -> None:
        del self._submissions[key]
        
    def __len__(self) -> int:
        return len(self._submissions)
        
    def append(self, elem:Submission) -> None:
        self._submissions.append(elem)

    def insert(self, index:int, elem:Submission) -> None:
        self._submissions.insert(index, elem)
        
        self._submissions = sorted(self._submissions)

    def __add__(self, other:"SubmissionList") -> "SubmissionList":
        return SubmissionList(self._submissions + other._submissions, clean=False, spent=False)
    
    def to_df(self):
        d = [submission.to_series() for submission in self._submissions]
        
        df = DataFrame(d)

        return df