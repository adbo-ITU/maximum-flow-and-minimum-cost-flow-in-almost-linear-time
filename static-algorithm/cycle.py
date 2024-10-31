import networkx as nx
import numpy as np
import numpy.linalg as LA
from min_cost_flow_instance import MinCostFlow

kappa = 10


def find_min_ratio_cycle(I: MinCostFlow, f: np.ndarray):
    l = I.calc_lengths(f)
    g = I.calc_gradients(f)
    L = np.diagflat(l)

    min_ratio = float('inf')
    min_ratio_cycle = None

    if I.cycle_cache is None:
        cycles = find_all_cycles(I)
        I.cycle_cache = cycles
    else:
        cycles = I.cycle_cache

    # TODO: handle parallel edges - they are not returned as multiple cycles
    for cycle in cycles:
        circulation = np.zeros(I.m, dtype=float)

        for i, edge in enumerate(cycle):
            nex = cycle[(i + 1) % len(cycle)]
            a, b = I.edges[edge]
            if I.edges[nex][0] == a or I.edges[nex][1] == a:
                circulation[edge] = I.B[edge, a]
            else:
                circulation[edge] = I.B[edge, b]

        for dir in [1, -1]:
            delta = dir * circulation

            gd = g.dot(delta)
            Lxd = L @ delta
            norm = LA.norm(Lxd, 1)
            ratio = gd / norm

            if ratio < min_ratio:
                min_ratio = ratio
                min_ratio_cycle = circulation

    assert min_ratio_cycle is not None, "No min ratio cycle found"

    # assert min_ratio <= -kappa, f"min_ratio is not less than -kappa: {min_ratio}"

    # TODO: I don't know how I made this work, but I did. I'm not sure how good it is.
    # For example, eta can now be negative, which essentially flips the circulation..
    # Do we want that? Is it correct? If I understand the paper correctly, eta is always >0.
    # But Φ(f) explodes if I do the absolute value.
    gd = g.dot(min_ratio_cycle)
    print("gd =", gd)
    # TODO: Scale the circulation according to Theorem 4.3, step 2
    eta = -kappa / gd
    print("eta =", eta)

    return (min_ratio, min_ratio_cycle * eta)


def find_all_cycles(I: MinCostFlow):
    G = nx.MultiGraph(I.edges)

    visited_cycles = set()
    cycles = []
    pair_cycles = []
    for cycle in nx.simple_cycles(G):
        cycle_edges = []
        for i in range(len(cycle)):
            a = cycle[i]
            b = cycle[(i + 1) % len(cycle)]

            # TODO: handle parallel edges
            edges = I.undirected_edge_to_indices[(a, b)]
            if len(edges) > 1:
                pair_cycles.append(cycle)
                break
            else:
                cycle_edges.append(edges[0])
        else:
            check_if_visited(cycle_edges, visited_cycles, cycles)
    cycles.extend(handle_pair_cycles(I, pair_cycles))

    return cycles


def handle_pair_cycles(I: MinCostFlow, pair_cycles: list[list[int]]):
    visited_cycles = set()
    cycles = []
    for cycle in pair_cycles:
        pair_edges = set()
        normal_edges = []

        for i in range(len(cycle)):
            a = cycle[i]
            b = cycle[(i + 1) % len(cycle)]

            edges = I.undirected_edge_to_indices[(a, b)]
            if len(edges) > 1:
                pair_edges = pair_edges.union(edges)
                check_if_visited(edges, visited_cycles, cycles)
            else:
                normal_edges.append(edges[0])

        pair_edges = list(pair_edges)
        for i, pair_edge in enumerate(pair_edges):
            exclude = pair_edges[:i] + pair_edges[i + 1:]

            G = nx.MultiGraph(resolve_edges(I, normal_edges + exclude))
            for cycle in nx.simple_cycles(G):
                cycle_edges = []
                for i in range(len(cycle)):
                    a = cycle[i]
                    b = cycle[(i + 1) % len(cycle)]

                    edges = I.undirected_edge_to_indices[(a, b)]
                    edges = [e for e in edges if e != pair_edge]
                    cycle_edges.append(edges[0])

                if len(cycle_edges) == 2 and cycle_edges[0] == cycle_edges[1]:
                    continue
                check_if_visited(cycle_edges, visited_cycles, cycles)
    return cycles


def resolve_edges(I: MinCostFlow, edge_indices: list[int]):
    return [I.edges[a] for a in edge_indices]


def check_if_visited(cycle_edges: list[int], visited_cycles: set, cycles: list[int]):
    sorted_cycle_edges = tuple(sorted(cycle_edges))
    if sorted_cycle_edges not in visited_cycles:
        visited_cycles.add(sorted_cycle_edges)
        cycles.append(cycle_edges)
