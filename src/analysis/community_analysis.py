from typing import List, Set, Any
import pandas as pd

def caracterize_community(students_data:pd.DataFrame, communities:List[Set[Any]]):
    new_df = pd.DataFrame(index=students_data.index)

    new_df['n_right_questions'] = students_data['question_ids'].apply(lambda question_ids: len(question_ids))
    new_df['n_submissions'] = students_data['submission_types'].apply(lambda submission_types: len(submission_types))
    new_df['n_wrong'] = students_data['submission_types'].apply(lambda submission_types: len([submission for submission in submission_types if submission == 0]))
    new_df['n_right'] = students_data['submission_types'].apply(lambda submission_types: len([submission for submission in submission_types if submission == 1]))
    new_df['mean_question_times'] = students_data['question_times'].apply(lambda x: (sum(x) / len(x)) if len(x) > 0 else None)

    idx_communities = {}
    for idx, community in enumerate(communities):
        idx_communities[idx] = list(community)

    student_communities = {}
    for community in idx_communities:
        for student in idx_communities[community]:
            student_communities[student] = community

    column = [student_communities[student] for student in students_data.index]

    new_df['community'] = column

    grouped = new_df.groupby('community')
    mean_df = grouped.mean()
    std_df = grouped.std()

    # Contando o número de elementos (alunos) em cada comunidade
    n_elements = grouped.size()

    # Inserindo as colunas 'n_elements', 'std' (desvio padrão) no DataFrame de médias
    mean_df.insert(0, 'n_elements', n_elements)

    for pos, column in enumerate(std_df.columns):
        mean_df.insert(2*(pos+1), 'std_'+column, std_df[column])

    return mean_df