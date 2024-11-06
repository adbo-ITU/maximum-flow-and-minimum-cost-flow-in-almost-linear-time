import networkx as nx
import numpy as np
from min_cost_flow_instance import MinCostFlow
from typing import Tuple, Set, List
from itertools import combinations
import min_ratio as mrlib

kappa = 10


def find_min_ratio_cycle(I: MinCostFlow, f: np.ndarray):
    l = I.calc_lengths(f)
    g = I.calc_gradients(f)

    gl = list(g)
    ll = list(l)

    if I.min_ratio_cycle_finder is None:
        cycles = find_all_cycles(I)
        print(f"Found {len(cycles)} cycles")
        circulations = get_circulations(I, cycles)
        I.min_ratio_cycle_finder = mrlib.MinRatioCycleFinder(circulations)

    min_ratio, min_ratio_cycle = I.min_ratio_cycle_finder.find_min_ratio_cycle(gl, ll)
    min_ratio_cycle = np.array(min_ratio_cycle)

    assert min_ratio_cycle is not None and min_ratio < float('inf'), "No min ratio cycle found"

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


def get_circulations(I: MinCostFlow, cycles: list[list[int]]) -> list[np.ndarray]:
    circulations = []
    for cycle in cycles:
        circulation = np.zeros(I.m, dtype=float)

        for i, edge in enumerate(cycle):
            nex = cycle[(i + 1) % len(cycle)]
            a, b = I.edges[edge]
            if I.edges[nex][0] == a or I.edges[nex][1] == a:
                circulation[edge] = I.B[edge, a]
            else:
                circulation[edge] = I.B[edge, b]

        circulations.append(circulation)
    return circulations


def find_all_cycles(I: MinCostFlow):
    G = nx.MultiGraph(I.edges)

    visited_cycles = set()
    cycles = []
    pair_cycles = []
    for cycle in nx.simple_cycles(G):
        cycle_edges = []
        pair_edges = set()

        for i in range(len(cycle)):
            a = cycle[i]
            b = cycle[(i + 1) % len(cycle)]

            # TODO: handle parallel edges
            edges = I.undirected_edge_to_indices[(a, b)]
            if len(edges) > 1:
                pair_edges.add(edges[0])
            cycle_edges.append(edges[0])

        if len(pair_edges) > 0:
            pair_cycles.append((cycle_edges, pair_edges))

        if len(cycle_edges) == 2 and cycle_edges[0] == cycle_edges[1]:
            continue
        check_if_visited(cycle_edges, visited_cycles, cycles)

    cycles.extend(handle_pair_cycles(I, visited_cycles, pair_cycles))

    return cycles


def handle_pair_cycles(I: MinCostFlow, visited_cycles: Set[List[int]], pair_cycles: List[Tuple[List[int], Set[int]]]):
    cycles = []
    for (cycle, pair_edges) in pair_cycles:
        for amount_to_replace in range(1, len(pair_edges) + 1):
            for edges_to_replace in combinations(pair_edges, amount_to_replace):
                G = nx.MultiGraph(resolve_edges(I, cycle))
                for new_cycle in nx.simple_cycles(G):
                    cycle_edges = []
                    for i in range(len(new_cycle)):
                        a = new_cycle[i]
                        b = new_cycle[(i + 1) % len(new_cycle)]

                        edges = I.undirected_edge_to_indices[(a, b)]
                        edges = [e for e in edges if e not in edges_to_replace]
                        cycle_edges.append(edges[0])

                    if len(cycle_edges) == 2 and cycle_edges[0] == cycle_edges[1]:
                        continue
                    check_if_visited(cycle_edges, visited_cycles, cycles)
        for edge in pair_edges:
            a, b = I.edges[edge]

            check_if_visited(
                I.undirected_edge_to_indices[(a, b)], visited_cycles, cycles)
    return cycles


def resolve_edges(I: MinCostFlow, edge_indices: list[int]):
    return [I.edges[a] for a in edge_indices]


def check_if_visited(cycle_edges: list[int], visited_cycles: set, cycles: list[int]):
    sorted_cycle_edges = tuple(sorted(cycle_edges))
    if sorted_cycle_edges not in visited_cycles:
        visited_cycles.add(sorted_cycle_edges)
        cycles.append(cycle_edges)
