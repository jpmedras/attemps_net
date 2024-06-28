from graphs.students_graph import StudentsGraph
from networkx import read_gexf, write_gexf
from networkx import set_node_attributes
from networkx.algorithms.community import louvain_communities, modularity
import matplotlib.pyplot as plt

def students_graph(file_path):
    G = StudentsGraph.from_json(file_path)

    graph = G.to_graph()

    communities = louvain_communities(graph, seed=42, weight='weight')
    # modularity_ = modularity(graph, communities, weight='weight')

    community_attr = {}
    for idx, community in enumerate(communities):
        for node in community:
            community_attr[node] = {
                'community': idx
            }

    set_node_attributes(graph, community_attr)

    return graph

if __name__ == '__main__':
    # YEARS = [2018, 2019, 2021, 2022, 2023]
    YEARS = [2018]
    OUTPUT_PATH = 'assets/'

    for year in YEARS:
        file_path = 'private_data/by_year/' + str(year) + '.json'
        output_path = OUTPUT_PATH + 'students/' + str(year) + '/' + str(year) + '.gexf'

        G = students_graph(file_path)
        print(G)

        write_gexf(G, output_path)

    
    # G = read_gexf('assets/students/Untitled.gexf')
    # for node, data in G.nodes(data=True):
    #     print(node, data)

    # for 