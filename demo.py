"""Run with python demo.py. Small deterministic output for a live demo."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from algorithms import bfs, dfs, connected_components, path_to, shortest_path
from graphs import demo_graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Also save the demo evidence as JSON")
    args = parser.parse_args()
    graph = demo_graph()
    breadth, depth = bfs(graph), dfs(graph)
    evidence = {
        "adjacency": graph.adjacency,
        "source": 0,
        "target": 5,
        "bfs": asdict(breadth),
        "dfs": asdict(depth),
        "bfs_shortest_path": shortest_path(graph, 0, 5),
        "dfs_tree_path": path_to(depth, 5),
        "unreachable_target_9": shortest_path(graph, 0, 9),
        "components_bfs": connected_components(graph, "bfs"),
        "components_dfs": connected_components(graph, "dfs"),
    }
    print("BFS and DFS on the same unweighted, undirected graph")
    for vertex, neighbors in enumerate(graph.adjacency):
        print(f"  {vertex}: {list(neighbors)}")
    print("\nBFS discovery order:", breadth.order)
    print("DFS discovery order:", depth.order)
    print("BFS shortest path 0 -> 5:", evidence["bfs_shortest_path"], "(2 edges)")
    print("DFS tree path 0 -> 5:", evidence["dfs_tree_path"], "(5 edges)")
    print("Path 0 -> 9:", evidence["unreachable_target_9"], "(unreachable)")
    print("Components from BFS:", evidence["components_bfs"])
    print("Components from DFS:", evidence["components_dfs"])
    print("\nDFS finds a valid path. BFS guarantees the fewest edges here.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(evidence, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
