from networkx import set_node_attributes, set_edge_attributes

def add_graphic_attrs(graph, value='BT') -> None:
    graph.graph['graph'] = {'rankdir':value}

def add_community_attrs(graph, communities) -> None:
    attrs = {}
    for idx, community in enumerate(communities):
        name = idx

        for node in community:
            attrs[node] = {
                'community': name,
            }

    set_node_attributes(graph, attrs)

def add_student_attrs(graph, nodes) -> None:
    attrs = {}
    for student_id in nodes:
        attrs[student_id] = {
            'shape': 'circle',
            'style': 'filled',
            'fillcolor': 'lightblue'
        }

    set_node_attributes(graph, attrs)

def add_exercise_attrs(graph, nodes):
    attrs = {}

    for exercise_id in nodes:
        attrs[exercise_id] = {
            'shape': 'rect',
            'style': 'filled',
            'fillcolor': 'lightyellow'
        }

    set_node_attributes(graph, attrs)

def add_edges_attrs(graph):
    attrs = {}

    for u, v, data in graph.edges(data=True):
        attrs[(u, v)] = {
            'label': data['weight']
        }

    set_edge_attributes(graph, attrs)