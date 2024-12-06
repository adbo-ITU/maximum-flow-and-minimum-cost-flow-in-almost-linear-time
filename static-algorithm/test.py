from dataclasses import dataclass
from typing import List, Tuple, TypeVar
from enum import Enum

# Type variables for generic implementations
T = TypeVar("T", float, int)
V = TypeVar("V")  # Vertex type
E = TypeVar("E")  # Edge type


class Color(Enum):
    WHITE = 0
    BLACK = 1


@dataclass
class Edge:
    """Edge in weighted directed graph"""

    source: int
    target: int
    weight1: float  # First weight (cost)
    weight2: float = 1.0  # Second weight (time/denominator)

    def __repr__(self):
        return (
            f"Edge({self.source}->{self.target}, w1={self.weight1}, w2={self.weight2})"
        )


class Graph:
    """Directed graph with weighted edges"""

    def __init__(self, num_vertices: int):
        self.V = num_vertices
        self.edges: List[Edge] = []
        self.adj: List[List[int]] = [[] for _ in range(num_vertices)]
        self.in_edges: List[List[int]] = [[] for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight1: float, weight2: float = 1.0) -> int:
        """Add edge with weights. Returns edge index."""
        edge_id = len(self.edges)
        self.edges.append(Edge(u, v, weight1, weight2))
        self.adj[u].append(edge_id)
        self.in_edges[v].append(edge_id)
        return edge_id

    def num_edges(self) -> int:
        return len(self.edges)


class MCRFloat:
    """Floating point utilities for minimum/maximum cycle ratio"""

    @staticmethod
    def infinity() -> float:
        return float("inf")

    @staticmethod
    def epsilon() -> float:
        return -0.005


class MinComparatorProps:
    """Properties for minimum ratio computation"""

    @staticmethod
    def compare(x: float, y: float) -> bool:
        return x > y

    multiplier = 1


class MaxComparatorProps:
    """Properties for maximum ratio computation"""

    @staticmethod
    def compare(x: float, y: float) -> bool:
        return x < y

    multiplier = -1


class HowardMCR:
    """Howard's algorithm for computing minimum/maximum cycle ratio"""

    def __init__(self, graph: Graph, comparator_props, float_traits=MCRFloat):
        self.g = graph
        self.cmp = comparator_props.compare
        self.multiplier = comparator_props.multiplier
        self.float_traits = float_traits

        self.V = graph.V
        self.distances = [0.0] * self.V
        self.policy = [-1] * self.V  # Current edge choice for each vertex
        self.colors = [Color.WHITE] * self.V
        self.bad_vertices = [False] * self.V

        # In-edges lists for policy graph
        self.in_edges_list = [[] for _ in range(self.V)]

        self.sink = None  # Special vertex for handling vertices with no outgoing edges
        self.bound = self._compute_bound()
        self.best_ratio = self.bound

    def _compute_bound(self) -> float:
        """Compute bound for cycle ratio"""
        closest_to_zero = float("inf")
        sum_weights = 0.0

        for edge in self.g.edges:
            sum_weights += abs(edge.weight1)
            w2_abs = abs(edge.weight2)
            if w2_abs > 1e-10 and w2_abs < closest_to_zero:
                closest_to_zero = w2_abs

        return self.multiplier * (sum_weights / closest_to_zero)

    def _construct_policy_graph(self):
        """Construct initial policy graph"""
        for v in range(self.V):
            best_edge = None
            best_weight = -float("inf") if self.multiplier == 1 else float("inf")

            for edge_id in self.g.adj[v]:
                edge = self.g.edges[edge_id]
                if self.cmp(edge.weight1, best_weight):
                    best_weight = edge.weight1
                    best_edge = edge_id

            if best_edge is None:
                if self.sink is None:
                    self.sink = v
                self.bad_vertices[v] = True
                self.in_edges_list[self.sink].append(v)
            else:
                target = self.g.edges[best_edge].target
                self.in_edges_list[target].append(v)
                self.policy[v] = best_edge

    def _find_cycle_vertex(self, start: int) -> int:
        """Find vertex that belongs to a cycle in policy graph"""
        current = start
        visited = set()

        while current not in visited:
            visited.add(current)
            if not self.bad_vertices[current]:
                current = self.g.edges[self.policy[current]].target
            else:
                current = self.sink

        return current

    def _compute_cycle_ratio(self, start: int) -> float:
        """Compute ratio of cycle starting at given vertex"""
        if start == self.sink:
            return self.bound

        sum_w1 = 0.0
        sum_w2 = 0.0
        current = start
        cycle_edges = []

        while True:
            edge = self.g.edges[self.policy[current]]
            cycle_edges.append(edge)
            sum_w1 += edge.weight1
            sum_w2 += edge.weight2
            current = edge.target
            if current == start:
                break

        ratio = sum_w1 / sum_w2
        if self.cmp(self.best_ratio, ratio):
            self.best_ratio = ratio
            self.critical_cycle = cycle_edges

        return ratio

    def _improve_policy(self, current_ratio: float) -> bool:
        """Try to improve current policy"""
        improved = False
        eps = self.float_traits.epsilon()

        for v in range(self.V):
            if not self.bad_vertices[v]:
                for edge_id in self.g.adj[v]:
                    edge = self.g.edges[edge_id]
                    target = edge.target
                    new_dist = (
                        edge.weight1
                        - current_ratio * edge.weight2
                        + self.distances[target]
                    )

                    if self.cmp(self.distances[v] + eps, new_dist):
                        # Update policy
                        old_target = self.g.edges[self.policy[v]].target
                        self.in_edges_list[old_target].remove(v)
                        self.policy[v] = edge_id
                        self.in_edges_list[target].append(v)
                        self.distances[v] = new_dist
                        improved = True
            else:
                new_dist = self.bound - current_ratio + self.distances[self.sink]
                if self.cmp(self.distances[v] + eps, new_dist):
                    self.distances[v] = new_dist

        return improved

    def find_optimum_cycle_ratio(self) -> Tuple[float, List[Edge]]:
        """
        Find optimum (minimum/maximum) cycle ratio.
        Returns (ratio, critical_cycle).
        """
        self._construct_policy_graph()

        iteration = 0
        while iteration < 100:  # Limit iterations to avoid infinite loops
            # Find current ratio
            ratio = float("inf")
            critical_vertex = None

            for v in range(self.V):
                if self.colors[v] == Color.WHITE:
                    cycle_vertex = self._find_cycle_vertex(v)
                    curr_ratio = self._compute_cycle_ratio(cycle_vertex)
                    if self.cmp(ratio, curr_ratio):
                        ratio = curr_ratio
                        critical_vertex = cycle_vertex

            # Try to improve policy
            if not self._improve_policy(ratio):
                break

            iteration += 1

        if self.cmp(ratio, self.bound - 1e-10):
            return float("inf"), []
        else:
            return ratio, self.critical_cycle


def minimum_cycle_ratio(g: Graph) -> Tuple[float, List[Edge]]:
    """Find minimum cycle ratio in graph"""
    howard = HowardMCR(g, MinComparatorProps)
    return howard.find_optimum_cycle_ratio()


def maximum_cycle_ratio(g: Graph) -> Tuple[float, List[Edge]]:
    """Find maximum cycle ratio in graph"""
    howard = HowardMCR(g, MaxComparatorProps)
    return howard.find_optimum_cycle_ratio()


def minimum_cycle_mean(g: Graph) -> Tuple[float, List[Edge]]:
    """Find minimum cycle mean (ratio with all w2=1)"""
    # Create new graph with all w2=1
    g_mean = Graph(g.V)
    for edge in g.edges:
        g_mean.add_edge(edge.source, edge.target, edge.weight1, 1.0)
    return minimum_cycle_ratio(g_mean)


def maximum_cycle_mean(g: Graph) -> Tuple[float, List[Edge]]:
    """Find maximum cycle mean (ratio with all w2=1)"""
    g_mean = Graph(g.V)
    for edge in g.edges:
        g_mean.add_edge(edge.source, edge.target, edge.weight1, 1.0)
    return maximum_cycle_ratio(g_mean)


# Example usage
def main():
    # Create example graph
    g = Graph(4)

    # Add edges (source, target, weight1, weight2)
    g.add_edge(0, 1, 2, 1)
    g.add_edge(1, 2, 3, 1)
    g.add_edge(2, 3, -6, 1)
    g.add_edge(3, 1, 2, 1)

    # Find minimum cycle ratio
    ratio, cycle = minimum_cycle_ratio(g)
    print(f"Minimum cycle ratio: {ratio}")
    print("Critical cycle:")
    for edge in cycle:
        print(f"{edge.source}->{edge.target} (w1={edge.weight1}, w2={edge.weight2})")

    # Create example graph
    g = Graph(4)

    # Add edges (source, target, weight1, weight2)
    g.add_edge(0, 1, 3, 0)
    g.add_edge(1, 2, 99, 2)
    g.add_edge(1, 3, 9, 3)
    g.add_edge(3, 2, 8, 2)
    g.add_edge(2, 0, 7, 2)

    # Find minimum cycle ratio
    ratio, cycle = minimum_cycle_ratio(g)
    print(f"Minimum cycle ratio: {ratio}")
    print("Critical cycle:")
    for edge in cycle:
        print(f"{edge.source}->{edge.target} (w1={edge.weight1}, w2={edge.weight2})")


if __name__ == "__main__":
    main()
