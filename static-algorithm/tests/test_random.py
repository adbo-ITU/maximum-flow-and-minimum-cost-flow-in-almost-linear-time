from main import max_flow_with_guess
from tests.find_max_flow import find_max_flow
from tests.utils import make_edges_and_capacities
import pytest


@pytest.mark.slow
def test_flow_random_dag():
    edges, s, t = parse_input(INPUT)
    edges, capacities, _ = make_edges_and_capacities(edges)
    mf, _ = max_flow_with_guess(edges, capacities, s=s, t=t, optimal_flow=184)
    assert mf == 184


def test_rikos_code():
    edges, s, t = parse_input(INPUT)
    edges, capacities, _ = make_edges_and_capacities(edges)
    mf, _ = find_max_flow(edges, capacities, s=s, t=t)
    assert mf == 184


def parse_input(input):
    lines = input.strip().split("\n")
    n, m, s, t = map(int, lines[0].split())
    edges = []
    for line in lines[1:]:
        u, rest = line.split("-(")
        cap, v = rest.split(")>")
        edges.append(((int(u), int(v)), int(cap)))
    return edges, s, t


INPUT = """
16 34 0 15
0-(66)>1
0-(99)>2
0-(42)>3
1-(43)>5
2-(72)>4
2-(62)>5
3-(23)>4
3-(44)>5
4-(41)>6
4-(84)>9
5-(19)>6
5-(21)>7
5-(84)>8
5-(12)>9
6-(44)>10
6-(32)>11
6-(33)>12
6-(28)>13
6-(79)>14
7-(19)>10
7-(23)>11
7-(28)>12
8-(40)>12
8-(80)>13
8-(78)>14
9-(53)>10
9-(86)>11
9-(4)>13
9-(62)>14
10-(99)>15
11-(12)>15
12-(8)>15
13-(27)>15
14-(46)>15
"""
