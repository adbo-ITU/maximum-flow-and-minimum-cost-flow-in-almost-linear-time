from typing import Tuple
from cycle import find_min_ratio_cycle
from min_cost_flow_instance import MinCostFlow
from feasible_flow import calc_feasible_flow
import numpy as np


def max_flow_with_guess(edges: list[Tuple[int, int]], capacities: list[int], s: int, t: int, optimal_flow: int, lower_capacities: list[int] = None):
    I = MinCostFlow.from_max_flow_instance(
        edges=edges, s=s, t=t, optimal_flow=optimal_flow, capacities=capacities, lower_capacities=lower_capacities)

    print("Initial instance:")
    print(I)
    print()
    I.print_B()
    print()

    original_m = I.m
    flow_idx = original_m - 1
    I, cur_flow = calc_feasible_flow(I)

    print("Feasible flow instance:")
    print(I)
    print("initial_flow:", cur_flow)
    print()
    I.print_B()
    print()


    # threshold = float(I.m * I.U) ** (-10)
    threshold = 1e-5
    print("Threshold:", threshold)

    i = 0
    cur_phi = I.phi(cur_flow)
    while I.c.dot(cur_flow) - I.optimal_cost >= threshold:
        i += 1
        print("Iteration", i)
        print("Φ(f) =", cur_phi)

        assert np.max(np.abs(I.B.T @ cur_flow)) < 1e-10, "Flow conservation has been broken"

        min_ratio, min_ratio_cycle = find_min_ratio_cycle(I, cur_flow)

        cur_flow += min_ratio_cycle

        print("min_ratio =", min_ratio)
        print("min_ratio_cycle =", min_ratio_cycle)
        print("  -> edges:", [I.edges[e]
              for e, c in enumerate(min_ratio_cycle) if c != 0])
        print(f"flow ({cur_flow[flow_idx]}): ", cur_flow)
        print("original flow:", cur_flow[:original_m])

        new_phi = I.phi(cur_flow)
        assert new_phi < float('inf'), "Φ(f) has exploded"
        # assert new_phi < cur_phi, "Φ(f) has not decreased"
        cur_phi = new_phi

        print()

    print("rounded flow:", np.round(cur_flow[:original_m]))

    return round(cur_flow[flow_idx])


def max_flow(edges: list[Tuple[int, int]], capacities: list[int], s: int, t: int, lower_capacities: list[int] = None):
    max_possible_flow = sum(capacities[e]
                            for e, (u, _) in enumerate(edges) if u == s)

    low, high = 0, max_possible_flow
    mf = None
    while low < high:
        mid = (low + high) // 2
        mf = max_flow_with_guess(
            edges, capacities, s=s, t=t, optimal_flow=mid, lower_capacities=lower_capacities)

        if mf < mid:
            high = mid
        else:
            low = mid + 1

    # TODO: fix this, I'm pretty sure this can be off by one
    return low


if __name__ == "__main__":
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

    edges = [e[0] for e in graph]
    capacities = [c[1] for c in graph]

    ans = max_flow(edges, capacities, s=0, t=5)

    print("Found max flow:", ans)
