from optparse import check_choice
import numpy as np
from min_cost_flow_instance import MinCostFlow

INF = float("inf")
EPS = -0.005


class Howard:
    graph: MinCostFlow
    flow: np.ndarray
    multiplier: int

    p_policy: list[float]
    p_dist: list[float]
    p_target: list[int]
    p_weight: list[float]
    p_transit: list[float]
    p_visited: list[int]

    def __init__(self, graph: MinCostFlow, f: np.ndarray):
        self.graph = graph
        self.flow = f
        self.multiplier = 1

        self.p_policy = [INF] * graph.n
        self.p_dist = [INF] * graph.n
        self.p_policy = [-1] * graph.n
        self.p_target = [-1] * graph.n
        self.p_weight = [-1] * graph.n
        self.p_transit = [-1] * graph.n
        self.p_visited = [-1] * graph.n

    def find_ratio(self, start_lambda: float) -> tuple[float, int, list[int]]:
        best_node = -1
        cur_lambda = start_lambda
        cycle_vertices: list[int] = []

        for v in range(self.graph.n):
            if self.p_visited[v] != -1:
                continue

            u = v
            while True:
                self.p_visited[u] = v
                u = self.p_target[u]

                if self.p_visited[u] != -1:
                    break

            if self.p_visited[u] != v:
                continue  # u is on an old cycle

            start_node = u
            current_cycle: list[int] = []
            total_weight = 0.0
            total_length = 0.0
            while True:
                current_cycle.append(u)
                total_length += 1
                total_weight += self.p_weight[u]
                u = self.p_target[u]
                if u == start_node:
                    break

            new_lambda = total_weight / total_length
            if new_lambda < cur_lambda:
                cur_lambda = new_lambda
                best_node = u
                cycle_vertices = current_cycle

        return cur_lambda, best_node, cycle_vertices

    def min_ratio_cycle(self, lambda_so_far: float = INF) -> tuple[float, list[int]]:
        # Create the initial policy graph

        gradients = self.graph.calc_gradients(self.flow)
        lengths = self.graph.calc_lengths(self.flow)

        for (u, v), edge_indices in self.graph.undirected_edge_to_indices.items():
            for edge_index in edge_indices:
                w = gradients[edge_index]

                if w < self.p_dist[u]:
                    self.p_dist[u] = w
                    self.p_policy[u] = edge_index
                    self.p_target[u] = v
                    self.p_weight[u] = w

                    edge = self.graph.edges[edge_index]
                    if edge[0] == u:
                        self.p_transit[u] = lengths[edge_index]
                    else:
                        self.p_transit[u] = -lengths[edge_index]

        cur_lambda = lambda_so_far
        check_limit = self.graph.n
        check_count = 0
        final_cycle_vertices = []

        while True:
            self.p_visited = [-1] * self.graph.n

            # find ratio
            cur_lambda, best_node, cycle_vertices = self.find_ratio(cur_lambda)

            if best_node == -1:
                check_count += 1
                if check_count > check_limit:
                    break
            else:
                check_count = 0
                final_cycle_vertices = cycle_vertices

                q: list[int] = []
                q.append(best_node)
                self.p_visited[best_node] = -1

                while q:
                    v = q.pop()

                    for edge_index in self.graph.edge_endpoints[v]:
                        u = self.graph.edges[edge_index][0]

                        if self.p_visited[u] == -1 or self.p_target[u] != v:
                            continue

                        self.p_visited[u] = -1
                        self.p_dist[u] = (
                            self.p_dist[v]
                            + self.p_weight[u]
                            - cur_lambda * self.p_transit[u]
                        )
                        q.append(u)

            not_improved = True

            for i, (u, v) in enumerate(self.graph.edges):
                new_dist = self.p_dist[v] + gradients[i] - cur_lambda * lengths[i]

                if EPS < self.p_dist[u] - new_dist:
                    not_improved = False

                    self.p_dist[u] = new_dist
                    self.p_policy[u] = i
                    self.p_target[u] = v
                    self.p_weight[u] = gradients[i]
                    self.p_transit[u] = lengths[i]

            if not_improved:
                break
        return cur_lambda, final_cycle_vertices
