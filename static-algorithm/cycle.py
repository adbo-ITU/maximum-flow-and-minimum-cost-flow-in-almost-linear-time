import networkx as nx
import numpy as np
import numpy.linalg as LA
from min_cost_flow_instance import MinCostFlow


kappa = 1

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

    # assert min_ratio <= -kappa, f"min_ratio is not less than -kappa: {min_ratio}"

    gd = g.dot(min_ratio_cycle)
    print("gd =", gd)
    # TODO: Scale the circulation according to Theorem 4.3, step 2
    eta = -kappa / gd
    print("eta =", eta)

    return (min_ratio, min_ratio_cycle * eta)
