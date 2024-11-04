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
        correct_exercise_ids = solving_times.index.tolist()
        s_times = solving_times['solving_time'].tolist()

        attemping_times = DataFrame((
            group[group["is_correct"] == False]
            .groupby("exercise_id")["spent_time"]
            .sum()
            .rename("attemping_time")
        ))
        attempted_exercise_ids = attemping_times.index.tolist()
        a_times = attemping_times['attemping_time'].tolist()

        results = group['is_correct'].tolist()

        student_obj = StudentClass(
            student_id,
            correct_exercise_ids,
            s_times,
            attempted_exercise_ids,
            a_times,
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

def find_filtering_parameter(attemps:DataFrame) -> DataFrame:
    data = {
        'filtering_parameter': [],
        'n_edges': [],
        'modularity': [],
        'criterion': []
    }

    for k in np.arange(0.0, 0.95, 0.05):
        graph = StudentsGraph.from_attemps(attemps=attemps, filtering_parameter=k).graph

        communities = louvain_communities(graph, seed=42, weight='weight')
        grouped_communities = group_singleton_communities(communities)
        graph_modularity = modularity(graph, communities=grouped_communities)

        students_analysis_df = students_analysis(attemps=attemps, communities=communities)
        communities_analysis_df = caracterize_communities(students_analysis_df)

        criterion = (communities_analysis_df['std_ns_correct_exercises'] * communities_analysis_df['n_students']).sum() / communities_analysis_df['n_students'].sum()

        data['filtering_parameter'].append(k)
        data['n_edges'].append(len(graph.edges))
        data['modularity'].append(graph_modularity)
        data['criterion'].append(criterion)

    df = DataFrame(data)

    return df

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    DATA_PATH = 'data/'
    INPUT_PATH = DATA_PATH + 'attemps/'
    ANALYSIS_OUTPUT_PATH = DATA_PATH + 'analysis/'
    GRAPHS_OUTPUT_PATH = DATA_PATH + 'graphs/'

    attemps_metrics_data = {
        'year': [],
        'n_students': [],
        'n_exercises': [],
        'n_attemps': [],
    }

    compare_graphs_data = {
        'year': [],
        'n_nodes': [],
        'filtering_parameter': [],
        'n_edges': [],
        'n_edges_filtered_graph': [],
        'modularity': [],
        'modularity_filtered_graph': [],
    }

    for year in YEARS:
        attemps_filepath = INPUT_PATH + 'attemps' + '_' + str(year) + '.csv'
        attemps_df = read_csv(attemps_filepath)

        attemps_metrics_data['year'].append(year)
        attemps_metrics_data['n_students'].append(len(attemps_df['student_id'].unique().tolist()))
        attemps_metrics_data['n_exercises'].append(len(attemps_df['exercise_id'].unique().tolist()))
        attemps_metrics_data['n_attemps'].append(len(attemps_df.index))

        # Grafo sem filtragem
        students_graph = StudentsGraph.from_attemps(attemps=attemps_df).graph
        students_graph_communities = louvain_communities(students_graph, seed=42, weight='weight')
        students_graph_grouped_communities = group_singleton_communities(students_graph_communities)
        students_graph_modularity = modularity(students_graph, communities=students_graph_grouped_communities)

        students_graph_attr = {}
        for idx, community in enumerate(students_graph_grouped_communities):
            for node in community:
                students_graph_attr[node] = {
                    'community': idx
                }
        set_node_attributes(students_graph, students_graph_attr)

        students_graph_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'students_graph' + '.gexf'
        write_gexf(students_graph, students_graph_filepath)

        filtering_parameter_df = find_filtering_parameter(attemps_df)
        filtering_parameter_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'filtering_parameter.csv'
        filtering_parameter_df.to_csv(filtering_parameter_filepath, index=False, decimal=',')
        filtering_parameter = float(filtering_parameter_df.loc[filtering_parameter_df['criterion'] == filtering_parameter_df['criterion'].min(), 'filtering_parameter'].squeeze())

        students_filtered_graph_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'students_filtered_graph' + '.gexf'
        students_filtered_graph = StudentsGraph.from_attemps(attemps_df, filtering_parameter).graph
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
        write_gexf(students_filtered_graph, students_filtered_graph_filepath)

        # Salvando dados da análise dos estudantes
        students_analysis_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'students_analysis' + '.csv'
        students_analysis_df = students_analysis(attemps=attemps_df, communities=students_filtered_graph_grouped_communities)
        students_analysis_df.to_csv(students_analysis_filepath, decimal=',')

        # Salvando dados da análise das comunidades
        communities_analysis_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'communities_analysis' + '.csv'
        communities_analysis_df = caracterize_communities(students_analysis_df)
        communities_analysis_df.to_csv(communities_analysis_filepath, decimal=',')

        # Adicionando dados de comparação entre os grafos
        compare_graphs_data['year'].append(year)
        compare_graphs_data['n_nodes'].append(len(students_graph.nodes))
        compare_graphs_data['n_edges'].append(len(students_graph.edges))
        compare_graphs_data['filtering_parameter'].append(filtering_parameter)
        compare_graphs_data['n_edges_filtered_graph'].append(len(students_filtered_graph.edges))
        compare_graphs_data['modularity'].append(students_graph_modularity)
        compare_graphs_data['modularity_filtered_graph'].append(students_filtered_graph_modularity)

    # Salvando dados das métricas
    attemps_metrics_filepath = ANALYSIS_OUTPUT_PATH + 'attemps_metrics.csv'
    attemps_metrics_df = DataFrame(attemps_metrics_data)
    attemps_metrics_df.to_csv(attemps_metrics_filepath, index=False, decimal=',')

    # Salvando dados da comparação entre os grafos
    compare_graphs_filepath = ANALYSIS_OUTPUT_PATH + 'compare_graphs.csv'
    compare_graphs_df = DataFrame(compare_graphs_data)
    compare_graphs_df.to_csv(compare_graphs_filepath, index=False, decimal=',')