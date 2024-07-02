from graphs import StudentsGraph, SimpleGraph
from networkx import write_gexf
from networkx import set_node_attributes
from networkx.algorithms.community import louvain_communities, modularity
import pandas as pd
import numpy as np
from analysis import StudentClass, caracterize_communities, community_questions
from submissions import SubmissionList

def get_data_analysis(submissions):    
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

    return df

def find_k(submissions):
    criterion = {}

    for k in np.arange(0.0, 0.95, 0.05):
        graph = StudentsGraph(submissions, k=k)
        G = graph.to_graph()

        communities = louvain_communities(G, seed=42, weight='weight')

        student_data = get_data_analysis(submissions)
        analysis_df = caracterize_communities(student_data, communities)

        criterion[k] = (analysis_df['std_n_right_questions'] * analysis_df['n_students']).sum() / analysis_df['n_students'].sum()

    min_k = min(criterion, key=criterion.get)

    print(criterion[0.0], criterion[min_k])

    return min_k

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    # YEARS = [2018]
    OUTPUT_PATH = 'assets/'

    compare_data = {
        'year': [],
        'n_nodes': [],
        'n_edges_no_k': [],
        'n_edges_with_k': [],
        'modularity_no_k': [],
        'modularity_with_k': [],
    }
    COMPARE_PATH = OUTPUT_PATH + 'students/compare_graphs.csv'

    simple_data = {
        'year': [],
        'n_students': [],
        'n_questions': [],
        'n_edges': [],
    }
    SIMPLE_PATH = OUTPUT_PATH + 'students/simple_graph.csv'

    for year in YEARS:
        FILE_PATH = 'private_data/by_year/' + str(year) + '.json'
        GRAPH_PATH = OUTPUT_PATH + 'students/' + str(year) + '/' + str(year) + '.gexf'
        GRAPH_T_PATH = OUTPUT_PATH + 'students/' + str(year) + '/' + str(year) + '_t' +'.gexf'
        SIMPLE_PATH = OUTPUT_PATH + 'students/' + str(year) + '/' + str(year) + '_simple' + '.gexf'
        ANALYSIS_PATH = OUTPUT_PATH + 'students/' + str(year) + '/' + 'analysis_' + str(year) + '.csv'
        QUESTIONS_PATH = OUTPUT_PATH + 'students/' + str(year) + '/' + 'questions_' + str(year) + '.csv'
        ANALY_SIMPLE_PATH = OUTPUT_PATH + 'students/' + str(year) + '/' + 'simple_' + str(year) + '.csv'

        submissions = SubmissionList.from_json(FILE_PATH)

        graph_simple = SimpleGraph(submissions)
        one_simple_g = graph_simple.to_graph()
        write_gexf(one_simple_g, SIMPLE_PATH)

        simple_data["year"].append(year)
        simple_data["n_students"].append(len([node for node, data in one_simple_g.nodes(data=True) if data['category'] == 'student']))
        simple_data["n_questions"].append(len([node for node, data in one_simple_g.nodes(data=True) if data['category'] == 'question']))
        simple_data["n_edges"].append(len(one_simple_g.edges))

        graph_no_k = StudentsGraph(submissions)
        G_no_k = graph_no_k.to_graph()
        communities_no_k = louvain_communities(G_no_k, seed=42, weight='weight')
        modularity_no_k = modularity(G_no_k, communities=communities_no_k)

        community_no_k_attr = {}
        for idx, community in enumerate(communities_no_k):
            for node in community:
                community_no_k_attr[node] = {
                    'community': idx
                }

        set_node_attributes(G_no_k, community_no_k_attr)

        k = find_k(submissions)
        print('k =', k)

        graph = StudentsGraph(submissions, k)
        G_with_k = graph.to_graph()
        communities_with_k = louvain_communities(G_with_k, seed=42, weight='weight')
        modularity_with_k = modularity(G_with_k, communities=communities_with_k)

        community_attr = {}
        for idx, community in enumerate(communities_with_k):
            for node in community:
                community_attr[node] = {
                    'community': idx
                }

        set_node_attributes(G_with_k, community_attr)

        print(G_no_k)
        print(G_with_k)

        write_gexf(G_no_k, GRAPH_T_PATH)
        write_gexf(G_with_k, GRAPH_PATH)

        compare_data['year'].append(year)
        compare_data['n_nodes'].append(len(G_no_k.nodes))
        compare_data['n_edges_no_k'].append(len(G_no_k.edges))
        compare_data['n_edges_with_k'].append(f"{len(G_with_k.edges)} ({100*(len(G_with_k.edges)/len(G_no_k.edges)):.2f})")
        compare_data['modularity_no_k'].append(f"{modularity_no_k:.2f}")
        compare_data['modularity_with_k'].append(f"{modularity_with_k:.2f}")

        student_data = get_data_analysis(submissions)

        analysis_df = caracterize_communities(student_data, communities_with_k)
        analysis_df.to_csv(ANALYSIS_PATH)

        question_df = community_questions(student_data, communities_with_k)
        question_df.to_csv(QUESTIONS_PATH)

        print()

    df_simple = pd.DataFrame(simple_data)
    df_simple.to_csv(ANALY_SIMPLE_PATH, index=False, decimal=',')

    df = pd.DataFrame(compare_data)
    df.to_csv(COMPARE_PATH, index=False, decimal=',')