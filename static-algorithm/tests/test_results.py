from main import max_flow, max_flow_with_guess
from tests.utils import make_edges_and_capacities


# https://cp-algorithms.com/graph/edmonds_karp.html
CP_ALGORITHMS_GRAPH = [
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


def test_flow_sample_from_cp_algorithms_binary_search():
    edges, capacities, _ = make_edges_and_capacities(CP_ALGORITHMS_GRAPH)
    mf, _ = max_flow(edges, capacities, s=0, t=5)
    assert mf == 10


def test_flow_sample_from_cp_algorithms_correct_guess():
    edges, capacities, _ = make_edges_and_capacities(CP_ALGORITHMS_GRAPH)
    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=10)
    assert mf == 10


# https://www.geeksforgeeks.org/max-flow-problem-introduction/
GEEKS_FOR_GEEKS_GRAPH = [
    ((0, 1), 16),
    ((0, 2), 13),
    ((1, 2), 10),
    ((2, 1), 4),
    ((1, 3), 12),
    ((2, 4), 14),
    ((3, 2), 9),
    ((4, 3), 7),
    ((3, 5), 20),
    ((4, 5), 4),
]


def test_flow_real_sample_from_geeksforgeeks_correct_guess():
    edges, capacities, _ = make_edges_and_capacities(GEEKS_FOR_GEEKS_GRAPH)
    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=23)
    assert mf == 23


def test_flow_real_sample_from_geeksforgeeks_binary_search():
    edges, capacities, _ = make_edges_and_capacities(GEEKS_FOR_GEEKS_GRAPH)
    mf, _ = max_flow(edges, capacities, s=0, t=5)
    assert mf == 23


# Previous graph but use the graph of the optimal flow. Useful because
# using half of the edge capacities for initial flow is a feasible flow.
GEEKS_FOR_GEEKS_MAXFLOW_GRAPH = [
    ((0, 1), 11),
    ((0, 2), 12),
    ((2, 1), 1),
    ((1, 3), 12),
    ((2, 4), 11),
    ((4, 3), 7),
    ((3, 5), 19),
    ((4, 5), 4),
]


def test_flow_sample_from_geeksforgeeks_binary_search():
    edges, capacities, _ = make_edges_and_capacities(
        GEEKS_FOR_GEEKS_MAXFLOW_GRAPH)
    mf, _ = max_flow(edges, capacities, s=0, t=5)
    assert mf == 23


def test_flow_sample_from_geeksforgeeks_correct_guess():
    edges, capacities, _ = make_edges_and_capacities(
        GEEKS_FOR_GEEKS_MAXFLOW_GRAPH)
    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=23)
    assert mf == 23


def test_flow_parallel_edge_correct_guess():
    graph = [
        ((0, 1), 5),
        ((2, 1), 1),
        ((1, 2), 6),
        ((2, 3), 7),
    ]

    edges, capacities, _ = make_edges_and_capacities(graph)

    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=3, optimal_flow=5)
    assert mf == 5


IDK_GRAPH = [
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


def test_idk_binary_search():
    edges, capacities, _ = make_edges_and_capacities(IDK_GRAPH)
    mf, _ = max_flow(edges, capacities, s=0, t=5)
    assert mf == 23


def test_idk_correct_guess():
    graph = IDK_GRAPH
    edges, capacities, _ = make_edges_and_capacities(graph)
    # init_flow = np.array([6, 7, 1, 6, 8, 1, 3, 3, 10, 13], dtype=float)
    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=5, optimal_flow=23)
    assert mf == 23


FLOW_LOWER_UPPER_GRAPH = [
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


def test_flow_lower_and_upper_binary_search():
    edges, capacities, lower_capacities = make_edges_and_capacities(FLOW_LOWER_UPPER_GRAPH)
    mf, _ = max_flow(edges, capacities, s=0, t=5, lower_capacities=lower_capacities)
    assert mf == 15


def test_flow_lower_and_upper_correct_guess():
    edges, capacities, lower_capacities = make_edges_and_capacities(FLOW_LOWER_UPPER_GRAPH)
    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=5, lower_capacities=lower_capacities, optimal_flow=15)
    assert mf == 15


def test_thore_fractional_graph_correct_guess():
    graph = [
        ((0, 1), 1),
        ((0, 2), 1),
        ((1, 3), 1),
        ((2, 3), 1),
        ((3, 4), 1),
    ]

    edges, capacities, _ = make_edges_and_capacities(graph)

    mf, _ = max_flow_with_guess(edges, capacities, s=0, t=4, optimal_flow=1)
    assert mf == 1
