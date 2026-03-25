import csv
import sys

edgeFile = 'edges.csv'
_graph = None


def _load_graph():
    global _graph
    if _graph is not None:
        return _graph

    graph = {}
    with open(edgeFile, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row["start"])
            end = int(row["end"])
            distance = float(row["distance"])
            graph.setdefault(start, []).append((end, distance))
            graph.setdefault(end, [])

    _graph = graph
    return _graph
def _reconstruct_path(parent, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def _compute_distance(graph, path):
    total = 0.0
    for u, v in zip(path, path[1:]):
        for nxt, dist in graph[u]:
            if nxt == v:
                total += dist
                break
    return total

def dfs(start, end):
    graph = _load_graph()
    sys.setrecursionlimit(max(sys.getrecursionlimit(), len(graph) + 100))

    if start == end:
        return [start], 0.0, 1

    stack = [start]
    visited = {start}
    parent = {start: None}
    num_visited = 0

    while stack:
        node = stack.pop()
        num_visited += 1

        if node == end:
            path = _reconstruct_path(parent, end)
            dist = _compute_distance(graph, path)
            return path, dist, num_visited

        neighbors = graph.get(node, [])
        for neighbor, _dist in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                stack.append(neighbor)

    return [], float("inf"), num_visited
if __name__ == "__main__":
    # Public case 1 in current dataset.
    path, dist, num_visited = dfs(2773409914, 1079387396)
    print(f"The number of path nodes: {len(path)}")
    print(f"Total distance of path: {dist}")
    print(f"The number of visited nodes: {num_visited}")
