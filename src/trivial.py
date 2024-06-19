import json
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

years = [2018, 2019, 2021, 2022, 2023]

path = 'data/by_year/'
out_path = 'assets/trivial/'

for year in years:
    filepath = path + f'{year}.json'

    subs = from_json(filepath)

    my_g = GraphTrivial(subs)
    g = my_g.to_graph()

    write_dot(g, out_path + f'{year}.dot')