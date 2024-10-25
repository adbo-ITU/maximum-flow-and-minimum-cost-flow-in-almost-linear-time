from copy import deepcopy
import numpy as np
from min_cost_flow_instance import MinCostFlow


def calc_feasible_flow(I_or: MinCostFlow):
    # TODO: Probably thanos-snap this
    I = deepcopy(I_or)

    # Add a new vertex v*
    v_star = I.add_vertex()

    # TODO: Replace with actual demands when implemented
    demands = np.zeros(I.n, dtype=int)
    assert np.sum(demands) == 0

    init_flow = (I.u_lower + I.u_upper) / 2
    print(init_flow)
    d_hat = np.dot(I.B.transpose(), init_flow)

    c = 4 * I.m * I.U ** 2
    for v in range(I.n):
        dh = d_hat[v]
        d = demands[v]

        if dh > d:
            I.add_edge(v, v_star, c, 0, 2 * (dh - d))
            init_flow = np.append(init_flow, dh - d)
        elif dh < d:
            I.add_edge(v_star, v, c, 0, 2 * (d - dh))
            init_flow = np.append(init_flow, d - dh)

    assert len(init_flow) == I.m

    return I, init_flow
