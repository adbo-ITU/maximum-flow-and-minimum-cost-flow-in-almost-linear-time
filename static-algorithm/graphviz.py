from min_cost_flow_instance import MinCostFlow
from typing import Tuple, List, Optional


def get_dot_edge(edge: Tuple[int, int], lower: int, upper: int, cost: int, flow: Optional[int] = None):
    label = []
    label.append(f'caps={lower}/{upper}')
    label.append(f'cost={cost}')
    if flow is not None:
        label.append(f'flow={flow}')

    u, v = edge
    return f'{u} -> {v} [label="' + '\\n'.join(label) + '"];'


def get_dot_graph(I: MinCostFlow, flow: Optional[List[int]] = None):
    lines = []

    for i in range(I.n):
        lines.append(f'{i} [label="{i}"];')

    for i, edge in enumerate(I.edges):
        lines.append(get_dot_edge(
            edge,
            I.u_lower[i],
            I.u_upper[i],
            I.c[i],
            flow[i] if flow is not None else None
        ))

    return lines


def get_dot(I: MinCostFlow, flow: Optional[List[int]] = None):
    lines = []
    lines.append("rankdir=LR;")
    lines.extend(get_dot_graph(I, flow))
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
