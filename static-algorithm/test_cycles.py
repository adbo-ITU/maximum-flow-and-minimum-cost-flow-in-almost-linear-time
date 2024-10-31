from cycle import find_all_cycles
from min_cost_flow_instance import MinCostFlow
from typing import List, Tuple
import numpy as np


def create_dummy_instance(edges: List[Tuple[int, int]]):
    zeroes = np.zeros(len(edges))

    return MinCostFlow(
        edges,
        zeroes,
        zeroes,
        zeroes,
        0
    )


def test_triangle_one_pair():
    edges = [
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 0),
    ]

    cycles = find_all_cycles(create_dummy_instance(edges))
    assert len(cycles) == 3
    print(cycles)


def test_triangle_two_pairs():
    edges = [
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
    ]

    cycles = find_all_cycles(create_dummy_instance(edges))
    assert len(cycles) == 5
    print(cycles)
