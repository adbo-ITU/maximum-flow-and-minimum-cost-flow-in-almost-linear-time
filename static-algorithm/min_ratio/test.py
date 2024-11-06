import min_ratio

x = min_ratio.find_min_ratio_cycle(
    edge_cycles=[[1, 2], [3, 4]],
    gradients=[1, 2],
    lengths=[1, 3],
)
print(x)
