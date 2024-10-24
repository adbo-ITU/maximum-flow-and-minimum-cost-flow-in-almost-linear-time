from typing import Tuple
import networkx as nx


AdjacencyList = dict[int, list[int]]
SpanningTree = list[Tuple[int, int]]


def make_undirected_adjacency_list(edges: list[Tuple[int, int]]) -> AdjacencyList:
    adj_list = {}
    for v, u in edges:
        if v not in adj_list:
            adj_list[v] = []

        if u not in adj_list:
            adj_list[u] = []

        adj_list[v].append(u)
        adj_list[u].append(v)

    return adj_list


def find_spanning_tree(edges: AdjacencyList) -> SpanningTree:
    spanning_tree = []
    visited = set()

    def dfs(v):
        visited.add(v)
        for u in edges[v]:
            if u not in visited:
                spanning_tree.append((v, u))
                dfs(u)

    dfs(list(edges.keys())[0])

    return spanning_tree


"""
As a first observation, we show that if we sample a random “low-stretch”
spanning tree of the graph, then with constant probability, some fundamental
tree cycle approximately solves the min-ratio cycle problem. Recall a
fundamental tree cycle is a cycle defined by a single non-tree edge and the
unique tree path between its endpoints. Unfortunately, this simple approach
fails after a single flow update, as the IPM requires us to change the
gradients and lengths after each update.

https://cacm.acm.org/research-highlights/almost-linear-time-algorithms-for-maximum-flow-and-minimum-cost-flow/
"""
def find_all_simple_cycles(in_edges: list[Tuple[int, int]]):
    edges = make_undirected_adjacency_list(in_edges)

    spanning_tree_edges = find_spanning_tree(edges)
    spanning_tree = make_undirected_adjacency_list(spanning_tree_edges)

    non_tree_edges = set(in_edges)
    for u, v in spanning_tree_edges:
        non_tree_edges.discard((u, v))
        non_tree_edges.discard((v, u))

    def find_cycle_from_edge(non_tree_edge: Tuple[int, int]):
        a, b = non_tree_edge

        cycle = [a, b]
        queue = deque([a, b])
        visited = set()

        while queue:
            v = queue.popleft()
            visited.add(v)

            for u in spanning_tree[v]:
                if u in queue:
                    return cycle

                if u in visited:
                    continue

                queue.append(u)
                cycle.append(u)

        raise ValueError("Cycle not found")

    # TODO: can a single off tree edge create multiple cycles?
    cycles = []
    for non_tree_edge in non_tree_edges:
        cycle = find_cycle_from_edge(non_tree_edge)
        cycles.append(cycle)


    print(spanning_tree)
    print(non_tree_edges)
    print(cycles)
