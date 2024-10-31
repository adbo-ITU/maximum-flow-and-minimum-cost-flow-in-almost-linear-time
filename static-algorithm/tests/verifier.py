from tests.utils import make_edges_and_capacities, Graph
from tests.find_max_flow import find_max_flow


def assert_valid_solution(graph: Graph, s: int, t: int, flow: list[int], flow_value: int):
    edges, capacities, lower_capacities = make_edges_and_capacities(graph)

    print("Flow:", flow)

    if lower_capacities:
        raise Exception("No no. Only basic flow instances here.")

    actual_max_flow, _ = find_max_flow(edges, capacities, s=s, t=t)

    assert actual_max_flow == flow_value, f"Expected max flow {flow_value}, got {actual_max_flow}"

    flow_from_s, flow_to_t = 0, 0
    for e, (u, v) in enumerate(edges):
        if u == s:
            flow_from_s += flow[e]
        if v == t:
            flow_to_t += flow[e]

    assert flow_from_s == flow_value, f"Flow from s = {flow_from_s}, expected {flow_value}"
    assert flow_from_s == flow_to_t, f"Flow conservation not satisfied: flow from s = {flow_from_s}, flow to t = {flow_to_t}"

    assert_flow_is_valid(edges, capacities, flow=flow, s=s, t=t)


def assert_flow_is_valid(edges: list[tuple[int, int]], capacities: list[int], flow: list[int], s: int, t: int):
    vertices = set(v for e in edges for v in e)
    vertex_flows = {v: 0 for v in vertices}

    for e, (u, v) in enumerate(edges):
        assert flow[e] >= 0, f"Flow {flow[e]} on edge {u} -> {v} is negative"
        assert flow[e] <= capacities[e], f"Flow {flow[e]} on edge {u} -> {v} exceeds capacity {capacities[e]}"

        vertex_flows[u] -= flow[e]
        vertex_flows[v] += flow[e]

    for v, f in vertex_flows.items():
        if v == s:
            assert f == -sum(flow[e] for e, (u, _) in enumerate(edges)
                             if u == s), "Flow from s does not match"
        elif v == t:
            assert f == sum(flow[e] for e, (_, v) in enumerate(
                edges) if v == t), "Flow to t does not match"
        else:
            assert f == 0, f"Flow conservation broken at vertex {v}: has {f} flow"
