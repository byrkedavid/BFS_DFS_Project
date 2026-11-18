# Preparation for the presentation script

This handoff gives the next writer the project facts, evidence, slide order, demo actions, and decisions still needed from the team. It accompanies working code and measured results. It is an outline for writing the script after the team reviews the experiment.

## Core message and research question

The proposal asks how BFS and DFS compare in efficiency and usefulness on graph traversal problems. Our implementation demonstrates equal reachable-set and component correctness, different traversal orders and frontier shapes, and BFS's shortest-path guarantee for unweighted graphs. The experiment measured BFS with a lower median runtime on all 55 graph pairs. This empirical observation is specific to these Python implementations and inputs. Both full traversals perform O(V + E) work.

Use `results/FINDINGS.md` as the source of numeric claims. Use `results/summary.csv` to verify any number copied into a slide. Methodology details are in `METHODS.md`, and exact raw measurements are in the two trial CSVs. Avoid explaining CPU timing differences solely through Big O, since the asymptotic order is the same.

## Instructor requirements and dates

- The presentation outline specifies 12 minutes and 3 minutes of Q&A, with a live demo of at most 3 minutes.
- It asks for an introduction, functional and non-functional requirements, at least two system/model design slides, at least five development-strategy slides, at least three results slides, a conclusion, and references.
- Results must identify algorithm functions and show actual runtime and theoretical growth.
- The live presentation window runs November 9-21, 2026. Available Teams slots are Tuesday, Wednesday, Friday, and Saturday, 3-5 p.m. All group members attend with cameras on. Create the meeting and add the instructor after coordinating the time.
- The presentation upload is due November 21 at 11:59 p.m. Eastern. The final report is due November 30 at 11:59 p.m. Eastern.
- The report outline asks for a title page, contents, one-page introduction, one-page objectives, one-page literature review, at least three methodology pages, at least four results pages, a one-page conclusion, references, and a code/raw-data appendix where applicable.

The D2L folders showed both project deliverables unsubmitted when reviewed on November 17. The team's booked presentation slot remains unknown. Recheck dates and folder instructions before submission.

## Proposed slide sequence

The following 15-slide sequence allocates roughly 11 minutes including the demo, leaving about one minute for transitions. These timings are a rehearsal target. Speaker assignment should be agreed by all four members.

| Slides | Section and suggested time | Content and evidence |
|---|---|---|
| 1-2 | Title and introduction, 45 seconds | Team names, approved topic, research question, applications. Use the proposal and demo graph. State each member's actual contribution after the team agrees. |
| 3 | Requirements, 30 seconds | Functional requirements are traversal, reachable-set reporting, path reconstruction, unweighted shortest path, components, and repeatable experiments. Quality requirements are correctness, reproducibility, bounded scope, deterministic behavior, and a usable live demo. |
| 4-5 | System and model design, 60 seconds | Diagram the flow from graph generator to shared adjacency-list graph to BFS/DFS to metrics/CSV/figures. Show queue and iterator-frame stack, discovery marking, parent maps, and forest restarts. |
| 6 | Development strategy 1, 20 seconds | Define scope, integer vertex labels, undirected unweighted experiment, deterministic neighbor order. Explain how it follows the proposal. |
| 7 | Development strategy 2, 20 seconds | BFS queue logic, popleft, mark on discovery, parent/depth recording. Point to algorithms.py. |
| 8 | Development strategy 3, 20 seconds | DFS explicit frames and backtracking. Explain why avoiding recursion supports long paths. |
| 9 | Development strategy 4, 20 seconds | Graph generation, fixed seeds, same inputs for both algorithms, separate runtime/memory passes. |
| 10 | Development strategy 5, 20 seconds | Independent correctness tests, then benchmark, analyze, and document. Describe this actual build workflow. Team collaboration practices need confirmation before being described as past work. |
| 11 | Results 1, 40 seconds | Runtime figure, 55 graph pairs, 9 timing trials each. Discuss sparse versus dense edge growth and the scaled V + A reference. Use runtime_by_family.png and the matching CSV rows. |
| 12 | Results 2, 40 seconds | Memory figure and frontier_shape.png. Contrast path and star measurements using the concrete counts below. Explain traced allocation and shared result storage. |
| 13 | Results 3, 40 seconds | Correctness, traversal order, components, shortest-path counterexample. Use demo_paths.png and demo.json. Every timed traversal checks A adjacency entries and visits V vertices. |
| Live program | Demo, 2 minutes 30 seconds | Run python demo.py. Follow the actions below. |
| 14 | Conclusion, 30 seconds | Answer the research question with supported findings, practical choices, and limitations. Mention synthetic graphs, fixed labels, one machine, and full traversals. |
| 15 | References, 15 seconds | Cite relevant graph algorithm sources, Python measurement documentation, and course requirements. |

## Verified talking points

- There are 55 graph instances, 110 algorithm summaries, 990 raw runtime records, and 330 raw memory records.
- All measured full traversals visited V distinct vertices and examined exactly A adjacency entries. A equals 2E for the loop-free undirected benchmark inputs.
- On the 5,000-vertex path, the BFS queue peak was 1 and the DFS stack peak was 5,000 frames.
- On the 5,000-vertex star, the BFS queue peak was 4,999 and the DFS stack peak was 2 frames.
- Median path timings were 2.3832 ms for BFS and 3.2514 ms for DFS. Peak traced allocations were 811.9 KiB and 1,359.7 KiB, respectively.
- Median star timings were 2.3382 ms for BFS and 3.2160 ms for DFS. Peak traced allocations were 738.9 KiB and 716.6 KiB, respectively.
- The demo's BFS order is [0, 1, 6, 2, 5, 3, 4]. DFS order is [0, 1, 2, 3, 4, 5, 6].
- The BFS shortest path is [0, 6, 5], with 2 edges. The DFS tree path is [0, 1, 2, 3, 4, 5], with 5 edges.
- Both methods find the same three undirected component sets, including isolated vertex 9.

These numeric values refer to the included November 17 run. If results are regenerated, update this page from the new FINDINGS.md and CSVs before scripting. Use only the precision needed to make a point on slides.

## Demo plan

Open a terminal in the project folder and run `python demo.py`. This command works without Matplotlib or third-party packages.

1. Point out the shared adjacency-list input. Vertices 0 through 6 form the first component, 7 and 8 form another, and 9 is isolated.
2. Compare the BFS and DFS discovery orders. Ascending neighbor ordering makes the difference reproducible.
3. Show the two routes from 0 to 5. Count the edges. The shorter BFS route uses 0 to 6 to 5.
4. Show that target 9 is unreachable from 0.
5. Show the full connected-component results. The member ordering differs, while the sets agree.
6. Return to the conclusion slide. Keep a copy of results/demo.json and demo_paths.png open in case the terminal cannot be shared.

Do not run the complete benchmark in the live demo. The included measurement files can be opened directly to show evidence. A short demonstration of the tests can be rehearsed separately if the instructor asks about validation.

## Likely questions and evidence to use

| Question | Explanation |
|---|---|
| Why is DFS slower in these measurements? | Both have the same asymptotic traversal work. This implementation's DFS manages iterator frames and backtracking, while BFS uses deque. The experiment also includes instrumentation and maps. This is a plausible implementation explanation, not a causal profiling result. |
| Does BFS always use more memory? | Frontier shape depends on the graph. The path and star examples reverse which frontier is larger. Total traced memory also includes common result maps and implementation-specific frame sizes. |
| Why can dense traversal look quadratic? | E increases approximately quadratically with V. Both algorithms remain linear in V + E. |
| Can DFS find a shortest path? | Its first discovered tree path can be longer than the shortest path. The demo supplies a counterexample to a general guarantee. BFS gives fewest-edge paths in unweighted graphs. |
| How were disconnected graphs handled? | Full traversal restarts from unvisited roots and labels components. Single-source traversal visits only the source's reachable set. |
| How do you know it works? | The tests compare against independent Floyd-Warshall distances, recursive DFS order, and reachability partitions on 1,099 small undirected graphs, plus boundary and large-path cases. |
| Were application timings measured? | Connected components and path finding were validated in examples. The recorded timing workload is full graph traversal. |
| Where did the graphs come from? | Deterministic generators and seeded synthetic generators in graphs.py. Their precise construction and graph hashes are recorded. |

## Team decisions before writing the script

Confirm the presentation slot, speakers, actual contributions, and whether the team wants to rerun measurements on the demo computer. Each speaker should explain the code or evidence they will present. Agree on terminology for V, E, adjacency entries, queue frontier, DFS frames, and traced memory. Confirm that the shared report uses the same experiment and result files. Update the report's contents page and replace its prompts, blank programming-language field, and unrelated references. The supplied proposal's timeline is a plan, so claims that the team used a specific collaboration method must come from the team's actual work.
