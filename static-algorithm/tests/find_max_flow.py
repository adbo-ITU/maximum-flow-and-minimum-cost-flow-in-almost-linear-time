from collections import defaultdict, deque
from tests.utils import Edge
import utils

# all credit to Riko Jacob for this code


def find_max_flow(edges: list[Edge], capacities: list[int], s: int, t: int):
    graph = defaultdict(lambda: defaultdict(lambda: 0))

    for (u, v), capacity in zip(edges, capacities):
        graph[u][v] = capacity

    max_flow, flow_graph, _ = flow(graph, s, t)

    flow_edges = []
    for u, d in flow_graph.items():
        for v, c in d.items():
            flow_edges.append((u, v, c))

    print(f"[CAPACITY] Max flow: {max_flow}")
    print("[CAPACITY] Flow edges:", flow_edges)

    return max_flow, flow_edges


def bfs(graph, src, dest, mincap=0):  # returns path to dest
    parent = {src: src}
    layer = [src]
    while layer:
        nextlayer = []
        for u in layer:
            for v, cap in graph[u].items():
                if cap > mincap and v not in parent:
                    parent[v] = u
                    nextlayer.append(v)
                    if v == dest:
                        p = []
                        current_vertex = dest
                        while src != current_vertex:
                            p.append((parent[current_vertex], current_vertex))
                            current_vertex = parent[current_vertex]
                        return (True, p)
        layer = nextlayer
    return (False, set(parent))


def flow(orggraph, src, dest):
    edge_updates: list[int] = []
    graph = defaultdict(lambda: defaultdict(int))
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
        p = p_or_seen
        saturation = min(graph[u][v] for u, v in p)
        # for i in range(len(p)-1):
        #     assert(p[i][0] == p[i+1][1])
        # print(current_flow,saturation,file=sys.stderr)#,[f"{u[0]}-{u[1]}:{inp[u[0]][u[1]]}:{graph[u][v]}" for u,v in p if u[2]==0])
        current_flow += saturation
        edge_update = 0
        for u, v in p:
            edge_update += 2
            graph[u][v] -= saturation
            graph[v][u] += saturation

        if utils.ENABLE_EDGE_COUNT:
            edge_updates.append(edge_update)


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
