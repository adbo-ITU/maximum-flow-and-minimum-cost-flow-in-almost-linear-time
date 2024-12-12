import os
import sys


def get_params(file: str) -> list[int]:
    with open(file, "r") as f:
        line = f.readline()
        params = [int(x) for x in line.split()]
        return params


def convert_to_russian(file: str) -> list[str]:
    result: list[str] = []

    with open(file, "r") as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            split = lines[i].split()
            result.append(f"{split[0]}-({split[2]})>{split[1]}")

    return result


def get_solution(file: str) -> int:
    with open(file.replace(".in", ".ans"), "r") as f:
        line = f.readline()
        return int(line.split()[1])


def get_name(i: int, solution: int, params: list[int]) -> str:
    return f"{i:03}_{params[0]}_{params[1]}_{solution}.txt"


if __name__ == "__main__":
    folder = sys.argv[1]
    out = sys.argv[2]

    files: list[tuple[int, str, list[int], int]] = []

    for file in os.listdir(folder):
        if not file.endswith(".in"):
            continue

        file = os.path.join(folder, file)

        params = get_params(file)
        edges = convert_to_russian(file)
        solution = get_solution(file)

        file_contents: list[str] = []
        file_contents.append(" ".join(map(str, params)))
        file_contents.extend(edges)

        if params[1] <= 1 or params[1] > 1000:
            continue

        files.append((params[1], "\n".join(file_contents), params, solution))

    files.sort()
    pytest_tuples: list[str] = []
    for i, (_, content, params, solution) in enumerate(files):
        name = get_name(i, solution, params)
        out_path = os.path.join(out, name)
        with open(out_path, "w") as f:
            _ = f.write(content)
        out_path = out_path.replace("data/", "")
        pytest_tuples.append(f'("{out_path}", {solution})')

    print("Insert the following code into test_bench.py, over the existing code:")
    print(
        '@pytest.mark.parametrize("file,solution", [' + ", ".join(pytest_tuples) + "])"
    )
