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
    U: int
    alpha: float
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
        self.U = max(np.max(np.abs(self.u_upper)),
                     np.max(np.abs(self.u_lower)))
        self.alpha = 1 / np.log2(1000 * self.m * self.U)

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
        left = (self.u_upper - f) ** (-1 - self.alpha)
        right = (f - self.u_lower) ** (-1 - self.alpha)
        return left - right


def max_flow(edges: list[Tuple[int, int]], capacities: list[int], s: int, t: int, optimal_flow: int):
    I = MinCostFlow.from_max_flow_instance(
        edges=edges, s=s, t=t, optimal_flow=optimal_flow, capacities=capacities)

    print(I)

    cur_flow = np.zeros(I.m, dtype=int)

    # TODO: change for loop to line 14 of algorithm 7 in the paper
    num_iters = 100
    for _ in range(num_iters):
        l = I.calc_lengths(cur_flow)
        g = I.calc_gradients(cur_flow)

        print("l", l)
        print("g", g)
        break


if __name__ == "__main__":
    # This is the example max-flow graph at https://www.geeksforgeeks.org/max-flow-problem-introduction/
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

    max_flow(edges, capacities, s=0, t=5, optimal_flow=23)
