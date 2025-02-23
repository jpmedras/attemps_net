from pandas import read_csv
from analysis import attemps_to_solving, attemps_to_trying
from graphs import AttempsMultiGraph, StudentsDiGraph, StudentsGraph
from networkx.drawing.nx_pydot import write_dot
from networkx import write_gml
from graphs import louvain_grouped_communities, filtering_parameter_analysis
from graphs import add_graphic_attrs, add_student_attrs, add_community_attrs, add_exercise_attrs, add_edges_attrs

if __name__ == "__main__":
    PATH = 'data/examples/'

    attemps_filepath = PATH + 'attemps.csv'
    attemps_df = read_csv(attemps_filepath)
    print(attemps_df)

    solving_filepath = PATH + 'solving.csv'
    solving_df = attemps_to_solving(attemps_df=attemps_df)
    solving_df.to_csv(solving_filepath, decimal=',')
    print(solving_df)

    trying_filepath = PATH + 'trying.csv'
    trying_df = attemps_to_trying(attemps_df=attemps_df)
    trying_df.to_csv(trying_filepath, decimal=',')
    print(trying_df)

    graph_a = AttempsMultiGraph(attemps_df=attemps_df)
    add_graphic_attrs(graph_a.graph)
    add_student_attrs(graph_a.graph, attemps_df['student_id'].unique())
    add_exercise_attrs(graph_a.graph, attemps_df['exercise_id'].unique())
    write_dot(graph_a.graph, PATH + 'graph_a.dot')

    print("Graph A:")
    for u, data in graph_a.graph.nodes(data=True):
        print(u, data)

    for u, v, data in graph_a.graph.edges(data=True):
        print(u, v, data)

    graph_o = StudentsDiGraph(solving_df=solving_df)
    add_graphic_attrs(graph_o.graph, 'LR')
    add_student_attrs(graph_o.graph, graph_o.graph.nodes)
    write_dot(graph_o.graph, PATH + 'graph_o.dot')

    print("Graph O:")
    for u, data in graph_o.graph.nodes(data=True):
        print(u, data)

    for u, v, data in graph_o.graph.edges(data=True):
        print(u, v, data)

    print("Graph S:")
    graph_s = StudentsGraph(solving_df=solving_df)
    add_graphic_attrs(graph_s.graph, 'LR')
    add_student_attrs(graph_s.graph, graph_s.graph.nodes)
    add_edges_attrs(graph_s.graph)
    write_dot(graph_s.graph, PATH + 'graph_s.dot')

    for u, data in graph_s.graph.nodes(data=True):
        print(u, data)

    for u, v, data in graph_s.graph.edges(data=True):
        print(u, v, data)

    print("Graph G:")
    graph_g = StudentsGraph(solving_df=solving_df, filtering_parameter=0.5)
    add_graphic_attrs(graph_g.graph, 'LR')
    add_student_attrs(graph_g.graph, graph_g.graph.nodes)
    add_edges_attrs(graph=graph_g.graph)
    write_dot(graph_g.graph, PATH + 'graph_g.dot')

    for u, data in graph_g.graph.nodes(data=True):
        print(u, data)

    for u, v, data in graph_g.graph.edges(data=True):
        print(u, v, data)

    filtering_df = filtering_parameter_analysis(solving_df=solving_df, step=0.1)
    print(filtering_df)

    communities, pseudocommunity_idx = louvain_grouped_communities(graph_g.graph, weight='weight')
    add_community_attrs(graph=graph_g.graph, communities=communities)
    
    write_gml(graph_g.graph, PATH + 'g.gml')