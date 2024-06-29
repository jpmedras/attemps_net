from typing import List, Set, Any
import pandas as pd

def caracterize_community(students_data:pd.DataFrame, communities:List[Set[Any]]):
    students_data['n_questions'] = students_data['question_ids'].apply(lambda question_ids: len(question_ids))
    students_data['n_submissions'] = students_data['submission_types'].apply(lambda submission_types: len(submission_types))
    students_data['n_wrong'] = students_data['submission_types'].apply(lambda submission_types: len([submission for submission in submission_types if submission == 0]))
    students_data['n_right'] = students_data['submission_types'].apply(lambda submission_types: len([submission for submission in submission_types if submission == 1]))
    students_data['mean_question_times'] = students_data['question_times'].apply(lambda x: (sum(x) / len(x)) if len(x) > 0 else None)

    idx_communities = {}
    for idx, community in enumerate(communities):
        idx_communities[idx] = list(community)

    student_communities = {}
    for community in idx_communities:
        for student in idx_communities[community]:
            student_communities[student] = community

    for index in students_data.index:
        print(index)