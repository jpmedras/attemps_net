from graphs.graph_abc import GraphABC
from networkx import Graph, DiGraph
from typing import List, Dict, Set
from typing import Any
from submissions import SubmissionList
import numpy as np

class StudentsGraph(GraphABC):
    def __init__(self, submissions:SubmissionList=None, k:float=None) -> None:
        super().__init__(submissions)
        
        self._neighbors = self._student_neighbors()

        self._overlap_graph = DiGraph()
        self._add_nodes()
        self._add_edges()
        
        overlaps = self.overlap_dist()
        quantile = np.quantile(overlaps, 0.5)

        if k is None:
            k = quantile

        self._filter(k)


    def _student_neighbors(self) -> Dict[Any, Set[Any]]:
        neighbors = {}

        for s in self._submissions:
            if s.student not in neighbors:
                neighbors[s.student] = set()
            
            if s.result:
                neighbors[s.student].add(s.question)

        return neighbors
    
    @property
    def neighbors(self) -> Dict[Any, Set[Any]]:
        return self._neighbors

    def _add_nodes(self) -> None:
        for student_u in self._neighbors:
            if not self._overlap_graph.has_node(student_u):
                self._overlap_graph.add_node(student_u, size=len(self._neighbors[student_u]))
    
    def _add_edges(self):
        for u, neighbors_u in self._neighbors.items():
            for v, neighbors_v in self._neighbors.items():

                if u == v:
                    continue

                if len(neighbors_u) > 0:
                    overlap = len(neighbors_u & neighbors_v) / len(neighbors_u)

                    if overlap > 0:
                        self._overlap_graph.add_edge(u, v, weight=overlap)
                        # self._overlap_graph[u][v].update({'weight': overlap})

    def _filter(self, k:float) -> None:
        graph = DiGraph()

        for u, v, data in self._overlap_graph.edges(data=True):
            if data['weight'] >= k:
                graph.add_edge(u, v, **data)

        self._overlap_graph = graph

    def to_graph(self) -> Graph:
        graph = Graph()

        for u in self._neighbors:
            graph.add_node(u, size=len(self._neighbors[u]))

        for u in self._overlap_graph:
            for v in self._overlap_graph:

                if u == v:
                    continue

                if self._overlap_graph.has_edge(u, v) and self._overlap_graph.has_edge(v, u):
                    graph.add_edge(u, v, weight=len(self._neighbors[u] & self._neighbors[v]))

        return graph
    
    def neighbor_dist(self) -> List[int]:
        return [len(neighbors) for u, neighbors in self._neighbors.items()]
    
    def overlap_dist(self) -> List[float]:
        overlaps = []
        for _, _, data in self._overlap_graph.edges(data=True):
            overlaps.append(data['weight'])

        return overlaps