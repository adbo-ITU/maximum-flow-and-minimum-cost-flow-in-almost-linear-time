from collections import defaultdict, deque
from tests.utils import Edge


def find_max_flow(edges: list[Edge], capacities: list[int], s: int, t: int):
    graph = defaultdict(lambda: defaultdict(lambda: 0))

    for (u, v), capacity in zip(edges, capacities):
        graph[u][v] = capacity

    max_flow, flow_graph, _ = find_max_flow_inner(graph, s, t)

    flow_edges = []
    for u, d in flow_graph.items():
        for v, c in d.items():
            flow_edges.append((u, v, c))

    print(f"Max flow: {max_flow}")
    print("Flow edges:", flow_edges)

    return max_flow, flow_edges


def bfs(graph, source, sink, min_capacity=0):
    parent = dict()
    queue = deque([source])

    while queue:
        u = queue.popleft()

        for v, capacity in graph[u].items():
            if capacity > min_capacity and v not in parent:
                parent[v] = u
                queue.append(v)

                if v == sink:
                    path = []
                    cur = sink
                    while source != cur:
                        prev = parent[cur]
                        path.append((prev, cur))
                        cur = prev

                    return (True, path)

    return (False, set(parent))


def find_max_flow_inner(original_graph, source, sink):
    graph = defaultdict(lambda: defaultdict(lambda: 0))
    max_capacity = 0

    for u, d in original_graph.items():
        for v, c in d.items():
            graph[u][v] = c
            max_capacity = max(max_capacity, c)

    current_flow = 0
    min_capacity = max_capacity
    while True:
        has_path, path = bfs(graph, source, sink, min_capacity)

        if not has_path:
            if min_capacity <= 0:
                cut = path
                return (current_flow, retain_only_active_edges(original_graph, graph), cut)

            min_capacity //= 2
            continue

        path_flow = min(graph[u][v] for u, v in path)
        current_flow += path_flow

        for u, v in path:
            graph[u][v] -= path_flow
            graph[v][u] += path_flow


def retain_only_active_edges(original_graph, graph):
    flow_graph = dict()

    for u, adj in original_graph.items():
        edges = dict()

        for v, capacity in adj.items():
            if graph[u][v] < capacity:
                edges[v] = capacity - graph[u][v]

        if len(edges):
            flow_graph[u] = edges

    return flow_graph
