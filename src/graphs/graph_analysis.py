import numpy as np
from networkx import Graph
from pandas import DataFrame
from .students_graph import StudentsGraph
from networkx.algorithms.community import louvain_communities, modularity
from typing import List, Set

def louvain_grouped_communities(graph:Graph, weight) -> List[Set[int]]:
    if len(graph.edges) == 0:
        communities = [set(graph.nodes),]
    else:
        communities = louvain_communities(graph, seed=42, weight=weight)

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

def filtering_parameter_analysis(solving_df:DataFrame, step=0.05):

    data = {
        'filtering_parameter': [],
        'n_edges': [],
        'modularity': [],
        'criterion': []
    }

    for k in np.arange(0.0, 1.1, step=step):
        graph = StudentsGraph(solving_df=solving_df, filtering_parameter=k).graph

        n_students = len(solving_df.index.get_level_values('student_id').unique())

        graph_communities = louvain_grouped_communities(graph=graph, weight='weight')
        if len(graph.edges) == 0:
            graph_modularity = None
        else:
            graph_modularity = modularity(graph, communities=graph_communities)

        errors = []
        for community in graph_communities:
            df = solving_df.loc[solving_df.index.get_level_values('student_id').isin(community)].groupby(level='student_id').size()
            std = np.std(df)

            error = std * len(community)
            errors.append(error)

        criterion = np.sum(errors)/n_students

        data['filtering_parameter'].append(k)
        data['n_edges'].append(len(graph.edges))
        data['modularity'].append(graph_modularity)
        data['criterion'].append(criterion)

    df = DataFrame(data)

    return df