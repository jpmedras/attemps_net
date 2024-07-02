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
        'std_n_right_questions': [],
        'mean_n_submissions': [],
        'std_n_submissions': [],
        'n_students_right': [],
        'n_submissions_right': [],
        'p_submissions_right': [],
        'mean_mean_question_times': [],
        'std_mean_question_times': []
    }

    for name, group in grouped:
        data["community"].append(name)

        data["n_students"].append(len(group))

        students = [student for student in group.index]
        data["student_ids"].append(students)

        n_right_questions = [len(question_ids) for question_ids in group['question_ids'] if len(question_ids) > 0]
        data["std_n_right_questions"].append(std(n_right_questions))

        n_submissions = [len(submission_types) for submission_types in group['submission_types']]
        data["mean_n_submissions"].append(mean(n_submissions))
        data["std_n_submissions"].append(std(n_submissions))
        
        n_right_questions = [len(question_ids) for question_ids in group['question_ids']]
        n_right_questions_not_zero = [n for n in n_right_questions if n > 0]
        data["n_students_right"].append(len(n_right_questions_not_zero))

        submission_types_ = [submission_types for submission_types in group['submission_types'] if 1 in submission_types]
        n_submissions_ = sum([len(types) for types in submission_types_])
        n_right_submissions = sum([types.count(1) for types in submission_types_])

        if len(submission_types_) > 0:
            data['n_submissions_right'].append(n_right_submissions/len(submission_types_))
        else:
            data['n_submissions_right'].append(None)
        
        if n_submissions_ > 0:
            p_submissions_right = n_right_submissions/n_submissions_
            data['p_submissions_right'].append(f"{(100*p_submissions_right):.2f}")
        else:
            data['p_submissions_right'].append(None)

        mean_question_times = [(mean(question_times) if len(question_times) > 0 else None) for question_times in group['question_times']]
        mean_question_times_ = [mean_times for mean_times in mean_question_times if mean_times is not None]
        if len(mean_question_times_) > 0:
            data["mean_mean_question_times"].append(mean(mean_question_times_))
            data["std_mean_question_times"].append(std(mean_question_times_))
        else:
            data["mean_mean_question_times"].append(None)
            data["std_mean_question_times"].append(None)

    df = pd.DataFrame(data)
    df = df.set_index('community')

    return df