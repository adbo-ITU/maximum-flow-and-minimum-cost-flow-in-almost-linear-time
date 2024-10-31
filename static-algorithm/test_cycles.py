from cycle import find_all_cycles
from min_cost_flow_instance import MinCostFlow
from typing import List, Tuple
import sys
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

    # abusable but works
    correct_cycles = [set([0, 1]), set([2, 3, 1]), set([2, 3, 0])]
    cycles = find_all_cycles(create_dummy_instance(edges))
    print(cycles, correct_cycles)
    assert len(cycles) == 3
    assert all(set(cycle) in correct_cycles for cycle in cycles)


def test_triangle_two_pairs():
    edges = [
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
    ]

    # 0 -> 1 -> 0 (0,1)
    # 1 -> 2 -> 1 (2,3)
    # 0 -> 1 -> 2 -> 0 (0,2,4)
    # 0 -> 1 -> 2 -> 1 (1,2,4)
    # 0 -> 1 -> 2 -> 0 (0,3,4)

    # abusable but works, for now
    correct_cycles = [set([0, 1]), set([2, 3]), set(
        [4, 1, 2]), set([4, 0, 2]), set([4, 0, 3])]
    cycles = find_all_cycles(create_dummy_instance(edges))
    print(cycles, correct_cycles)
    assert len(cycles) == 5
    assert all(set(cycle) in correct_cycles for cycle in cycles)
