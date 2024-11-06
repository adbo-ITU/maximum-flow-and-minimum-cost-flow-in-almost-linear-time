import min_ratio

m = min_ratio.MinRatioCycleFinder([[1, 2], [3, 4]])

x = m.find_min_ratio_cycle(
    gradients=[1, 2],
    lengths=[1, 3],
)
print(x)
