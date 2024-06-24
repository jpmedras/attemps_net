import json
import pandas as pd
from models.submission import Submission
from models.graph_trivial import GraphTrivial
from networkx.drawing.nx_agraph import write_dot

def from_json(filepath:str) -> None:
    subs = []

    with open(filepath) as file:
        content = json.load(file)

    for s in content:
        sub = Submission(s['id_student'], s['id_question'], s['result'], s['timestamp'], s['time'])
        subs.append(sub)

    return subs

YEARS = [2018, 2019, 2021, 2022, 2023]

PATH = 'data/by_year/'
OUT_PATH = 'assets/trivial/'

n_nodes = []
n_edges = []

for year in YEARS:
    filepath = PATH + f'{year}.json'

    subs = from_json(filepath)

    my_g = GraphTrivial(subs)
    g = my_g.to_graph()

    n_nodes.append(len(g.nodes))
    n_edges.append(len(g.edges))

    write_dot(g, OUT_PATH + f'{year}.dot')

df = pd.DataFrame.from_dict(
    {
        'year': YEARS,
        'n_nodes': n_nodes,
        'n_edges': n_edges
    },
).set_index('year')

df.to_csv('assets/trivial_info.csv')