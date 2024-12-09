from main import max_flow_with_guess
from tests.find_max_flow import find_max_flow
from tests.utils import make_edges_and_capacities
from tests.verifier import assert_valid_solution
from tests.test_random import parse_input
import pytest
import pathlib
from typing import List
import benchmark


def eval_files(files: List[str]):
    for file in files:
        path = pathlib.Path(__file__).parent.parent / "data" / file
        with open(path) as f:
            content = f.read()

        graph, s, t = parse_input(content)
        print("Running test for", len(graph), "edges")
        edges, capacities, _ = make_edges_and_capacities(graph)

        actual_max_flow, _ = find_max_flow(edges, capacities, s=s, t=t)

        benchmark.start_benchmark(file)
        mf, flows = max_flow_with_guess(edges, capacities, s=s, t=t, optimal_flow=actual_max_flow)
        benchmark.end_benchmark()

        assert mf == actual_max_flow, f"Expected max flow {actual_max_flow}, got {mf}"

    benchmark.write_benchmark()


DAG_FILES = [
    "dag_edges_25.txt",
    "dag_edges_50.txt",
    "dag_edges_100.txt",
    "dag_edges_150.txt",
    "dag_edges_200.txt",
    "dag_edges_250.txt",
    "dag_edges_500.txt"
]


@pytest.mark.slow
def test_bench_dag():
    eval_files(DAG_FILES)


FULLY_CONNECTED_FILES = [
    "fully_connected_edges_20.txt",
    "fully_connected_edges_90.txt",
    "fully_connected_edges_210.txt",
    "fully_connected_edges_380.txt",
]

@pytest.mark.slow
def test_bench_fully_connected():
    eval_files(FULLY_CONNECTED_FILES)


@pytest.mark.slow
def test_bench_all():
    eval_files(DAG_FILES + FULLY_CONNECTED_FILES)


def make_pgfplots_coords(inps, iters):
    # lines = ["Edges & IPM iterations"]
    coords = []
    for inp, its in zip(inps, iters):
        graph, s, t = inp
        coords.append(f"({len(graph)},{its})")

        # lines.append(f"{len(graph)} & {its} \\\\")

    print("".join(coords))
