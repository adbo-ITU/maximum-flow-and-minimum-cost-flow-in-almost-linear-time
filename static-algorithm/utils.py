import os
from numpy.typing import NDArray
from numpy import float64

ENABLE_LOG = "ENABLE_LOG" in os.environ
ENABLE_EDGE_COUNT = "ENABLE_EDGE_COUNT" in os.environ
ENABLE_ALL_EDGE_COUNT = "ENABLE_ALL_EDGE_COUNT" in os.environ

EDGE_UPDATES: list[int] = []


def log(*args, **kwargs):
    if ENABLE_LOG:
        print(*args, **kwargs)


def reset_edge_updates():
    if ENABLE_EDGE_COUNT:
        EDGE_UPDATES.clear()


def count_edge_updates(cycle: NDArray[float64]):
    if ENABLE_EDGE_COUNT:
        count = sum(x != 0.0 for x in cycle)
        EDGE_UPDATES.append(count)


def print_edge_updates():
    if ENABLE_EDGE_COUNT:
        if ENABLE_ALL_EDGE_COUNT:
            print("Edge updates:", EDGE_UPDATES)
        print("Total edge updates:", sum(EDGE_UPDATES))
        print("Max edge updates:", max(EDGE_UPDATES))
        print("Min edge updates:", min(EDGE_UPDATES))
        print("Average edge updates:", sum(EDGE_UPDATES) / len(EDGE_UPDATES))
