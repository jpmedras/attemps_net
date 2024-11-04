from graphs import StudentsGraph
from networkx import write_gexf
from networkx import set_node_attributes
from networkx.algorithms.community import louvain_communities, modularity
from pandas import DataFrame, read_csv
import numpy as np
from analysis import StudentClass, caracterize_communities
from typing import List, Set

def group_singleton_communities(communities:List[Set[int]]) -> List[Set[int]]:
    singleton_community = set()
    new_communities = []

    for community in communities:
        if len(community) == 1:
            singleton_community.update(community)
        else:
            new_communities.append(community)

    # for student_id in student_ids:
    #     has_community = False

    #     for community in communities:
    #         if student_id in community:
    #             has_community = True
    #             break

    #     if not has_community:        
    #         singletons_community.add(student_id)

    if len(singleton_community) > 0:
        new_communities = new_communities + [singleton_community]

    return new_communities

def students_analysis(attemps:DataFrame, communities:list) -> DataFrame:
    students = []
    for student_id, group in attemps.groupby("student_id"):
        solving_times = DataFrame((
            group[group["is_correct"] == True]
            .groupby("exercise_id")["spent_time"]
            .sum()
            .rename("solving_time")
        ))
        exercise_ids = solving_times.index.tolist()
        times = solving_times['solving_time'].tolist()
        results = group['is_correct'].tolist()

        student_obj = StudentClass(
            student_id,
            exercise_ids,
            times,
            results
        )
        students.append(student_obj)

    df = DataFrame(students)
    df = df.set_index('student_id')

    new_communities = group_singleton_communities(communities)

    community_column = []
    for student_id in df.index:
        for idx, community in enumerate(new_communities):
            if student_id in community:
                community_column.append(idx)
                break

    assert len(community_column) == len(df.index), "student_id com nenhuma comunidade correspondente"

    df['community'] = community_column

    return df

def find_filtering_parameter(attemps:DataFrame):
    criterions = {}

    for k in np.arange(0.0, 0.95, 0.05):
        graph = StudentsGraph(attemps=attemps, k=k).graph

        communities = louvain_communities(graph, seed=42, weight='weight')

        students_analysis_df = students_analysis(attemps=attemps, communities=communities)
        communities_analysis_df = caracterize_communities(students_analysis_df)

        # print(students_analysis_df)
        # print(communities_analysis_df)

        criterion = (communities_analysis_df['std_ns_correct_exercises'] * communities_analysis_df['n_students']).sum() / communities_analysis_df['n_students'].sum()
        criterions[k] = criterion

    parameter = min(criterions, key=criterions.get)

    # print(criterions[0.0], criterions[parameter])

    return parameter

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    DATA_PATH = 'data/'
    INPUT_PATH = DATA_PATH + 'attemps/'
    ANALYSIS_OUTPUT_PATH = DATA_PATH + 'analysis/'
    GRAPHS_OUTPUT_PATH = DATA_PATH + 'graphs/'

    compare_graphs_data = {
        'year': [],
        'n_nodes': [],
        'n_edges': [],
        'n_edges_filtered_graph': [],
        'modularity': [],
        'modularity_filtered_graph': [],
    }

    attemps_metrics_data = {
        'year': [],
        'n_students': [],
        'n_exercises': [],
        'n_attemps': [],
    }

    for year in YEARS:
        # ATTEMPS METRICS
        attemps_filepath = INPUT_PATH + 'attemps' + '_' + str(year) + '_' + '3' + '.csv'

        attemps = read_csv(attemps_filepath)

        attemps_metrics_data['year'].append(year)
        attemps_metrics_data['n_students'].append(len(attemps['student_id'].unique().tolist()))
        attemps_metrics_data['n_exercises'].append(len(attemps['exercise_id'].unique().tolist()))
        attemps_metrics_data['n_attemps'].append(len(attemps.index))

        # STUDENTS GRAPH 
        # grafo onde nós são os estudantes e as arestas representam quantas quesões tem em comum
        students_graph_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'students_graph' + '.gexf'
        students_graph = StudentsGraph(attemps=attemps).graph
        students_graph_communities = louvain_communities(students_graph, seed=42, weight='weight')
        students_graph_grouped_communities = group_singleton_communities(students_graph_communities)
        students_graph_modularity = modularity(students_graph, communities=students_graph_grouped_communities)

        # adicionando atributo aos nós com a comunidade
        students_graph_attr = {}
        for idx, community in enumerate(students_graph_grouped_communities):
            for node in community:
                students_graph_attr[node] = {
                    'community': idx
                }
        set_node_attributes(students_graph, students_graph_attr)

        # salvando graph
        write_gexf(students_graph, students_graph_filepath)
       
        filtering_parameter = find_filtering_parameter(attemps)
        print('k =', filtering_parameter)

        students_filtered_graph_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'students_filtered_graph' + '.gexf'
        students_filtered_graph = StudentsGraph(attemps, k=filtering_parameter).graph
        students_filtered_graph_communities = louvain_communities(students_filtered_graph, seed=42, weight='weight')
        students_filtered_graph_grouped_communities = group_singleton_communities(students_filtered_graph_communities)
        students_filtered_graph_modularity = modularity(students_filtered_graph, communities=students_filtered_graph_grouped_communities)

        students_filtered_graph_attr = {}
        for idx, community in enumerate(students_filtered_graph_grouped_communities):
            for node in community:
                students_filtered_graph_attr[node] = {
                    'community': idx
                }


        set_node_attributes(students_filtered_graph, students_filtered_graph_attr)

        # salvando graph
        write_gexf(students_filtered_graph, students_filtered_graph_filepath)

        assert len(students_graph.nodes) == len(students_filtered_graph.nodes), "Número de nodes errado"
       
        compare_graphs_data['year'].append(year)
        compare_graphs_data['n_nodes'].append(len(students_graph.nodes))
        compare_graphs_data['n_edges'].append(len(students_graph.edges))
        compare_graphs_data['n_edges_filtered_graph'].append(len(students_filtered_graph.edges))
        compare_graphs_data['modularity'].append(students_graph_modularity)
        compare_graphs_data['modularity_filtered_graph'].append(students_filtered_graph_modularity)


        students_analysis_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'students_analysis' + '.csv'
        students_analysis_df = students_analysis(attemps=attemps, communities=students_filtered_graph_grouped_communities)
        students_analysis_df.to_csv(students_analysis_filepath, decimal=',')

        communities_analysis_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'communities_analysis' + '.csv'
        communities_analysis_df = caracterize_communities(students_analysis_df)
        communities_analysis_df.to_csv(communities_analysis_filepath, decimal=',')

        print()

    compare_graphs_filepath = ANALYSIS_OUTPUT_PATH + 'compare_graphs.csv'
    compare_graphs_df = DataFrame(compare_graphs_data)
    compare_graphs_df.to_csv(compare_graphs_filepath, index=False, decimal=',')

    attemps_metrics_filepath = ANALYSIS_OUTPUT_PATH + 'attemps_metrics.csv'
    attemps_metrics_df = DataFrame(attemps_metrics_data)
    attemps_metrics_df.to_csv(attemps_metrics_filepath, index=False, decimal=',')