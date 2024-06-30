from graphs import StudentsGraph
from networkx import write_gexf
from networkx import set_node_attributes
from networkx.algorithms.community import louvain_communities
import pandas as pd
from analysis import StudentClass, caracterize_community
from submissions import SubmissionList

def get_data_analysis(submissions, communities):    
    student_questions = submissions.student_questions()
    student_question_times = submissions.student_question_times()
    student_submission_types = submissions.student_submission_types()

    students = []
    for student_id in submissions.get_students():
        question_ids = student_questions[student_id]
        question_times = [student_question_times[student_id][question] for question in student_questions[student_id]]
        submission_types = student_submission_types[student_id]

        student_obj = StudentClass(
            student_id,
            question_ids,
            question_times,
            submission_types
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

        submissions = SubmissionList.from_json(file_path)
        graph = StudentsGraph(submissions)
        G = graph.to_graph()

        communities = louvain_communities(G, seed=42, weight='weight')

        community_attr = {}
        for idx, community in enumerate(communities):
            for node in community:
                community_attr[node] = {
                    'community': idx
                }

        set_node_attributes(G, community_attr)

        print(f'{year}:', G)
        write_gexf(G, graph_path)

        analysis_df = get_data_analysis(submissions, communities)
        analysis_df.to_csv(analysis_path, decimal=',')