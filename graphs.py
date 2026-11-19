"""Deterministic, simple, unweighted undirected graph generators."""

import math

from algorithms import Graph


def make_graph(family: str, n: int, seed=2026):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    edges = set()
    if family == "path":
        edges = {(v - 1, v) for v in range(1, n)}
    elif family == "star":
        edges = {(0, v) for v in range(1, n)}
    elif family == "grid":
        width = max(1, math.isqrt(n))
        for v in range(n):
            if v % width and v - 1 >= 0:
                edges.add((v - 1, v))
            if v >= width:
                edges.add((v - width, v))
    elif family == "disconnected":
        # Three path components plus an isolated final vertex (for n >= 4).
        for group in range(3):
            vertices = list(range(group, max(0, n - 1), 3))
            edges.update(zip(vertices, vertices[1:]))
    else:
        raise ValueError(f"Unknown graph family: {family}")
    return Graph.from_edges(n, edges)


def demo_graph():
    # Two components and an isolated vertex. DFS's first route from 0 to 5
    # is longer than the BFS shortest route under ascending neighbor order.
    return Graph.from_edges(10, [(0, 1), (1, 2), (2, 3), (3, 4),
                                 (4, 5), (0, 6), (6, 5), (7, 8)])
