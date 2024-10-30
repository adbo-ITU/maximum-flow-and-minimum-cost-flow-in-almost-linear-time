from typing import Tuple
from cycle import find_min_ratio_cycle
from min_cost_flow_instance import MinCostFlow
from feasible_flow import calc_feasible_flow


def max_flow_with_guess(edges: list[Tuple[int, int]], capacities: list[int], s: int, t: int, optimal_flow: int, lower_capacities: list[int] = None):
    I = MinCostFlow.from_max_flow_instance(
        edges=edges, s=s, t=t, optimal_flow=optimal_flow, capacities=capacities, lower_capacities=lower_capacities)

    print(I)
    print()
    I.print_B()
    print()

    before_m = I.m

    I, cur_flow = calc_feasible_flow(I)

    print(I)
    print()
    I.print_B()
    print()

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
        print("original flow:", cur_flow[:before_m])
        print()

    return cur_flow[-1]


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

    return mf


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
