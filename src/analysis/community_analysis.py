from typing import List, Set, Any
from dataclasses import make_dataclass
from numpy import mean, std
import pandas as pd
from .deal_comunities import group_communities

StudentClass = make_dataclass("Student", [("student_id", any), ("question_ids", list), ("question_times", list), ("submission_types", list)])
    
def community_questions(students_data:pd.DataFrame, communities:List[Set[Any]]):
    grouped = group_communities(students_data, communities)

    data = {
        'community': [],
        'n_students': [],
        'student_ids': [],
        'question_ids': [],
    }

    for name, group in grouped:
        data["community"].append(name)

        data["n_students"].append(len(group))
        
        students = [student for student in group.index]
        data["student_ids"].append(students)

        all_questions = set([question_id for question_ids in group['question_ids'] for question_id in question_ids])
        data["question_ids"].append(list(all_questions))

    df = pd.DataFrame(data)
    df = df.set_index('community')

    return df

# def caracterize_students(students_data:pd.DataFrame):
#     df = pd.DataFrame(index=students_data.index)
#     df['n_right_questions'] = students_data['question_ids'].apply(lambda question_ids: len(question_ids))
#     df['n_submissions'] = students_data['submission_types'].apply(lambda submission_types: len(submission_types))
#     df['n_wrong'] = students_data['submission_types'].apply(lambda submission_types: len([submission for submission in submission_types if submission == 0]))
#     df['n_right'] = students_data['submission_types'].apply(lambda submission_types: len([submission for submission in submission_types if submission == 1]))
#     df['mean_question_times'] = students_data['question_times'].apply(lambda x: (sum(x) / len(x)) if len(x) > 0 else None)

#     return df

def caracterize_communities(students_data:pd.DataFrame, communities:List[Set[Any]]):
    grouped = group_communities(students_data, communities)

    data = {
        'community': [],
        'n_students': [],
        'student_ids': [],
        'mean_n_right_questions': [],
        'std_n_right_questions': [],
        'mean_n_submissions': [],
        'std_n_submissions': [],
        'mean_n_right': [],
        'std_n_right': [],
        'mean_n_wrong': [],
        'std_n_wrong': [],
        'mean_mean_question_times': [],
        'std_mean_question_times': []
    }

    for name, group in grouped:
        data["community"].append(name)

        data["n_students"].append(len(group))

        students = [student for student in group.index]
        data["student_ids"].append(students)

        n_right_questions = [len(question_ids) for question_ids in group['question_ids']]
        data["mean_n_right_questions"].append(mean(n_right_questions))
        data["std_n_right_questions"].append(std(n_right_questions))

        n_submissions = [len(submission_types) for submission_types in group['submission_types']]
        data["mean_n_submissions"].append(mean(n_submissions))
        data["std_n_submissions"].append(std(n_submissions))

        n_right = [submission_types.count(1) for submission_types in group['submission_types']]
        data["mean_n_right"].append(mean(n_right))
        data["std_n_right"].append(std(n_right))

        n_wrong = [submission_types.count(0) for submission_types in group['submission_types']]
        data["mean_n_wrong"].append(mean(n_wrong))
        data["std_n_wrong"].append(std(n_wrong))

        if 0 in n_right_questions:
            data["mean_mean_question_times"].append(None)
            data["std_mean_question_times"].append(None)
        else:
            mean_times = [mean(question_times) for question_times in group['question_times']]
            data["mean_mean_question_times"].append(mean(mean_times))
            data["std_mean_question_times"].append(std(mean_times))        

    df = pd.DataFrame(data)
    df = df.set_index('community')

    return df