from main import max_flow, max_flow_with_guess
import numpy as np


def make_edges_and_capacities(graph):
    edges = [e[0] for e in graph]

    if len(graph[0]) == 3:
        capacities = [c[2] for c in graph]
        lower_capacities = [c[1] for c in graph]
    else:
        capacities = [c[1] for c in graph]
        lower_capacities = None

    return edges, capacities, lower_capacities


def test_flow_sample_from_cp_algorithms_binary_search():
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

    edges, capacities, _ = make_edges_and_capacities(graph)

    assert max_flow(edges, capacities, s=0, t=5) == 10


def test_flow_sample_from_cp_algorithms_correct_guess():
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

    edges, capacities, _ = make_edges_and_capacities(graph)

    assert max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=10) == 10


def test_flow_sample_from_geeksforgeeks_binary_search():
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

    edges, capacities, _ = make_edges_and_capacities(graph)

    assert max_flow(edges, capacities, s=0, t=5) == 23


def test_flow_sample_from_geeksforgeeks_correct_guess():
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

    edges, capacities, _ = make_edges_and_capacities(graph)

    assert max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=23) == 23


def test_idk_binary_search():
    graph = [
        ((0, 1), 13),
        ((0, 2), 16),
        ((1, 2), 4),
        ((1, 3), 14),
        ((2, 4), 12),
        ((4, 1), 9),
        ((3, 4), 7),
        ((3, 5), 4),
        ((4, 5), 20),
    ]

    edges, capacities, _ = make_edges_and_capacities(graph)

    assert max_flow(edges, capacities, s=0, t=5) == 23


def test_idk_correct_guess():
    graph = [
        ((0, 1), 13),
        ((0, 2), 16),
        ((1, 2), 4),
        ((1, 3), 14),
        ((2, 4), 12),
        ((4, 1), 9),
        ((3, 4), 7),
        ((3, 5), 4),
        ((4, 5), 20),
    ]

    edges, capacities, _ = make_edges_and_capacities(graph)
    # init_flow = np.array([6, 7, 1, 6, 8, 1, 3, 3, 10, 13], dtype=float)

    assert max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=23) == 23


def test_flow_lower_and_upper_binary_search():
    graph = [
        ((0, 1), 2, 8),
        ((0, 2), 1, 9),
        ((1, 3), 1, 4),
        ((1, 2), 0, 3),
        ((2, 3), 2, 5),
        ((2, 4), 1, 8),
        ((3, 4), 4, 8),
        ((3, 5), 0, 7),
        ((4, 5), 4, 10),
    ]

    edges, capacities, lower_capacities = make_edges_and_capacities(graph)

    assert max_flow(edges, capacities, s=0, t=5,
                    lower_capacities=lower_capacities) == 15


def test_flow_lower_and_upper_correct_guess():
    graph = [
        ((0, 1), 2, 8),
        ((0, 2), 1, 9),
        ((1, 3), 1, 4),
        ((1, 2), 0, 3),
        ((2, 3), 2, 5),
        ((2, 4), 1, 8),
        ((3, 4), 4, 8),
        ((3, 5), 0, 7),
        ((4, 5), 4, 10),
    ]

    edges, capacities, lower_capacities = make_edges_and_capacities(graph)

    assert max_flow_with_guess(edges, capacities, s=0, t=5,
                    lower_capacities=lower_capacities, optimal_flow=15) == 15
