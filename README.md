# BFS and DFS semester project

This project implements the approved comparison of Breadth-First Search and Depth-First Search in Python. It includes a working demonstration, correctness checks, reproducible experiments, measured data, figures, and documentation for the team's next step of writing a presentation script.

The team is David Byrke, Kenneth Stuckey, Matthew Godfrey, and Christopher Mai in Algorithm Analysis W02, taught by Prof. Femi Ojo. The project follows the supplied proposal and the D2L project topic, presentation outline, and report outline. The source code and recorded experiments in this folder were created and executed with Codex assistance on November 17, 2026. Team members should run the demo and review the evidence before presenting it.

## Start here

Open this folder in VS Code and use Python 3.10 or later. Commands below assume the terminal is in this folder. The verified experiment used Python 3.12.14 on Windows. The core project uses only Python's standard library.

```powershell
python demo.py
python -m unittest -v
```

Read `docs/PRESENTATION_HANDOFF.md` next. It maps the instructor's slide sections to the implementation, figures, results, demo, and remaining team decisions. `results/FINDINGS.md` contains the actual measured results and their limitations.

## Reproduce the experiments

The measured CSVs and figures are included, so they can be reviewed without installing plotting packages. To regenerate them on your computer, install Matplotlib in a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe benchmark.py --output results_rerun
.\.venv\Scripts\python.exe plot_results.py --results results_rerun
.\.venv\Scripts\python.exe demo.py --output results_rerun/demo.json
```

The original evidence stays in `results/`. A small verification benchmark can be run with `python benchmark.py --quick --output results_quick`. It uses fewer graph sizes and one random seed. The full benchmark is the basis for the supplied findings.

## Files

| File | Purpose |
|---|---|
| `algorithms.py` | Graph representation, BFS, explicit-stack DFS, parent paths, shortest path, connected components |
| `graphs.py` | Seven deterministic graph families and the small demo graph |
| `demo.py` | Live traversal, shortest-path, unreachable-node, and connected-component examples |
| `benchmark.py` | Repeated runtime trials, separate memory trials, validations, graph fingerprints, environment capture |
| `plot_results.py` | Regenerates four PNG figures and the measured-results note |
| `test_project.py` | Independent correctness oracles and boundary cases |
| `docs/METHODS.md` | Implementation decisions, pseudocode, complexity, experimental method, limitations |
| `docs/PRESENTATION_HANDOFF.md` | Evidence map, proposed slide order, demo plan, likely questions, next steps |
| `docs/SOURCES_AND_REQUIREMENTS.md` | Proposal scope, D2L requirements, verified source links, bibliography corrections |
| `results/runtime_trials.csv` | 990 individual runtime records, with timing batch sizes |
| `results/memory_trials.csv` | 330 individual peak-allocation records |
| `results/summary.csv` | 110 per-graph, per-algorithm summaries |
| `results/environment.json` | Environment, parameters, 55 graph fingerprints |
| `results/demo.json` | Exact recorded demo inputs and outputs |
| `results/validation.txt` | Output from the verification run |
| `results/build_record.json` | SHA-256 fingerprints of the Python source files used for this delivery |
| `results/figures/` | Runtime, traced memory, frontier shape, and demo path figures |

## Use the algorithms with another graph

```python
from algorithms import Graph, bfs, dfs, connected_components, shortest_path

graph = Graph.from_edges(5, [(0, 1), (0, 2), (2, 3)])
print(bfs(graph, source=0).order)
print(dfs(graph, source=0).order)
print(shortest_path(graph, 0, 3))  # [0, 2, 3]
print(shortest_path(graph, 0, 4))  # None
print(connected_components(graph))  # includes isolated vertex 4
```

Vertices use integer labels from 0 through n-1. Build graphs with `Graph.from_edges` so endpoints are validated, repeated edges are deduplicated, and neighbor order is deterministic. `directed=True` supports directed reachability and unweighted shortest paths. Connected-component grouping requires undirected graphs. The measured experiments use undirected, loop-free, unweighted graphs.

`bfs` and `dfs` normally visit only the source's reachable vertices. Set `full=True` to restart from every remaining unvisited vertex. `SearchResult.depth` gives tree depth for both algorithms. BFS tree depth equals shortest-path distance. A DFS tree path can be longer.

## Presentation and report status

The live presentation window ends November 21, 2026. The presentation upload is due November 21 at 11:59 p.m. Eastern and the final report is due November 30 at 11:59 p.m. Eastern. The team still needs to confirm its Teams slot, assign speakers, rehearse, write the script, build the slides, incorporate this evidence into the shared report, and submit the required deliverables. Those decisions and submissions are outside this code package.

The measured results describe these implementations on the recorded machine. BFS was faster on all 55 paired graphs in this run. Both algorithms perform O(V + E) full traversal work. Graph shape changes queue size and stack depth, and the demo shows BFS's shortest-path guarantee on unweighted graphs. See the detailed caveats in `docs/METHODS.md` and `results/FINDINGS.md` before using these claims.
