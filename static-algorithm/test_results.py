from main import max_flow


def make_edges_and_capacities(graph):
    edges = [e[0] for e in graph]
    capacities = [c[1] for c in graph]
    return edges, capacities


def test_flow_sample_from_cp_algorithms():
    # https://cp-algorithms.com/graph/edmonds_karp.html
    graph = [
        ((0, 1), 7),
        ((0, 2), 4),
        ((2, 1), 3),
        ((1, 3), 5),
        ((1, 4), 3),
        ((2, 4), 2),
        ((4, 3), 3),
        ((3, 5), 8),
        ((4, 5), 5),
    ]

    edges, capacities = make_edges_and_capacities(graph)

    assert max_flow(edges, capacities, s=0, t=5) == 10


def test_flow_sample_from_geeksforgeeks():
    # https://www.geeksforgeeks.org/max-flow-problem-introduction/
    graph = [
        ((0, 1), 11),
        ((0, 2), 12),
        ((2, 1), 1),
        ((1, 3), 12),
        ((2, 4), 11),
        ((4, 3), 7),
        ((3, 5), 19),
        ((4, 5), 4),
    ]

    edges, capacities = make_edges_and_capacities(graph)

    assert max_flow(edges, capacities, s=0, t=5) == 23
