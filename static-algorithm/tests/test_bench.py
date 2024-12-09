from main import max_flow_with_guess
from flows import find_max_flow
from tests.utils import make_edges_and_capacities
from tests.verifier import assert_valid_solution
from tests.test_random import parse_input
import pytest
import pathlib
from typing import List


def eval_files(files: List[str]):
    paths = []
    for file in files:
        paths.append(pathlib.Path(__file__).parent.parent / "data" / file)

    inps = []

    for path in paths:
        with open(path) as f:
            content = f.read()
        inps.append(parse_input(content))

    for inp in inps:
        graph, s, t = inp
        print("Running test for", len(graph), "edges")
        edges, capacities, _ = make_edges_and_capacities(graph)

        actual_max_flow = find_max_flow(edges, capacities, s=s, t=t)
        mf, flows = max_flow_with_guess(
            edges, capacities, s=s, t=t, optimal_flow=actual_max_flow
        )
        assert mf == actual_max_flow, f"Expected max flow {actual_max_flow}, got {mf}"

    return inps


@pytest.mark.slow
def test_bench_dag():
    files = [
        "dag_edges_25.txt",
        "dag_edges_50.txt",
        "dag_edges_100.txt",
        "dag_edges_150.txt",
        "dag_edges_200.txt",
        "dag_edges_250.txt",
        "dag_edges_500.txt",
    ]

    inps = eval_files(files)

    # https://regex101.com/r/o5upRj/1
    iters = [
        # s=500
        # 2764,
        # 5233,
        # 9606,
        # 13590,
        # 18379,
        # 22444,
        # 43833
        # s=250
        5546,
        10477,
        19311,
        26056,
        34962,
        42735,
        86379,
        108309,
        # s=100
        # 13891,
        # 25899,
        # 48290,
        # 67708,
        # 88824
    ]


@pytest.mark.slow
def test_bench_fully_connected():
    files = [
        "fully_connected_edges_20.txt",
        "fully_connected_edges_90.txt",
        "fully_connected_edges_210.txt",
        "fully_connected_edges_380.txt",
    ]

    inps = eval_files(files)

    # https://regex101.com/r/o5upRj/1
    iters = [
        # s=500
        # 1718,
        # 7444,
        # 16436,
        # 29487,
        # s=250
        # 3453,
        # 15137,
        # 33584,
        # 60861
        # s=100
        8658,
        37737,
        80423,
        145301,
    ]

    make_pgfplots_coords(inps, iters)


def make_pgfplots_coords(inps, iters):
    # lines = ["Edges & IPM iterations"]
    coords = []
    for inp, its in zip(inps, iters):
        graph, s, t = inp
        coords.append(f"({len(graph)},{its})")

        # lines.append(f"{len(graph)} & {its} \\\\")

    print("".join(coords))
