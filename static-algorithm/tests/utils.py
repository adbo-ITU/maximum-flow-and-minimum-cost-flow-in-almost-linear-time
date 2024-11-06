from typing import Union


Edge = tuple[int, int]
EdgeSpec = Union[tuple[Edge, int], tuple[Edge, int, int]]
Graph = list[EdgeSpec]


def make_edges_and_capacities(graph: Graph):
    edges = [e[0] for e in graph]

    if len(graph[0]) == 3:
        capacities = [c[2] for c in graph]
        lower_capacities = [c[1] for c in graph]
    else:
        capacities = [c[1] for c in graph]
        lower_capacities = None

    return edges, capacities, lower_capacities
