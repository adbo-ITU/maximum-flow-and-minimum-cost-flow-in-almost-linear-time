from .capacity_scaling import find_max_flow as cap_find_max_flow
from .edmond_karp import MaxFlow
from .push_relabel import PushRelabel
from tests.utils import Edge


def find_max_flow(edges: list[Edge], capacities: list[int], s: int, t: int):
    cap, _ = cap_find_max_flow(edges, capacities, s, t)
    edk = MaxFlow(edges, capacities).max_flow(s, t)
    pr = PushRelabel(edges, capacities).max_flow(s, t)

    assert cap == edk
    assert cap == pr

    return cap
