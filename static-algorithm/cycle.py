import networkx as nx
import numpy as np
import numpy.linalg as LA
from min_cost_flow_instance import MinCostFlow


def find_min_ratio_cycle(I: MinCostFlow, f: np.ndarray):
    l = I.calc_lengths(f)
    g = I.calc_gradients(f)
    L = np.diagflat(l)

    min_ratio = float('inf')
    min_ratio_cycle = None

    G = nx.MultiGraph(I.edges)
    # TODO: handle parallel edges - they are not returned as multiple cycles
    for cycle in nx.simple_cycles(G):
        circulation = np.zeros(I.m, dtype=float)

        for i in range(len(cycle)):
            a = cycle[i]
            b = cycle[(i + 1) % len(cycle)]

            # TODO: handle parallel edges
            e = I.undirected_edge_to_indices[(a, b)][0]

            circulation[e] = I.B[e, a]

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

    # TODO: scale the circulation according to Theorem 4.3, step 2
    # idk how to do that right now, so we just do 90% of the way to
    # the closest constraint of an edge on the cycle
    max_valid_change = float('inf')
    for e in range(I.m):
        if min_ratio_cycle[e] != 0:
            diff_upper = abs(I.u_upper[e] - f[e])
            diff_lower = abs(f[e] - I.u_lower[e])
            max_valid_change = min(max_valid_change, min(abs(diff_upper), abs(diff_lower)))
    scaling_factor = max_valid_change * 0.9

    return (min_ratio, min_ratio_cycle * scaling_factor)
