# Implementation and experimental methods

This document explains the runnable program and the decisions behind the recorded experiment. It supports the methodology section of the report and the presentation's design and development slides. Exact measurements are in `../results/summary.csv` and `../results/FINDINGS.md`.

## Scope and assumptions

The approved proposal compares correctness, runtime, visited vertices, memory, graph structure, connected components, and unweighted shortest paths. The main experimental scope is simple undirected graphs with integer vertices. Edges have no weights. A factory creates sorted adjacency lists, which are stored as immutable tuples. Each non-loop undirected edge appears in two neighbor lists. The graph and its sorting are constructed before measurement.

The source vertex is 0. A single-source traversal visits only reachable vertices. The full traversal used for benchmarking restarts from ascending unvisited vertices until every vertex has been processed. This gives equal coverage on disconnected graphs and includes isolated vertices. The same graph object and ascending neighbor order are used for BFS and DFS.

The explicit DFS stack follows the same discovery order as recursive DFS. Each frame contains a vertex and an iterator over its remaining neighbors. Python call-stack limits therefore do not constrain long paths. The tests compare this order to a small independent recursive implementation.

## BFS logic

```text
discover the source and enqueue it
while the queue has vertices
    remove the oldest vertex u
    examine each neighbor v of u
    if v is undiscovered
        record u as parent of v
        record depth[v] as depth[u] + 1
        discover and enqueue v
```

Discovery happens when a vertex enters the queue. A vertex can therefore enter only once. The implementation uses collections.deque and popleft. List pop(0) would add avoidable shifting costs.

## DFS logic

```text
discover the source and push its neighbor iterator
while stack frames remain
    examine the next neighbor v from the top frame
    if the iterator is exhausted
        pop the frame
    otherwise if v is undiscovered
        record its parent and tree depth
        discover v and push its neighbor iterator
```

Every adjacency entry is consumed once. A frame remains active until all of that vertex's neighbors have been processed. This models recursion and backtracking directly. The metrics count iterator frames as stack depth.

## Correctness and applications

Both searches maintain a discovered map and return each reachable vertex once. Every recorded parent-child pair is an actual graph edge. For BFS, a vertex at distance k is discovered before any vertex at distance k+1 is removed for expansion, so the resulting parent path has the fewest edges. DFS provides a valid tree path and can choose a longer route first.

The connected-components function runs a full search on an undirected graph and groups vertices by their root. It rejects directed inputs because directed connectivity needs a separate definition and algorithm. Directed single-source reachability and shortest paths remain supported.

The demo has 10 vertices and 8 undirected edges. Vertex 0 reaches vertices 0 through 6. Vertices 7 and 8 form another component, and 9 is isolated. With ascending neighbors, BFS returns path [0, 6, 5] and DFS's tree path is [0, 1, 2, 3, 4, 5]. Target 9 is unreachable from 0. Both component methods partition all vertices into the same three sets.

## Complexity analysis

Let V be the vertex count and E the number of distinct undirected edges. Let A be the number of stored adjacency entries. The loop-free undirected benchmarks have A = 2E.

Each full traversal discovers V vertices, checks A neighbors, and performs O(V) queue or stack operations. Thus both take O(V + A), equivalent to O(V + E). Dictionary membership and updates are treated as expected constant time. The exact operation counter records A edge checks in both algorithms for every benchmark graph.

The graph uses O(V + E) input storage. Both returned results store O(V) order, parent, depth, and component data. The full traversal also creates an O(V) candidate-root list. The BFS queue can reach O(V) vertices and the DFS frame stack can reach O(V) depth, so total auxiliary space is O(V). Frontier size depends on graph shape. On a path BFS keeps at most one queued vertex while DFS holds the full path. On a star rooted at its center BFS queues almost all vertices while DFS needs only two active frames. These statements concern this implementation, source, and ordering.

Dense graphs have E proportional to V squared. O(V + E) then gives quadratic growth with V. Linear complexity in graph input size and quadratic growth with vertex count can both describe the same experiment.

## Graph families and input controls

| Family | Construction | Why included |
|---|---|---|
| Path | Consecutive vertices connected in a line | Deep DFS and narrow BFS frontier |
| Star | Vertex 0 linked to all other vertices | Wide BFS frontier and shallow DFS |
| Tree | Parent of vertex v is floor((v-1)/2) | Branching with logarithmic tree height |
| Grid | Near-square row-major layout with horizontal and vertical edges | Structured cycles and multiple routes |
| Sparse | A spanning path plus random extra edges, targeting 3V total edges | Connected cyclic graph with E proportional to V |
| Disconnected | Three separate interleaved-label paths plus an isolated vertex | Full coverage and component handling |
| Dense | Spanning path plus independent candidate edges with probability 0.15 | Edge-heavy graphs and quadratic E growth |

The sparse and dense generators deliberately include a spanning path for connectivity. Sorted neighbors can cause DFS to follow this long path, so random-family stack depths reflect that construction. These inputs are neither a uniform sample of all graphs nor a model of every real-world network.

Five vertex counts are used for each family. The first six use 100, 500, 1,000, 2,500, and 5,000. Dense graphs use 50, 100, 200, 400, and 800 to keep their larger edge sets practical. Sparse and dense families use seeds 2026, 2027, and 2028. Other families are deterministic and use one graph per size. This produces 55 graphs. Graph hashes and edge counts are saved in the environment file.

## Timing procedure

For each graph, run both algorithms and validate their output. Use two untimed warmups per algorithm, followed by a one-call timing calibration. Set a batch size near 5 milliseconds, bounded between 1 and 100 traversals. Each of nine runtime trials measures one batch using time.perf_counter_ns and divides its elapsed time by the batch size. BFS runs first on even-numbered trial indices and DFS first on odd ones. Garbage collection is disabled within each timed batch and restored afterward. Result creation, counters, result replacement, and associated cleanup are part of the measured work. Input generation, sorting, validation, plotting, and memory tracing are outside the timer.

Store every trial and its batch size. Summaries use the median of nine per-traversal times with observed minima and maxima. Random-family plots take a median across the three graph-specific medians. Deterministic-family points represent one graph's trial median. Differences are descriptive. The experiment does not establish statistical significance or universal performance rankings.

## Memory procedure

Run three memory measurements per algorithm and graph separately from timing. Collect garbage before each trial, start tracemalloc with one traceback frame, execute the full search, read its peak, and stop tracing. The input graph already exists before tracing starts. The result remains alive until the peak is read. Report the median peak bytes. This includes traversal-created Python allocations and the returned maps/lists. It excludes input graph storage, prior allocations, and process-level resident memory. A queue vertex and a DFS iterator frame occupy different numbers of bytes, so frontier counts should be interpreted alongside traced memory.

## Validation and evidence

Six unittest cases cover 1,099 distinct undirected graphs with one through five vertices. Every possible source is tested. A Floyd-Warshall distance oracle independently verifies BFS distances and reachable sets. A separate recursive search verifies DFS order. Components are compared against reachability equivalence classes. Further cases cover directed cycles, self-loops, duplicate input edges, isolates, unreachable targets, empty graphs, invalid endpoints, every generator, a 5,000-vertex path, and exact demo output.

Every benchmark traversal also asserts full vertex coverage, uniqueness, parent-edge validity, component-label consistency, tree-depth consistency, and the adjacency-entry operation count. See validation.txt for the executed test log.

## Limitations for the presentation

Runtime includes instrumentation and result bookkeeping. All trials use one machine and one Python version. Synthetic graph shapes and fixed ascending labels influence DFS paths. Sparse and dense graphs are connectivity-conditioned by construction. Only three seeds are used for random graphs. The timed workload explores the whole graph, while practical searches may stop once they find a target. The demo exercises application correctness without benchmarking separate application workloads. The plots' dashed reference lines scale V + A to the first measured point and serve as growth illustrations. They are not fitted models. Re-run on the team's presentation computer if reporting its performance.
