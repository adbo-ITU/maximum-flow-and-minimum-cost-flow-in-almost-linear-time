from typing import Tuple
from howard import minimum_cycle_ratio
from min_cost_flow_instance import MinCostFlow
from feasible_flow import calc_feasible_flow
import numpy as np
from utils import log


def max_flow_with_guess(
    edges: list[Tuple[int, int]],
    capacities: list[int],
    s: int,
    t: int,
    optimal_flow: int,
    lower_capacities: list[int] = None,
):
    I = MinCostFlow.from_max_flow_instance(
        edges=edges,
        s=s,
        t=t,
        optimal_flow=optimal_flow,
        capacities=capacities,
        lower_capacities=lower_capacities,
    )

    log("Initial instance:")
    log(I)
    log()
    I.print_B()
    log()

    original_m = I.m
    flow_idx = original_m - 1
    I, cur_flow = calc_feasible_flow(I)

    log("Feasible flow instance:")
    log(I)
    log("initial_flow:", cur_flow)
    log()
    I.print_B()
    log()

    # TODO: Understand why the paper's threshold is too small
    # threshold = float(I.m * I.U) ** (-10)
    threshold = 1e-5
    log("Threshold:", threshold)

    kappa = 0.9999
    upscale = 500

    i = 0
    cur_phi = I.phi(cur_flow)
    while I.c.dot(cur_flow) - I.optimal_cost >= threshold:
        i += 1
        log("Iteration", i)
        log("Φ(f) =", cur_phi)

        assert (
            np.max(np.abs(I.B.T @ cur_flow)) < 1e-10
        ), "Flow conservation has been broken"

        gradients = I.calc_gradients(cur_flow)
        lengths = I.calc_lengths(cur_flow)

        min_ratio, min_ratio_cycle = minimum_cycle_ratio(I, gradients, lengths)

        eta = -kappa**2 / (50 * gradients.dot(min_ratio_cycle))
        augment_cycle = min_ratio_cycle * (eta * upscale)

        cur_flow += augment_cycle

        log("min_cycle_ratio =", min_ratio)
        log("min_ratio_cycle =", augment_cycle)
        log(
            "  -> cycle_edges:",
            [I.edges[e] for e, c in enumerate(min_ratio_cycle) if c != 0],
        )
        log(f"flow ({cur_flow[flow_idx]}): ", cur_flow)
        log("original flow:", cur_flow[:original_m])

        new_phi = I.phi(cur_flow)
        if not new_phi < float("inf"):
            log("Φ(f) has exploded")
            break
        # assert new_phi < float('inf'), "Φ(f) has exploded"
        # TODO: Understand why we don't always decrease Φ(f). Sign of gradient? Too large step?
        # assert new_phi < cur_phi, "Φ(f) has not decreased"
        cur_phi = new_phi

        log()

    log("rounded flow:", np.round(cur_flow[:original_m]))

    return round(cur_flow[flow_idx]), np.round(cur_flow[:flow_idx])


def max_flow(
    edges: list[Tuple[int, int]],
    capacities: list[int],
    s: int,
    t: int,
    lower_capacities: list[int] = None,
):
    max_possible_flow = sum(capacities[e] for e, (u, _) in enumerate(edges) if u == s)

    low, high = 0, max_possible_flow + 1
    mf, flows = None, None
    while low < high:
        mid = (low + high) // 2
        mf, flows = max_flow_with_guess(
            edges,
            capacities,
            s=s,
            t=t,
            optimal_flow=mid,
            lower_capacities=lower_capacities,
        )

        if mf < mid:
            high = mid
        else:
            low = mid + 1

    # TODO: fix this, I'm pretty sure this can be off by one
    return mf, flows


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
