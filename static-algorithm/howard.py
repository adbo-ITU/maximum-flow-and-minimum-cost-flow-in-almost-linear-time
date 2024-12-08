import numpy as np
from numpy.typing import NDArray

from min_cost_flow_instance import MinCostFlow

INF = float("inf")
EPS = -0.005


class Howard:
    """Howard's algorithm for computing minimum/maximum cycle ratio"""

    g: MinCostFlow
    V: int
    distances: list[float]
    policy: list[int]
    bad_vertices: list[bool]  # Vertices with no outgoing edges.
    in_edges_list: list[list[int]]

    sink: int
    bound: float
    best_ratio: float

    critical_cycle: list[int] | None
    critical_vertex: int | None

    gradients: NDArray[np.float64]
    lengths: NDArray[np.float64]

    def __init__(
        self,
        graph: MinCostFlow,
        gradients: NDArray[np.float64],
        lengths: NDArray[np.float64],
    ):
        self.g = graph

        self.V = graph.n
        self.distances = [0.0] * self.V
        self.policy = [-1] * self.V  # Current edge choice for each vertex
        self.bad_vertices = [False] * self.V

        self.gradients = gradients
        self.lengths = lengths

        # In-edges lists for policy graph
        self.in_edges_list = [[] for _ in range(self.V)]

        self.sink = -1  # Special vertex for handling vertices with no outgoing edges
        self.bound = self._compute_bound()
        self.best_ratio = self.bound

        self.critical_cycle = None
        self.critical_vertex = None

    def _compute_bound(self) -> float:
        """Compute bound for cycle ratio"""
        closest_to_zero = INF
        sum_weights = 0.0

        for i in range(self.g.m):
            sum_weights += abs(float(self.gradients[i]))
            w2_abs = abs(float(self.lengths[i]))
            if w2_abs > 1e-10 and w2_abs < closest_to_zero:
                closest_to_zero = w2_abs

        return sum_weights / closest_to_zero

    def _get_gradient(self, start: int, edge_id: int) -> float:
        """Get gradient for given edge"""
        edge = self.g.edges[edge_id]
        if edge[0] == start:
            return -self.gradients[edge_id]
        else:
            return self.gradients[edge_id]

    def _get_edge_target(self, start: int, edge_id: int) -> int:
        """Get target vertex for given edge"""
        edge = self.g.edges[edge_id]
        if edge[0] == start:
            return edge[1]
        else:
            return edge[0]

    def _construct_policy_graph(self):
        """Construct initial policy graph"""
        for v in range(self.V):
            best_edge = -1
            best_weight: float = -INF

            for edge_id in self.g.adj[v]:
                gradient = self._get_gradient(v, edge_id)
                if gradient > best_weight:
                    best_weight = gradient
                    best_edge = edge_id

            if best_edge == -1:
                if self.sink == -1:
                    self.sink = v
                self.bad_vertices[v] = True
                self.in_edges_list[self.sink].append(v)
            else:
                target = self._get_edge_target(v, best_edge)
                self.in_edges_list[target].append(v)
                self.policy[v] = best_edge

    def _find_cycle_vertex(self, start: int) -> int:
        """Find vertex that belongs to a cycle in policy graph"""
        current: int = start
        visited: set[int] = set()

        while current not in visited:
            visited.add(current)
            if not self.bad_vertices[current]:
                current = self._get_edge_target(current, self.policy[current])
            else:
                current = self.sink

        return current

    def _compute_cycle_ratio(self, start: int) -> float:
        """Compute ratio of cycle starting at given vertex"""
        if start == self.sink:
            return self.bound

        sum_w1: float = 0.0
        sum_w2: float = 0.0
        current = start
        cycle_edges: list[int] = []

        while True:
            edge_id = self.policy[current]
            cycle_edges.append(edge_id)
            sum_w1 += self._get_gradient(current, edge_id)
            sum_w2 += self.lengths[edge_id]
            current = self._get_edge_target(current, edge_id)
            if current == start:
                break

        ratio = sum_w1 / sum_w2
        if self.best_ratio > ratio:
            self.best_ratio = ratio
            self.critical_vertex = start
            self.critical_cycle = cycle_edges

        return ratio

    def _improve_policy(self, current_ratio: float) -> bool:
        """Try to improve current policy"""
        improved = False

        for v in range(self.V):
            if not self.bad_vertices[v]:
                for edge_id in self.g.adj[v]:
                    target = self._get_edge_target(v, edge_id)
                    new_dist: float = (
                        self._get_gradient(v, edge_id)
                        - current_ratio * self.lengths[edge_id]
                        + self.distances[target]
                    )

                    if self.distances[v] + EPS > new_dist:
                        # Update policy
                        old_target = self._get_edge_target(v, self.policy[v])
                        self.in_edges_list[old_target].remove(v)
                        self.policy[v] = edge_id
                        self.in_edges_list[target].append(v)
                        self.distances[v] = new_dist
                        improved = True
            else:
                new_dist = self.bound - current_ratio + self.distances[self.sink]
                if self.distances[v] + EPS > new_dist:
                    self.distances[v] = new_dist

        return improved

    def find_optimum_cycle_ratio(self) -> tuple[float, NDArray[np.float64]]:
        """
        Find optimum (minimum/maximum) cycle ratio.
        Returns (ratio, critical_cycle).
        """
        self._construct_policy_graph()

        iteration = 0
        ratio = INF

        while iteration < 100:  # Limit iterations to avoid infinite loops
            # Find current ratio
            ratio = INF

            for v in range(self.V):
                cycle_vertex = self._find_cycle_vertex(v)
                curr_ratio = self._compute_cycle_ratio(cycle_vertex)
                if ratio > curr_ratio:
                    ratio = curr_ratio

            # Try to improve policy
            if not self._improve_policy(ratio):
                break

            iteration += 1

        if ratio > self.bound - 1e-10 or self.critical_cycle is None:
            return INF, np.zeros(self.g.m, dtype=np.float64)
        else:
            return ratio, self._numpy_cycle()

    def _numpy_cycle(self) -> NDArray[np.float64]:
        """Convert cycle to edge representation"""

        if self.critical_cycle is None or self.critical_vertex is None:
            return np.zeros(self.g.m, dtype=np.float64)

        edge_cycle = np.zeros(self.g.m, dtype=np.float64)
        current = self.critical_vertex

        for edge_id in self.critical_cycle:
            target = self._get_edge_target(current, edge_id)

            edge_cycle[edge_id] = 1.0 if current == self.g.edges[edge_id][0] else -1.0

            current = target

        return edge_cycle


def minimum_cycle_ratio(
    g: MinCostFlow,
    gradients: NDArray[np.float64],
    lengths: NDArray[np.float64],
) -> tuple[float, NDArray[np.float64]]:
    """Find minimum cycle ratio in graph"""
    howard = Howard(g, gradients, lengths)
    return howard.find_optimum_cycle_ratio()
