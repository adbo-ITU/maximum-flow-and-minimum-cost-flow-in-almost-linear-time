from dataclasses import dataclass
import random
import pathlib


@dataclass
class LineParams:
    min_weight: int
    max_weight: int

    num_edges: int
    seed: int


def generate_line(config: LineParams):
    random.seed(config.seed)

    upper_capacity = random.randint(config.min_weight, config.max_weight)

    n = config.num_edges + 1
    edges: list[tuple[int, int, int]] = []
    for i in range(config.num_edges):
        edges.append((i, i + 1, upper_capacity))

    assert len(edges) == config.num_edges
    assert edges[-1][1] == n - 1
    assert edges[0][0] == 0

    lines = [f"{n} {config.num_edges} 0 {n - 1}"]
    for u, v, cap in edges:
        lines.append(f"{u}-({cap})>{v}")

    return "\n".join(lines)


if __name__ == "__main__":
    SEED = 2

    configs = [
        LineParams(num_edges=25, min_weight=1, max_weight=50, seed=SEED),
        LineParams(num_edges=50, min_weight=1, max_weight=50, seed=SEED),
        LineParams(num_edges=100, min_weight=1, max_weight=50, seed=SEED),
        LineParams(num_edges=150, min_weight=1, max_weight=50, seed=SEED),
        LineParams(num_edges=200, min_weight=1, max_weight=50, seed=SEED),
        LineParams(num_edges=250, min_weight=1, max_weight=50, seed=SEED),
        LineParams(num_edges=500, min_weight=1, max_weight=50, seed=SEED),
    ]

    items = []

    for config in configs:
        items.append((f"line_edges_{config.num_edges}.txt", generate_line(config)))

    for filename, inp in items:
        path = pathlib.Path(__file__).parent.parent / "data" / filename
        with open(path, "w") as f:
            f.write(inp)
            print(f"Wrote to {path}")
