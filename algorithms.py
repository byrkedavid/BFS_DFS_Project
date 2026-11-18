"""Adjacency-list graph searches and applications. No third-party dependencies."""

from collections import deque
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Graph:
    """Vertices are integers 0 through n-1. Neighbor order is significant."""

    adjacency: tuple[tuple[int, ...], ...]
    directed: bool = False

    @classmethod
    def from_edges(cls, n: int, edges: Iterable[tuple[int, int]], directed=False):
        if type(n) is not int or n < 0:
            raise ValueError("Vertex count must be a nonnegative integer")
        neighbors = [set() for _ in range(n)]
        for u, v in edges:
            if type(u) is not int or type(v) is not int or not (0 <= u < n and 0 <= v < n):
                raise ValueError("Each endpoint must be a vertex in 0..n-1")
            neighbors[u].add(v)
            if not directed:
                neighbors[v].add(u)
        return cls(tuple(tuple(sorted(row)) for row in neighbors), directed)

    @property
    def n(self):
        return len(self.adjacency)

    @property
    def adjacency_entries(self):
        return sum(map(len, self.adjacency))

    @property
    def edges(self):
        if self.directed:
            return self.adjacency_entries
        loops = sum(u in row for u, row in enumerate(self.adjacency))
        return (self.adjacency_entries + loops) // 2


@dataclass
class SearchResult:
    order: list[int]
    parent: dict[int, int | None]
    depth: dict[int, int]
    roots: list[int]
    component: dict[int, int]
    edge_checks: int
    max_frontier: int


def search(graph: Graph, source: int | None = 0, *, method="bfs", full=False):
    """Run BFS or recursive-order iterative DFS.

    full=True continues at every unvisited vertex, producing a search forest.
    On directed graphs these forest labels are NOT connected components.
    depth is tree depth; only BFS depth is a shortest-path distance.
    """
    if method not in ("bfs", "dfs"):
        raise ValueError("method must be bfs or dfs")
    if graph.n == 0:
        if source not in (None, 0):
            raise ValueError("Empty graph has no such source")
        return SearchResult([], {}, {}, [], {}, 0, 0)
    if type(source) is not int or not 0 <= source < graph.n:
        raise ValueError("Source must be a valid vertex")
    order, roots = [], []
    parent, depth, component = {}, {}, {}
    checks = peak = 0
    # The source is first. Remaining roots are selected in ascending order.
    candidates = [source]
    if full:
        candidates.extend(v for v in range(graph.n) if v != source)
    for root in candidates:
        if root in parent:
            continue
        component_id = len(roots)
        roots.append(root)
        parent[root], depth[root], component[root] = None, 0, component_id
        order.append(root)
        if method == "bfs":
            frontier = deque([root])
            peak = max(peak, 1)
            while frontier:
                u = frontier.popleft()
                for v in graph.adjacency[u]:
                    checks += 1
                    if v not in parent:
                        parent[v], depth[v], component[v] = u, depth[u] + 1, component_id
                        order.append(v)
                        frontier.append(v)
                        peak = max(peak, len(frontier))
        else:
            # Each frame keeps the next neighbor to examine. This follows the
            # same discovery order as recursive DFS without Python recursion.
            stack = [(root, iter(graph.adjacency[root]))]
            peak = max(peak, 1)
            while stack:
                u, neighbors = stack[-1]
                v = next(neighbors, None)
                if v is None:
                    stack.pop()
                    continue
                checks += 1
                if v not in parent:
                    parent[v], depth[v], component[v] = u, depth[u] + 1, component_id
                    order.append(v)
                    stack.append((v, iter(graph.adjacency[v])))
                    peak = max(peak, len(stack))
    return SearchResult(order, parent, depth, roots, component, checks, peak)


def bfs(graph, source=0, *, full=False):
    return search(graph, source, method="bfs", full=full)


def dfs(graph, source=0, *, full=False):
    return search(graph, source, method="dfs", full=full)


def path_to(result: SearchResult, target: int):
    """Reconstruct a forest-root-to-target path, or None if unreachable."""
    if target not in result.parent:
        return None
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = result.parent[current]
    return list(reversed(path))


def shortest_path(graph: Graph, source: int, target: int):
    """Fewest edges in an unweighted directed or undirected graph."""
    if type(target) is not int or not 0 <= target < graph.n:
        raise ValueError("Target must be a valid vertex")
    return path_to(bfs(graph, source), target)


def connected_components(graph: Graph, method="bfs"):
    if graph.directed:
        raise ValueError("This function requires an undirected graph")
    result = search(graph, method=method, full=True)
    groups = [[] for _ in result.roots]
    for vertex in result.order:
        groups[result.component[vertex]].append(vertex)
    return groups
