import random


class Graph:
    nodes = []
    edges = []
    removed_edges = []

    def remove_edge(self, x, y):
        e = (x, y)
        try:
            self.edges.remove(e)
            # print("Removed edge %s" % str(e))
            self.removed_edges.append(e)
        except:
            return

    def Nodes(self):
        return self.nodes

    # Sample data
    def __init__(self):
        self.nodes = []
        self.edges = []


def get_random_source_sink_graph():
    MIN_PER_RANK = 2    # Nodes/Rank: How 'fat' the DAG should be
    MAX_PER_RANK = 10
    MIN_RANKS = 10   # Ranks: How 'tall' the DAG should be
    MAX_RANKS = 10
    PERCENT = 0.4  # Chance of having an Edge
    MIN_WEIGHT = 1
    MAX_WEIGHT = 100

    source = 0
    nodes = 1
    node_counter = 1

    ranks = random.randint(MIN_RANKS, MAX_RANKS)

    adjacency = []
    rank_list = []
    for i in range(ranks):
        if i == ranks - 1:
            sink = node_counter
            node_counter += 1
            nodes += 1
            for j in rank_list[i - 1]:
                weight = random.randint(MIN_WEIGHT, MAX_WEIGHT)
                adjacency.append((j, sink, weight))
            break

        # New nodes of 'higher' rank than all nodes generated till now
        new_nodes = random.randint(MIN_PER_RANK, MAX_PER_RANK)

        list = []
        for j in range(new_nodes):
            if i == 0:
                weight = random.randint(MIN_WEIGHT, MAX_WEIGHT)
                adjacency.append((source, node_counter, weight))
            list.append(node_counter)
            node_counter += 1
        rank_list.append(list)

        # Edges from old nodes ('nodes') to new ones ('new_nodes')
        if i > 0:
            for j in rank_list[i - 1]:
                for k in range(new_nodes):
                    if random.random() <= PERCENT:
                        weight = random.randint(MIN_WEIGHT, MAX_WEIGHT)
                        adjacency.append((j, k+nodes, weight))


        nodes += new_nodes

    print(nodes, len(adjacency), source, node_counter - 1)
    for u, v, cap in adjacency:
        print(f"{u}-({cap})>{v}")


get_random_source_sink_graph()
