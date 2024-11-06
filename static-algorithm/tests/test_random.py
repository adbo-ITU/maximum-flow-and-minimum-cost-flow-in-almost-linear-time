from main import max_flow_with_guess
from tests.find_max_flow import find_max_flow
from tests.utils import make_edges_and_capacities
from tests.verifier import assert_valid_solution
import pytest


@pytest.mark.slow
def test_flow_random_dag_184():
    graph, s, t = parse_input(INPUT_184)
    edges, capacities, _ = make_edges_and_capacities(graph)
    mf, flows = max_flow_with_guess(edges, capacities, s=s, t=t, optimal_flow=184)
    assert_valid_solution(graph, s, t, flows, mf)


@pytest.mark.slow
def test_flow_random_dag_51():
    graph, s, t = parse_input(INPUT_51)
    edges, capacities, _ = make_edges_and_capacities(graph)
    mf, flows = max_flow_with_guess(edges, capacities, s=s, t=t, optimal_flow=51)
    assert_valid_solution(graph, s, t, flows, mf)


def test_rikos_code():
    edges, s, t = parse_input(INPUT_184)
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


INPUT_184 = """
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

INPUT_51 = """
24 45 0 23
0-(4)>1
0-(27)>2
0-(33)>3
0-(32)>4
0-(17)>5
1-(31)>6
1-(29)>8
2-(11)>7
2-(26)>8
2-(6)>9
2-(15)>10
3-(8)>7
3-(42)>10
4-(28)>7
4-(3)>8
4-(44)>9
4-(32)>10
5-(36)>6
5-(46)>7
5-(50)>8
6-(10)>13
6-(34)>14
7-(25)>13
7-(39)>14
8-(20)>12
8-(24)>13
9-(15)>11
9-(42)>12
9-(2)>13
10-(11)>11
10-(36)>13
12-(13)>15
12-(38)>16
14-(17)>17
15-(11)>18
15-(48)>19
16-(24)>18
16-(50)>19
18-(11)>20
18-(28)>22
19-(13)>21
19-(41)>22
20-(29)>23
21-(33)>23
22-(46)>23
"""
