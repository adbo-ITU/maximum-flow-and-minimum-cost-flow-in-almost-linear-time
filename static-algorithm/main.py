from typing import Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class MinCostFlow:
    m: int
    n: int
    edges: list[Tuple[int, int]]
    c: np.ndarray
    u_upper: np.ndarray
    u_lower: np.ndarray
    optimal_cost: int
    B: np.ndarray

    def __init__(
        self,
        edges: list[Tuple[int, int]],
        c: np.ndarray,
        u_lower: np.ndarray,
        u_upper: np.ndarray,
        optimal_cost: int
    ) -> None:
        self.m = len(edges)
        self.n = len(set(v for e in edges for v in e)) + 1
        self.edges = edges
        self.c = c
        self.u_lower = u_lower
        self.u_upper = u_upper
        self.optimal_cost = optimal_cost

        self.B = np.zeros((self.m, self.n), dtype=int)
        for e, (a, b) in enumerate(edges):
            self.B[e, a] = 1
            self.B[e, b] = -1

    def print_B(self):
        print(f"{'vertices:': >10} ", ' '.join(
            [f"{i: >2}" for i in range(self.n)]))
        for e, row in enumerate(self.B):
            print(f"{e: <2} {str(self.edges[e]): <7}", row)

    @staticmethod
    def from_max_flow_instance(edges: list[Tuple[int, int]], s: int, t: int, optimal_flow: int, capacities: list[int]):
        new_edges = edges + [(s, t)]

        c = np.array([0] * len(new_edges) + [-1])
        u_lower = np.zeros(len(new_edges), dtype=int)
        u_upper = np.array(capacities + [sum(capacities)])

        I = MinCostFlow(edges=new_edges, u_lower=u_lower,
                        u_upper=u_upper, c=c, optimal_cost=-optimal_flow)

        return I

    def phi(self, f: np.ndarray) -> float:
        objective = ...
        barrier = ...
        return objective + barrier

    def calc_gradients(self, f: np.ndarray) -> np.ndarray:
        ...

    def calc_lengths(self, f: np.ndarray) -> np.ndarray:
        ...


def max_flow(edges: list[Tuple[int, int]], capacities: list[int], s: int, t: int, optimal_flow: int):
    I = MinCostFlow.from_max_flow_instance(
        edges, s, t, optimal_flow, capacities)

    print(I)


if __name__ == "__main__":
    edges = [
        (1, 2),
        (1, 4),
        (3, 1),
        (4, 2),
        (6, 3),
        (6, 4),
        (2, 5),
        (5, 6),
    ]

    capacities = [3, 2, 2, 1, 1, 1, 2, 3]

    max_flow(edges, capacities, s=1, t=6, optimal_flow=3)
