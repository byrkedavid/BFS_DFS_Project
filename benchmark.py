"""Measure identical full traversals with separate runtime and memory trials."""

import argparse
import csv
import gc
import hashlib
import json
import platform
import statistics
import sys
import time
import tracemalloc
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from algorithms import search
from graphs import make_graph

FAMILIES = ("path", "star", "grid", "disconnected")


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def validate_full(graph, result):
    assert len(result.order) == graph.n
    assert set(result.order) == set(range(graph.n))
    assert result.edge_checks == graph.adjacency_entries
    for v, parent in result.parent.items():
        if parent is not None:
            assert v in graph.adjacency[parent]
            assert result.depth[v] == result.depth[parent] + 1
            assert result.component[v] == result.component[parent]


def runtime_trial(graph, method, batch):
    # No graph generation, sorting, validation, or memory tracing in this timer.
    enabled = gc.isenabled()
    gc.disable()
    try:
        start = time.perf_counter_ns()
        for _ in range(batch):
            result = search(graph, method=method, full=True)
        elapsed = time.perf_counter_ns() - start
    finally:
        if enabled:
            gc.enable()
    return elapsed / batch / 1_000_000, result


def memory_trial(graph, method):
    # Input adjacency lists already exist before tracing starts. Returned state,
    # visited maps, frontier, iterators, and allocations during traversal count.
    gc.collect()
    tracemalloc.start(1)
    try:
        result = search(graph, method=method, full=True)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return peak, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--trials", type=int, default=9)
    parser.add_argument("--memory-trials", type=int, default=3)
    parser.add_argument("--quick", action="store_true", help="Small verification run")
    args = parser.parse_args()
    if args.trials < 3 or args.memory_trials < 1:
        parser.error("Use at least 3 runtime trials and 1 memory trial")
    args.output.mkdir(parents=True, exist_ok=True)
    sizes = [100, 500] if args.quick else [100, 500, 1000, 2500, 5000]
    runtime_rows, memory_rows = [], []
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "command": sys.argv,
        "clock": vars(time.get_clock_info("perf_counter")),
        "runtime_trials": args.trials,
        "memory_trials": args.memory_trials,
        "sizes": sizes,
        "source_hashes": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(__file__).parent.glob("*.py"))
        },
        "graph_hashes": [],
        "scope": "Full traversals, undirected unweighted simple graphs, source 0; ascending neighbors",
    }
    for family in FAMILIES:
        family_seeds = [2026]
        for n in sizes:
            for seed in family_seeds:
                graph = make_graph(family, n, seed)
                base = {"family": family, "vertices": n, "edges": graph.edges,
                        "adjacency_entries": graph.adjacency_entries, "seed": seed}
                digest = hashlib.sha256(json.dumps(graph.adjacency).encode()).hexdigest()
                manifest["graph_hashes"].append({**base, "sha256": digest})
                batch_sizes = {}
                for method in ("bfs", "dfs"):
                    validate_full(graph, search(graph, method=method, full=True))
                    # Two untimed warmups, then calibrate each algorithm to a
                    # batch near 5 ms. Record batch size for audit/reproduction.
                    search(graph, method=method, full=True)
                    elapsed, _ = runtime_trial(graph, method, 1)
                    batch_sizes[method] = max(1, min(100, int(5 / max(elapsed, 0.001))))
                for trial in range(args.trials):
                    order = ("bfs", "dfs") if trial % 2 == 0 else ("dfs", "bfs")
                    for method in order:
                        batch = batch_sizes[method]
                        ms, result = runtime_trial(graph, method, batch)
                        validate_full(graph, result)
                        runtime_rows.append({**base, "method": method, "trial": trial + 1,
                                             "batch": batch, "runtime_ms": ms,
                                             "visited": len(result.order),
                                             "edge_checks": result.edge_checks,
                                             "max_frontier": result.max_frontier,
                                             "components": len(result.roots)})
                for trial in range(args.memory_trials):
                    for method in (("bfs", "dfs") if trial % 2 == 0 else ("dfs", "bfs")):
                        peak, result = memory_trial(graph, method)
                        validate_full(graph, result)
                        memory_rows.append({**base, "method": method, "trial": trial + 1,
                                            "peak_bytes": peak})
                print(f"Measured {family:12} V={n:5} E={graph.edges:6} seed={seed}", flush=True)
    groups = defaultdict(list)
    memory_groups = defaultdict(list)
    key_names = ("family", "vertices", "edges", "adjacency_entries", "seed", "method")
    for row in runtime_rows:
        groups[tuple(row[k] for k in key_names)].append(row)
    for row in memory_rows:
        memory_groups[tuple(row[k] for k in key_names)].append(row["peak_bytes"])
    summaries = []
    for key, rows in groups.items():
        times = [r["runtime_ms"] for r in rows]
        summaries.append({**dict(zip(key_names, key)),
                          "runtime_median_ms": statistics.median(times),
                          "runtime_min_ms": min(times), "runtime_max_ms": max(times),
                          "peak_median_bytes": statistics.median(memory_groups[key]),
                          "max_frontier": rows[0]["max_frontier"],
                          "visited": rows[0]["visited"],
                          "edge_checks": rows[0]["edge_checks"],
                          "components": rows[0]["components"]})
    write_csv(args.output / "runtime_trials.csv", runtime_rows)
    write_csv(args.output / "memory_trials.csv", memory_rows)
    write_csv(args.output / "summary.csv", summaries)
    (args.output / "environment.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Saved {len(manifest['graph_hashes'])} graphs and {len(summaries)} algorithm summaries")


if __name__ == "__main__":
    main()
