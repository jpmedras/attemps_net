from graphs import AttempsMultiDiGraph, StudentsGraph
from graphs import louvain_grouped_communities, filtering_parameter_analysis
from graphs import add_community_attrs
from analysis import attemps_to_solving, attemps_to_trying
from networkx.algorithms.community import modularity
from pandas import DataFrame, read_csv
from analysis import caracterize_communities
from networkx import write_gml
from scipy.stats import linregress
import numpy as np

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    DATA_PATH = 'data/'
    INPUT_PATH = DATA_PATH + 'attemps/'
    ANALYSIS_OUTPUT_PATH = DATA_PATH + 'analysis/'
    GRAPHS_OUTPUT_PATH = DATA_PATH + 'graphs/'

    graph_comparison_data = {
        'year': [],
        'n_nodes_a': [],
        'n_edges_a': [],
        'n_nodes_s_g': [],
        'n_edges_s': [],
        'n_edges_g': [],
        'modularity_s': [],
        'modularity_g': [],
        'filtering_parameter': [],
    }

    students_analysis_data = {
        'year': [],
        'student_id': [],
        'community': [],
        'n_solved_exercises': [],
        'solved_exercise_ids': [],
        'solving_times': [],
        'n_tried_exercises': [],
        'tried_exercise_ids': [],
        'trying_times': [],
        'results': []
    }

    metrics_correlation_data = {
        'year': [],
        'mean_std_ns_solved_exercises': [],
        'r-squared_mean_ns_solved_exercises_mean_ns_attemps': [],
        'mean_std_ns_attemps': [],
        'r-squared_mean_ns_solved_exercises_mean_ns_tried_exercises': [],
        'mean_std_ns_tried_exercises': [],
        'r-squared_mean_ns_solved_exercises_mean_mean_solving_times': [],
        'mean_std_mean_solving_times': []

    }

    for year in YEARS:
        attemps_filepath = INPUT_PATH + 'attemps' + '_' + str(year) + '.csv'
        attemps_df = read_csv(attemps_filepath)

        # Criando DataFrame de exercícios resolvidos

        solving_df = attemps_to_solving(attemps_df=attemps_df)

        # Criando DataFrame de exercícios tentados

        trying_df = attemps_to_trying(attemps_df=attemps_df) 

        # Criando grafo A

        graph_a = AttempsMultiDiGraph(attemps_df=attemps_df).graph

        # Criando grafo S

        graph_s_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'graph_s' + '.gml'
        graph_s = StudentsGraph(solving_df=solving_df).graph
        graph_s_communities = louvain_grouped_communities(graph_s, weight='weight')
        graph_s_modularity = modularity(graph_s, communities=graph_s_communities)

        add_community_attrs(graph_s, graph_s_communities)
        write_gml(graph_s, graph_s_filepath)

        # Calculando parâmetro de filtragem

        filtering_parameter_df = filtering_parameter_analysis(solving_df=solving_df)
        filtering_parameter_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'filtering_parameter.csv'
        filtering_parameter_df.to_csv(filtering_parameter_filepath, index=False, decimal=',')
        filtering_parameter = float(filtering_parameter_df.loc[filtering_parameter_df['criterion'] == filtering_parameter_df['criterion'].min(), 'filtering_parameter'].squeeze())

        # Criando grafo G
        
        graph_g_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'graph_g' + '.gml'
        graph_g = StudentsGraph(solving_df=solving_df, filtering_parameter=filtering_parameter).graph
        graph_g_communities = louvain_grouped_communities(graph_g, weight='weight')
        graph_g_modularity = modularity(graph_g, communities=graph_g_communities)

        add_community_attrs(graph_g, graph_g_communities)
        write_gml(graph_g, graph_g_filepath)

        # Adicionando dados de comparação entre os grafos

        graph_comparison_data['year'].append(year)
        graph_comparison_data['n_nodes_a'].append(len(graph_a.nodes()))
        graph_comparison_data['n_edges_a'].append(len(graph_a.edges()))
        graph_comparison_data['n_nodes_s_g'].append(len(graph_s.nodes))
        graph_comparison_data['n_edges_s'].append(len(graph_s.edges))
        graph_comparison_data['n_edges_g'].append(len(graph_g.edges))
        graph_comparison_data['modularity_s'].append(graph_s_modularity)
        graph_comparison_data['modularity_g'].append(graph_g_modularity)
        graph_comparison_data['filtering_parameter'].append(filtering_parameter)

        # Adicionando dados de análise dos estudantes

        for student_id, group in attemps_df.groupby('student_id'):
            for idx, community in enumerate(graph_g_communities):
                if student_id in community:
                    community_id = idx
                    break

            solved_group = solving_df.loc[solving_df.index.get_level_values('student_id') == student_id]
            solved_exercise_ids = solved_group.index.get_level_values('exercise_id').unique().to_list()
            solving_times = solved_group['solving_time'].to_list()

            tried_group = trying_df.loc[trying_df.index.get_level_values('student_id') == student_id]
            tried_exercise_ids = tried_group.index.get_level_values('exercise_id').unique().to_list()
            trying_times = tried_group['trying_time'].to_list()

            results = group['is_correct'].to_list()

            students_analysis_data['year'].append(year)
            students_analysis_data['student_id'].append(student_id)
            students_analysis_data['community'].append(community_id)
            students_analysis_data['n_solved_exercises'].append(len(solved_exercise_ids))
            students_analysis_data['solved_exercise_ids'].append(solved_exercise_ids)
            students_analysis_data['solving_times'].append(solving_times)
            students_analysis_data['n_tried_exercises'].append(len(tried_exercise_ids))
            students_analysis_data['tried_exercise_ids'].append(tried_exercise_ids)
            students_analysis_data['trying_times'].append(trying_times)
            students_analysis_data['results'].append(results)

    # Salvando dados da análise dos estudantes

    students_analysis_filepath = ANALYSIS_OUTPUT_PATH + 'students_analysis' + '.csv'
    students_analysis_df = DataFrame(students_analysis_data).set_index(['year', 'student_id'])
    students_analysis_df.to_csv(students_analysis_filepath, decimal=',')

    # Salvando dados da análise das comunidades

    communities_analysis_filepath = ANALYSIS_OUTPUT_PATH + 'communities_analysis' + '.csv'
    communities_analysis_df = caracterize_communities(students_analysis_df)
    communities_analysis_df.to_csv(communities_analysis_filepath, decimal=',')

    # Salvando dados da correlações entre métricas das comunidades

    metrics_correlation_filepath = ANALYSIS_OUTPUT_PATH + 'metrics_correlation' + '.csv'
    for year, group in communities_analysis_df.groupby('year'):
        mean_ns_solved_exercises = group['mean_ns_solved_exercises'].to_list()
        std_ns_solved_exercises = group['std_ns_solved_exercises'].to_list()

        mean_ns_tried_exercises = group['mean_ns_tried_exercises'].to_list()
        std_ns_tried_exercises = group['std_ns_tried_exercises'].to_list()

        mean_ns_attemps = group['mean_ns_attemps'].to_list()
        std_ns_attemps = group['std_ns_attemps'].to_list()

        mean_mean_solving_times = group['mean_mean_solving_times'].to_list()
        std_mean_solving_times = group['std_mean_solving_times'].to_list()

        r_mnse_mna = linregress(mean_ns_solved_exercises, mean_ns_attemps).rvalue
        r_mnse_mnte = linregress(mean_ns_solved_exercises, mean_ns_tried_exercises)
        r_mnse_mmst = linregress(mean_ns_solved_exercises, mean_mean_solving_times).rvalue

        metrics_correlation_data['year'].append(year)
        metrics_correlation_data['mean_std_ns_solved_exercises'].append(np.mean(std_ns_solved_exercises))
        metrics_correlation_data['r-squared_mean_ns_solved_exercises_mean_ns_attemps'].append(r_mnse_mna)
        metrics_correlation_data['mean_std_ns_attemps'].append(np.mean(std_ns_attemps))
        metrics_correlation_data['r-squared_mean_ns_solved_exercises_mean_ns_tried_exercises'].append(r_mnse_mna)
        metrics_correlation_data['mean_std_ns_tried_exercises'].append(np.mean(std_ns_tried_exercises))
        metrics_correlation_data['r-squared_mean_ns_solved_exercises_mean_mean_solving_times'].append(r_mnse_mmst)
        metrics_correlation_data['mean_std_mean_solving_times'].append(np.mean(std_mean_solving_times))
    
    metrics_correlation_df = DataFrame(metrics_correlation_data).set_index('year')
    metrics_correlation_df.to_csv(metrics_correlation_filepath, decimal=',')

    # Salvando dados da comparação entre os grafos

    graph_comparison_filepath = ANALYSIS_OUTPUT_PATH + 'graph_comparison.csv'
    graph_comparison_df = DataFrame(graph_comparison_data)
    graph_comparison_df.to_csv(graph_comparison_filepath, index=False, decimal=',')