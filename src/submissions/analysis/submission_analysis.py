from ..submission_list import SubmissionList
from typing import Any, List, Dict

def students_id(submissions:SubmissionList) -> List[Any]:
    return list(set([submission.student_id for submission in submissions]))

def exercises_id(submissions:SubmissionList) -> List[Any]:
    return list(set([submission.exercise_id for submission in submissions]))

def solved_exercises(submissions:SubmissionList) -> Dict[Any, List[int]]:
    grouped = {}
    for submission in submissions:
        if submission.student_id not in grouped:
            grouped[submission.student_id] = []
            
        if submission.correct and (submission.exercise_id not in grouped[submission.student_id]):
            grouped[submission.student_id].append(submission.exercise_id)

    return grouped
        
def tried_exercises(submissions:SubmissionList) -> Dict[Any, List[int]]:
    solved = solved_exercises(submissions=submissions)
    
    grouped = {}
    for submission in submissions:
        if submission.student_id not in grouped:
            grouped[submission.student_id] = []
            
        if (submission.exercise_id not in solved[submission.student_id]) and (submission.exercise_id not in grouped[submission.student_id]):
            grouped[submission.student_id].append(submission.exercise_id)
            
    return grouped

def student_submissions(submissions:SubmissionList) -> Dict[Any, SubmissionList]:
    grouped = {}
    for submission in submissions:
        if submission.student_id not in grouped:
            grouped[submission.student_id] = []
            
        grouped[submission.student_id].append(submission)
        
    for student in grouped:
        grouped[student] = SubmissionList(grouped[student], clean=False, spent=False)
        
    return grouped

def exercise_submissions(submissions:SubmissionList) -> Dict[Any, SubmissionList]:
    grouped = {}
    for submission in submissions:
        if submission.exercise_id not in grouped:
            grouped[submission.exercise_id] = []
            
        grouped[submission.exercise_id].append(submission)
        
    for exercise in grouped:
        grouped[exercise] = SubmissionList(grouped[exercise], clean=False, spent=False)
        
    return grouped

def lesson_submissions(submissions:SubmissionList) -> Dict[Any, SubmissionList]:
    grouped = {}
    for submission in submissions:
        if submission.lesson_id not in grouped:
            grouped[submission.lesson_id] = []
            
        grouped[submission.lesson_id].append(submission)
        
    for lesson in grouped:
        grouped[lesson] = SubmissionList(grouped[lesson], clean=False, spent=False)
        
    return grouped

def compute_time(submissions:SubmissionList) -> int:
    time = sum(submission.spent_time for submission in submissions)

    return time

def solving_times(submissions:SubmissionList) -> Dict[Any, Dict[Any, int]]:
    solved = solved_exercises(submissions=submissions)
    s_submissions = student_submissions(submissions=submissions)
    
    times = {}
    for student, exercises in solved.items():
        if (student not in times) and (len(exercises) > 0):
            times[student] = {}

        q_submissions = exercise_submissions(s_submissions[student])
        for exercise in exercises:
            time = compute_time(q_submissions[exercise])
            times[student][exercise] = time
            
    return times
    
def trying_times(submissions:SubmissionList) -> Dict[Any, Dict[Any, int]]:
    tried = tried_exercises(submissions=submissions)
    s_submissions = student_submissions(submissions=submissions)
    
    times = {}
    for student, exercises in tried.items():
        if (student not in times) and (len(exercises) > 0):
            times[student] = {}

        q_submissions = exercise_submissions(s_submissions[student])
        for exercise in exercises:
            time = compute_time(q_submissions[exercise])
            times[student][exercise] = time
            
    return times