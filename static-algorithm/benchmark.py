import time
import json
import numpy as np
from pathlib import Path

BENCH_INFO = {}
CUR_BENCH = None


def start_benchmark(id: str):
    global CUR_BENCH
    CUR_BENCH = id
    BENCH_INFO[CUR_BENCH] = {
        "start": time.time_ns()
    }


def register(key: str, value):
    if CUR_BENCH is None:
        return

    BENCH_INFO[CUR_BENCH][key] = value


def register_or_update(key: str, default, updater):
    if CUR_BENCH is None:
        return

    if key in BENCH_INFO[CUR_BENCH]:
        BENCH_INFO[CUR_BENCH][key] = updater(BENCH_INFO[CUR_BENCH][key])
    else:
        BENCH_INFO[CUR_BENCH][key] = default


def end_benchmark():
    global CUR_BENCH
    BENCH_INFO[CUR_BENCH]["end"] = time.time_ns()
    BENCH_INFO[CUR_BENCH]["duration_s"] = (BENCH_INFO[CUR_BENCH]["end"] - BENCH_INFO[CUR_BENCH]["start"]) / 1e9
    CUR_BENCH = None

    # so we have the data if we kill the program or it crashes
    write_benchmark(f"benchmark-tmp.json") 


def write_benchmark(filename: str | None = None):
    dir = Path("benches")
    dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"benchmark-{int(time.time())}.json"

    with open(dir / filename, "w") as f:
        json.dump(BENCH_INFO, f, cls=NpEncoder, indent=4)


class NpEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super(NpEncoder, self).default(o)
