"""Independent correctness checks. Run python -m unittest -v."""

import itertools
import unittest

from algorithms import Graph, bfs, dfs, path_to, shortest_path, connected_components
from benchmark import validate_full
from graphs import demo_graph, make_graph


def reference_distances(graph, source):
    """Floyd-Warshall oracle, independent of the traversal implementation."""
    n = graph.n
    distance = [[float("inf")] * n for _ in range(n)]
    for u in range(n):
        distance[u][u] = 0
        for v in graph.adjacency[u]:
            distance[u][v] = min(distance[u][v], 1)
    for k in range(n):
        for u in range(n):
            for v in range(n):
                distance[u][v] = min(distance[u][v], distance[u][k] + distance[k][v])
    return {v: int(d) for v, d in enumerate(distance[source]) if d != float("inf")}


def recursive_order(graph, source):
    seen, order = set(), []

    def visit(u):
        seen.add(u)
        order.append(u)
        for v in graph.adjacency[u]:
            if v not in seen:
                visit(v)

    visit(source)
    return order


class TraversalTests(unittest.TestCase):
    def assert_searches(self, graph, source):
        expected = reference_distances(graph, source)
        breadth, depth = bfs(graph, source), dfs(graph, source)
        self.assertEqual(breadth.depth, expected)
        self.assertEqual(set(depth.order), set(expected))
        self.assertEqual(depth.order, recursive_order(graph, source))
        for result in (breadth, depth):
            self.assertEqual(len(result.order), len(set(result.order)))
            for target in result.order:
                path = path_to(result, target)
                self.assertEqual(path[0], source)
                self.assertEqual(path[-1], target)
                self.assertTrue(all(v in graph.adjacency[u] for u, v in zip(path, path[1:])))

    def test_all_undirected_graphs_through_five_vertices(self):
        count = 0
        for n in range(1, 6):
            possible = list(itertools.combinations(range(n), 2))
            for mask in range(1 << len(possible)):
                graph = Graph.from_edges(n, [e for i, e in enumerate(possible) if mask & (1 << i)])
                for source in range(n):
                    self.assert_searches(graph, source)
                expected_groups = set()
                for source in range(n):
                    expected_groups.add(frozenset(reference_distances(graph, source)))
                for method in ("bfs", "dfs"):
                    actual = {frozenset(c) for c in connected_components(graph, method)}
                    self.assertEqual(actual, expected_groups)
                count += 1
        self.assertEqual(count, 1099)

    def test_directed_cycles_self_loops_and_duplicate_edges(self):
        graph = Graph.from_edges(6, [(0, 0), (0, 1), (0, 1), (1, 2), (2, 0), (3, 2), (4, 5)], True)
        for source in range(6):
            self.assert_searches(graph, source)
        self.assertEqual(shortest_path(graph, 2, 1), [2, 0, 1])
        self.assertIsNone(shortest_path(graph, 0, 3))
        with self.assertRaises(ValueError):
            connected_components(graph)

    def test_empty_and_invalid_inputs(self):
        empty = Graph.from_edges(0, [])
        self.assertEqual(bfs(empty).order, [])
        self.assertEqual(dfs(empty, full=True).order, [])
        self.assertEqual(connected_components(empty), [])
        for n, edges in [(-1, []), (2, [(0, 2)]), (2, [(False, 1)])]:
            with self.assertRaises(ValueError):
                Graph.from_edges(n, edges)
        graph = Graph.from_edges(1, [])
        for source in (-1, 1, None, False):
            with self.assertRaises(ValueError):
                bfs(graph, source)
        with self.assertRaises(ValueError):
            shortest_path(graph, 0, 2)

    def test_graph_families_and_generation(self):
        for family in ("path", "star", "grid", "disconnected"):
            for n in (0, 1, 2, 4, 11, 23):
                for seed in (2026, 2027):
                    graph = make_graph(family, n, seed)
                    self.assertEqual(graph, make_graph(family, n, seed))
                    for method in (bfs, dfs):
                        validate_full(graph, method(graph, full=True))
                    if n:
                        self.assert_searches(graph, 0)
        for family in ("path", "star"):
            self.assertEqual(make_graph(family, 100).edges, 99)

    def test_deep_graph_and_frontier_shape(self):
        path, star = make_graph("path", 5000), make_graph("star", 5000)
        self.assertEqual(bfs(path).max_frontier, 1)
        self.assertEqual(dfs(path).max_frontier, 5000)
        self.assertEqual(bfs(star).max_frontier, 4999)
        self.assertEqual(dfs(star).max_frontier, 2)
        self.assertEqual(bfs(path, full=True).edge_checks, 9998)
        self.assertEqual(dfs(path, full=True).edge_checks, 9998)

    def test_demo_outputs(self):
        graph = demo_graph()
        self.assertEqual(shortest_path(graph, 0, 5), [0, 6, 5])
        self.assertEqual(path_to(dfs(graph), 5), [0, 1, 2, 3, 4, 5])
        self.assertIsNone(shortest_path(graph, 0, 9))
        for method in ("bfs", "dfs"):
            self.assertEqual({frozenset(c) for c in connected_components(graph, method)},
                             {frozenset(range(7)), frozenset((7, 8)), frozenset((9,))})


if __name__ == "__main__":
    unittest.main()
