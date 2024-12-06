from min_cost_flow_instance import MinCostFlow
from typing import Tuple, List, Optional
from tests.test_results import CP_ALGORITHMS_GRAPH, GEEKS_FOR_GEEKS_GRAPH, make_edges_and_capacities

def fmt_float(x: float):
    if x.is_integer():
        return str(int(x))
    return f'{x:.8f}'

def get_dot_edge(edge: Tuple[int, int], lower: int, upper: int, cost: int, flow: Optional[float] = None):
    label = []
    label.append(f'[uₑ⁻, uₑ⁺]=[{fmt_float(lower)}, {fmt_float(upper)}]')
    if flow is not None:
        label.append(f'ƒₑ={fmt_float(flow)}')
    label.append(f'cₑ={fmt_float(cost)}')

    u, v = edge
    return f'{u} -> {v} [label="' + r'\l'.join(label) + r'\l"];'


def get_dot_graph(I: MinCostFlow, flow: Optional[List[float]] = None, conf: dict = dict()):
    lines = []

    for i in range(I.n-1):
        label = f'{i}'
        shape = 'shape=circle'
        if i == conf.get('s', -1):
            label = "s = " + label
        if i == conf.get('t', -1):
            label = "t = " + label

        keys = [f'label="{label}"', shape]
        lines.append(f'{i} [{", ".join(keys)}];')

    for i, edge in enumerate(I.edges):
        lines.append(get_dot_edge(
            edge,
            I.u_lower[i],
            I.u_upper[i],
            I.c[i],
            flow[i] if flow is not None else None
        ))

    return lines


def get_dot(I: MinCostFlow, flow: Optional[List[float]] = None, conf: dict = dict()):
    lines = []
    # lines.append("rankdir=LR;")
    lines.append('graph [fontname = "Palatino"]');
    lines.append('node [fontname = "Palatino"]')
    lines.append('edge [fontname = "Palatino"]')
    lines.extend(get_dot_graph(I, flow, conf))
    lines = ["    " + line for line in lines]

    dot = "digraph G {\n"
    dot += "\n".join(lines)
    dot += "\n}"

    return dot


def get_the_russian_stuff(I: MinCostFlow):
    lines = []

    for i, edge in enumerate(I.edges):
        u, v = edge
        cap = I.u_upper[i]
        lines.append(f'{u}-({cap})>{v}')

    return "\n".join(lines)


if __name__ == "__main__":
    flow = [float(x) for x in """[6.65076594 3.34923224 1.34923285 4.9999994  2.99999939 1.99999939
 1.49999989 6.49999928 3.49999889 9.99999818]""".strip("[]").split()]


    LEL = CP_ALGORITHMS_GRAPH

    edges, capacities, _ = make_edges_and_capacities(LEL)

    conf = dict(s=0, t=5)
    I = MinCostFlow.from_max_flow_instance(
        edges=edges,
        capacities=capacities,
        s=conf['s'],
        t=conf['t'],
        optimal_flow=10
    )

    print(get_dot(I, flow, conf))
