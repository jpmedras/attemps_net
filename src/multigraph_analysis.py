from submissions import SubmissionList
from graphs import MultiGraph
import pygraphviz as pgv
import pandas as pd

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    OUTPUT_PATH = 'assets/'

    for year in YEARS:
        file_path = 'private_data/by_year/' + str(year) + '.json'
        graph_path = OUTPUT_PATH + 'multigraph/' + str(year) + '/' + str(year) + '.dot'
        image_path = OUTPUT_PATH + 'multigraph/' + str(year) + '/' + 'plot_' + str(year) + '.png'
        # analysis_path = OUTPUT_PATH + 'multigraph/' + str(year) + '/' + 'analysis_' + str(year) + '.csv'

        submissions = SubmissionList.from_json(file_path)
        graph = MultiGraph(submissions)

        G = graph.to_graph()
        
        G.layout(prog="sfdp", args='-x -Goverlape=scale')

        G.write(graph_path)
        G.draw(image_path)