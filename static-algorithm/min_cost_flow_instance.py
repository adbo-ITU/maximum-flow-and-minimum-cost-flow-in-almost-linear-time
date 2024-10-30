from dataclasses import dataclass
from typing import Tuple
import numpy as np


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

    undirected_edge_to_indices: dict[Tuple[int, int], list[int]]

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
        self.c_org = c
        self.u_lower = u_lower
        self.u_upper = u_upper
        self.optimal_cost = optimal_cost
        self.U = max(np.max(np.abs(self.u_upper)),
                     np.max(np.abs(self.u_lower)))
        self.alpha = 1 / np.log2(1000 * self.m * self.U)

        rand_cost = np.random.randint(
            1, 2*self.m*self.U+1, size=self.m) / (4 * self.m**2 * self.U**2)

        self.c = c + rand_cost

        assert len(
            self.edges) == self.m, f"Number of elements does not match: len(edges) = {len(self.edges)}, m = {self.m}"
        assert len(
            self.c) == self.m, f"Number of elements does not match: len(c) = {len(self.c)}, m = {self.m}"
        assert len(
            self.u_lower) == self.m, f"Number of elements does not match: len(u_lower) = {len(self.u_lower)}, m = {self.m}"
        assert len(
            self.u_upper) == self.m, f"Number of elements does not match: len(u_upper) = {len(self.u_upper)}, m = {self.m}"

        self.B = np.zeros((self.m, self.n), dtype=int)
        for e, (a, b) in enumerate(edges):
            self.B[e, a] = 1
            self.B[e, b] = -1

        self.undirected_edge_to_indices = {}
        for e, (a, b) in enumerate(edges):
            if (a, b) not in self.undirected_edge_to_indices:
                self.undirected_edge_to_indices[(a, b)] = []
            if (b, a) not in self.undirected_edge_to_indices:
                self.undirected_edge_to_indices[(b, a)] = []
            self.undirected_edge_to_indices[(a, b)].append(e)
            self.undirected_edge_to_indices[(b, a)].append(e)

    def print_B(self):
        print(f"{'vertices:': >10} ", ' '.join(
            [f"{i: >2}" for i in range(self.n)]))
        for e, row in enumerate(self.B):
            print(f"{e: <2} {str(self.edges[e]): <7}", row)

    @staticmethod
    def from_max_flow_instance(edges: list[Tuple[int, int]], s: int, t: int, optimal_flow: int, capacities: list[int]):
        new_edges = edges + [(t, s)]

        c = np.zeros(len(new_edges), dtype=float)
        c[-1] = -1
        u_lower = np.zeros(len(new_edges), dtype=float)
        u_upper = np.array(capacities + [sum(capacities)])

        I = MinCostFlow(edges=new_edges, u_lower=u_lower,
                        u_upper=u_upper, c=c, optimal_cost=-optimal_flow)

        return I

    def phi(self, f: np.ndarray) -> float:
        cur_cost = np.dot(self.c, f)

        objective = 20 * self.m * np.log2(cur_cost - self.optimal_cost)

        upper_barriers = (self.u_upper - f) ** (-self.alpha)
        lower_barriers = (f - self.u_lower) ** (-self.alpha)
        barrier = np.sum(upper_barriers + lower_barriers)

        phi = objective + barrier
        if phi == float('inf'):
            raise Exception("Φ has exploded")

        return phi

    def calc_gradients(self, f: np.ndarray) -> np.ndarray:
        cur_cost = np.dot(self.c, f)

        objective = 20 * self.m * \
            ((cur_cost - self.optimal_cost) ** (-1)) * self.c

        left = self.alpha * (self.u_upper - f) ** (-1 - self.alpha)
        right = self.alpha * (f - self.u_lower) ** (-1 - self.alpha)

        return objective + left - right

    def calc_lengths(self, f: np.ndarray) -> np.ndarray:
        left = (self.u_upper - f) ** (-1 - self.alpha)
        right = (f - self.u_lower) ** (-1 - self.alpha)
        return left + right

    def edges_between(self, a: int, b: int) -> list[int]:
        return self.undirected_edge_to_indices[(a, b)]

    def add_vertex(self):
        self.n += 1
        self.B = np.pad(self.B, ((0, 0), (0, 1)),
                        mode='constant', constant_values=0)

        return self.n-1

    def add_edge(self, a: int, b: int, c: int, u_lower: int, u_upper: int):
        # FIXME: This might be really slow
        assert a < self.n
        assert b < self.n

        self.edges.append((a, b))
        if (a, b) not in self.undirected_edge_to_indices:
            self.undirected_edge_to_indices[(a, b)] = []
        if (b, a) not in self.undirected_edge_to_indices:
            self.undirected_edge_to_indices[(b, a)] = []
        self.undirected_edge_to_indices[(a, b)].append(len(self.edges)-1)
        self.undirected_edge_to_indices[(b, a)].append(len(self.edges)-1)

        self.m += 1
        self.c = np.append(self.c, c)
        self.u_lower = np.append(self.u_lower, u_lower)
        self.u_upper = np.append(self.u_upper, u_upper)
        self.B = np.pad(self.B, ((0, 1), (0, 0)),
                        mode='constant', constant_values=0)
        self.B[-1, a] = 1
        self.B[-1, b] = -1
