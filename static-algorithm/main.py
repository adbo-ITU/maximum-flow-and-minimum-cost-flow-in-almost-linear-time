from typing import Tuple
import numpy as np


class Graph:
    m: int
    n: int
    edges: list[Tuple[int, int]]
    B: np.ndarray

    def __init__(self, edges: list[Tuple[int, int]]) -> None:
        self.m = len(edges)
        self.n = len(set(v for e in edges for v in e)) + 1
        self.edges = edges

        self.B = np.zeros((self.m, self.n), dtype=int)
        for e, (a, b) in enumerate(edges):
            self.B[e, a] = 1
            self.B[e, b] = -1

    def print_B(self):
        for e, row in enumerate(self.B):
            print(f"{e: <2} {str(self.edges[e]): <7}", row)


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

    G = Graph(edges)

    print(G.m, G.n)
    G.print_B()
