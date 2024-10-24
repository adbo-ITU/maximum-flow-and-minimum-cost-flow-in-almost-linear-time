from typing import Tuple
import numpy as np
from cycle import find_min_ratio_cycle
from min_cost_flow_instance import MinCostFlow


def max_flow(edges: list[Tuple[int, int]], capacities: list[int], s: int, t: int, optimal_flow: int):
    I = MinCostFlow.from_max_flow_instance(
        edges=edges, s=s, t=t, optimal_flow=optimal_flow, capacities=capacities)

    print(I)
    print()
    I.print_B()
    print()

    # TODO: find actual feasible initial flow.
    cur_flow = (I.u_lower + I.u_upper) / 2
    cur_flow[-1] = optimal_flow / 2

    threshold = float(I.m * I.U) ** (-10)
    i = 0
    while I.c.dot(cur_flow) - I.optimal_cost >= threshold:
        i += 1
        print("Iteration", i)
        print("Φ(f) =", I.phi(cur_flow))

        min_ratio, min_ratio_cycle = find_min_ratio_cycle(I, cur_flow)

        cur_flow += min_ratio_cycle

        print("min_ratio =", min_ratio)
        print("min_ratio_cycle =", min_ratio_cycle)
        print("  -> edges:", [I.edges[e]
              for e, c in enumerate(min_ratio_cycle) if c != 0])
        print("flow: ", cur_flow)
        print()

    return cur_flow[-1]


if __name__ == "__main__":
    # This is the example max-flow graph at https://www.geeksforgeeks.org/max-flow-problem-introduction/
    # no its not - oops
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

    edges = [e[0] for e in graph]
    capacities = [c[1] for c in graph]

    low, high = 0, sum(c[1] for c in graph if c[0][0] == 0)
    while low < high:
        mid = (low + high) // 2
        mf = max_flow(edges, capacities, s=0, t=5, optimal_flow=mid)

        if mf == mid:
            low = mid
            break
        elif mf < mid:
            high = mid
        else:
            low = mid + 1

    print("Converged to", low)
