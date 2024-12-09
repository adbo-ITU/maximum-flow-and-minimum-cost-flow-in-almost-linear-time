from collections import defaultdict
from tests.utils import Edge
import utils

# all credit to Riko Jacob for this code


def find_max_flow(
    edges: list[Edge], capacities: list[int], s: int, t: int
) -> tuple[int, list[tuple[int, int, int]]]:
    graph: defaultdict[int, defaultdict[int, int]] = defaultdict(
        lambda: defaultdict(lambda: 0)
    )

    for (u, v), capacity in zip(edges, capacities):
        graph[u][v] = capacity

    max_flow, flow_graph, _ = flow(graph, s, t)

    flow_edges: list[tuple[int, int, int]] = []
    for u, d in flow_graph.items():
        for v, c in d.items():
            flow_edges.append((u, v, c))

    print(f"[CAPACITY] Max flow: {max_flow}")
    print("[CAPACITY] Flow edges:", flow_edges)

    return max_flow, flow_edges


def bfs(
    graph: defaultdict[int, defaultdict[int, int]], src: int, dest: int, mincap: int = 0
) -> tuple[bool, set[int] | list[tuple[int, int]]]:
    parent = {src: src}
    layer = [src]
    while layer:
        nextlayer: list[int] = []
        for u in layer:
            for v, cap in graph[u].items():
                if cap > mincap and v not in parent:
                    parent[v] = u
                    nextlayer.append(v)
                    if v == dest:
                        p: list[tuple[int, int]] = []
                        current_vertex = dest
                        while src != current_vertex:
                            p.append((parent[current_vertex], current_vertex))
                            current_vertex = parent[current_vertex]
                        return (True, p)
        layer = nextlayer
    return (False, set(parent))


def flow(
    orggraph: defaultdict[int, defaultdict[int, int]], src: int, dest: int
) -> tuple[int, defaultdict[int, defaultdict[int, int]], set[int]]:
    edge_updates: list[int] = []
    graph: defaultdict[int, defaultdict[int, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    maxcapacity = 0
    for u, d in orggraph.items():
        for v, c in d.items():
            graph[u][v] = c
            maxcapacity = max(maxcapacity, c)

    current_flow = 0
    mincap = maxcapacity
    while True:
        ispath, p_or_seen = bfs(graph, src, dest, mincap)
        if not ispath:
            if mincap > 0:
                mincap = mincap // 2
                continue
            else:
                if utils.ENABLE_EDGE_COUNT:
                    if utils.ENABLE_ALL_EDGE_COUNT:
                        print("[CAPACITY] Edge updates:", edge_updates)
                    print("[CAPACITY] Total edge updates:", sum(edge_updates))
                    print("[CAPACITY] Max edge updates:", max(edge_updates))
                    print("[CAPACITY] Min edge updates:", min(edge_updates))
                    print(
                        "[CAPACITY] Average edge updates:",
                        sum(edge_updates) / len(edge_updates),
                    )
                return (
                    current_flow,
                    {
                        a: {b: c - graph[a][b] for b, c in d.items() if graph[a][b] < c}
                        for a, d in orggraph.items()
                    },
                    p_or_seen,
                )
        p: list[tuple[int, int]] = p_or_seen
        saturation = min(graph[u][v] for u, v in p)
        current_flow += saturation
        edge_update = 0
        for u, v in p:
            edge_update += 2
            graph[u][v] -= saturation
            graph[v][u] += saturation

        if utils.ENABLE_EDGE_COUNT:
            edge_updates.append(edge_update)
