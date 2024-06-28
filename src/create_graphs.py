from submissions.submission import Submission
from graphs.students_graph import StudentsGraph
from networkx import read_gexf, write_gexf

def students_graph(file_path, output_path):
    G = StudentsGraph.from_json(file_path)
    G = G.to_graph()

    write_gexf(G, output_path)

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    OUTPUT_PATH = 'assets/'

    for year in YEARS:
        file_path = 'private_data/by_year/' + str(year) + '.json'
        output_path = OUTPUT_PATH + 'students/' + str(year) + '/' + str(year) + '.gexf'

        students_graph(file_path, output_path)

    G = read_gexf('assets/students/Untitled.gexf')
    for node, data in G.nodes(data=True):
        print(node, data)

    # for 