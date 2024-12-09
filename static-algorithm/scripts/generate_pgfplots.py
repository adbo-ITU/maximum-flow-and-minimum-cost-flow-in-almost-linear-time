import sys
import json


def varying_capacity(benches):
    items = list(benches.values())
    items.sort(key=lambda x: x["bench_config"]["scale_capacity"])

    items = [x for x in items if x["bench_config"]["file"] == "dag_edges_50.txt"]

    xs = [x["bench_config"]["scale_capacity"] for x in items]
    ys = [x["iterations"] for x in items]

    print(make_pgfplots_coords(xs, ys))


def make_pgfplots_coords(xs, ys):
    return "".join([f"({x},{y})" for x, y in zip(xs, ys)])


if __name__ == "__main__":
    bench_path = sys.argv[1]

    with open(bench_path, "r") as f:
        benches = json.load(f)

    varying_capacity(benches)
