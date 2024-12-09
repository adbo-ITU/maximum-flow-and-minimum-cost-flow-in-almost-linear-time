from main import max_flow, max_flow_with_guess
from tests.find_max_flow import find_max_flow
from tests.utils import make_edges_and_capacities
from tests.verifier import assert_valid_solution
from tests.test_random import parse_input
import pytest
import pathlib
from typing import List
import benchmark
from dataclasses import dataclass


def run_with_guess(edges, capacities, s, t, optimal_flow):
    return max_flow_with_guess(edges, capacities, s=s, t=t, optimal_flow=optimal_flow)

def run_with_binary_search(edges, capacities, s, t):
    return max_flow(edges, capacities, s=s, t=t)


@dataclass
class Config:
    file: str
    binary_search: bool = False
    scale_capacity: int = 1

    def id(self):
        h = hash((self.file, self.binary_search, self.scale_capacity))
        return f"{self.file}-{h}"

    def register_params(self):
        benchmark.register("bench_config", {
            "file": self.file,
            "binary_search": self.binary_search,
            "scale_capacity": self.scale_capacity
        })


def eval_files(configs: List[Config]):
    for config in configs:
        file = config.file
        path = pathlib.Path(__file__).parent.parent / "data" / file
        with open(path) as f:
            content = f.read()

        graph, s, t = parse_input(content)
        edges, capacities, _ = make_edges_and_capacities(graph)
        capacities = [c * config.scale_capacity for c in capacities]

        print("Running test for", len(graph), "edges")
        benchmark.start_benchmark(config.id())
        config.register_params()

        actual_max_flow, _ = find_max_flow(edges, capacities, s=s, t=t)

        if config.binary_search:
            mf, flows = max_flow(edges, capacities, s=s, t=t)
        else:
            mf, flows = max_flow_with_guess(edges, capacities, s=s, t=t, optimal_flow=actual_max_flow)

        benchmark.register("actual_max_flow", actual_max_flow)
        benchmark.register("max_flow_result", mf)
        benchmark.end_benchmark()

        # TODO: oopsie
        # assert mf == actual_max_flow, f"Expected max flow {actual_max_flow}, got {mf}"

    benchmark.write_benchmark()
    benchmark.clear()


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
    eval_files([Config(file=f) for f in DAG_FILES])


FULLY_CONNECTED_FILES = [
    "fully_connected_edges_20.txt",
    "fully_connected_edges_90.txt",
    "fully_connected_edges_210.txt",
    "fully_connected_edges_380.txt",
]


@pytest.mark.slow
def test_bench_fully_connected():
    eval_files([Config(file=f) for f in FULLY_CONNECTED_FILES])


@pytest.mark.slow
def test_bench_all():
    eval_files([Config(file=f) for f in DAG_FILES + FULLY_CONNECTED_FILES])


@pytest.mark.slow
def test_bench_binary_search():
    # TODO: vary U

    files = ["dag_edges_50.txt", "dag_edges_25.txt"]
    configs = []
    for f in files:
        for scale in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
            configs.append(Config(file=f, binary_search=True, scale_capacity=scale))

    eval_files(configs)
