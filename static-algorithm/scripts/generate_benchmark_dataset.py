import random
import pathlib
from dataclasses import dataclass


@dataclass
class DagParams:
    min_per_rank: int # Nodes/Rank: How 'fat' the DAG should be
    max_per_rank: int
    min_ranks: int # Ranks: How 'tall' the DAG should be
    max_ranks: int
    percent: float # Chance of having an Edge
    min_weight: int
    max_weight: int

    num_edges: int
    seed: int


def generate_random_dag(config: DagParams):
    random.seed(config.seed)

    source = 0
    nodes = 1
    node_counter = 1

    MIN_PER_RANK = config.min_per_rank
    MAX_PER_RANK = config.max_per_rank
    MIN_RANKS = config.min_ranks
    MAX_RANKS = config.max_ranks
    PERCENT = config.percent
    MIN_WEIGHT = config.min_weight
    MAX_WEIGHT = config.max_weight

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

    num_edge_error = 0.05
    NUM_EDGES = config.num_edges
    assert NUM_EDGES * (1 - num_edge_error) <= len(adjacency) <= NUM_EDGES * (1 + num_edge_error), f"Want {NUM_EDGES} edges, got {len(adjacency)}"

    lines = [f"{nodes} {len(adjacency)} {source} {sink}"]
    for u, v, cap in adjacency:
        lines.append(f"{u}-({cap})>{v}")

    return "\n".join(lines)


def generate_fully_connected_graph(seed: int, num_vertices: int):
    random.seed(seed)

    MIN_WEIGHT = 1
    MAX_WEIGHT = 50

    adjacency = []

    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                continue
            weight = random.randint(MIN_WEIGHT, MAX_WEIGHT)
            adjacency.append((i, j, weight))

    s, t = 0, num_vertices - 1

    lines = [f"{num_vertices} {len(adjacency)} {s} {t}"]
    for u, v, cap in adjacency:
        lines.append(f"{u}-({cap})>{v}")

    return "\n".join(lines)


if __name__ == "__main__":
    SEED = 2

    configs = [
        DagParams(
            num_edges=25,
            min_per_rank=4,
            max_per_rank=7,
            min_ranks=3,
            max_ranks=3,
            percent=0.7,
            min_weight=1,
            max_weight=50,
            seed=SEED
        ),
        DagParams(
            num_edges=50,
            min_per_rank=7,
            max_per_rank=10,
            min_ranks=3,
            max_ranks=3,
            percent=0.7,
            min_weight=1,
            max_weight=50,
            seed=SEED
        ),
        DagParams(
            num_edges=100,
            min_per_rank=9,
            max_per_rank=13,
            min_ranks=3,
            max_ranks=3,
            percent=0.7,
            min_weight=1,
            max_weight=50,
            seed=SEED
        ),
        DagParams(
            num_edges=150,
            min_per_rank=11,
            max_per_rank=17,
            min_ranks=3,
            max_ranks=3,
            percent=0.75,
            min_weight=1,
            max_weight=50,
            seed=SEED
        ),
        DagParams(
            num_edges=200,
            min_per_rank=14,
            max_per_rank=18,
            min_ranks=3,
            max_ranks=3,
            percent=0.70,
            min_weight=1,
            max_weight=50,
            seed=SEED
        ),
        DagParams(
            num_edges=250,
            min_per_rank=16,
            max_per_rank=19,
            min_ranks=3,
            max_ranks=3,
            percent=0.70,
            min_weight=1,
            max_weight=50,
            seed=SEED
        ),
        DagParams(
            num_edges=500,
            min_per_rank=25,
            max_per_rank=28,
            min_ranks=3,
            max_ranks=3,
            percent=0.70,
            min_weight=1,
            max_weight=50,
            seed=SEED
        )
    ]

    itms = []

    for config in configs:
        itms.append((f"dag_edges_{config.num_edges}.txt", generate_random_dag(config)))

    for n in [5, 10, 15, 20]:
        inp = generate_fully_connected_graph(SEED, n)
        m = inp.split("\n")[0].split()[1]
        itms.append((f"fully_connected_edges_{m}.txt", inp))

    for filename, inp in itms:
        path = pathlib.Path(__file__).parent.parent / "data" / filename
        with open(path, "w") as f:
            f.write(inp)
            print(f"Wrote to {path}")
