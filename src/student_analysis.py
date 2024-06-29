from graphs.students_graph import StudentsGraph
from networkx import write_gexf
from networkx import set_node_attributes
from networkx.algorithms.community import louvain_communities
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import make_dataclass
from analysis import caracterize_community
from submissions import SubmissionList

def analysis(file_path, communities):
    Student = make_dataclass("Student", [("student_id", any), ("question_ids", list), ("question_times", list), ("submission_types", list)])
    
    submissions = SubmissionList.from_json(file_path)

    student_questions = submissions.student_questions()
    student_question_times = submissions.student_question_times()
    student_submission_types = submissions.student_submission_types()

    students = []
    for student in submissions.students:
        student_obj = Student(
            student,
            student_questions[student],
            [student_question_times[student][question] for question in student_questions[student]],
            student_submission_types[student]
        )
        students.append(student_obj)

    df = pd.DataFrame(students)
    df = df.set_index('student_id')

    analysis_df = caracterize_community(students_data=df, communities=communities)

    return analysis_df

if __name__ == '__main__':
    # YEARS = [2018, 2019, 2021, 2022, 2023]
    YEARS = [2018]
    OUTPUT_PATH = 'assets/'

    for year in YEARS:
        file_path = 'private_data/by_year/' + str(year) + '.json'
        graph_path = OUTPUT_PATH + 'students/' + str(year) + '/' + str(year) + '.gexf'
        analysis_path = OUTPUT_PATH + 'students/' + str(year) + '/' + 'analysis_' + str(year) + '.csv'

        graph = StudentsGraph.from_json(file_path)
        G = graph.to_graph()

        communities = louvain_communities(G, seed=42, weight='weight')

        community_attr = {}
        for idx, community in enumerate(communities):
            for node in community:
                community_attr[node] = {
                    'community': idx
                }

        set_node_attributes(G, community_attr)

        print(G)
        write_gexf(G, graph_path)

        analysis_df = analysis(file_path, communities)
        print(analysis_df)