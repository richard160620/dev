import csv
import heapq

edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
_graph = None
_heuristics = None


def _load_graph():
    global _graph
    if _graph is not None:
        return _graph

    graph = {}
    with open(edgeFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row['start'])
            end = int(row['end'])
            distance = float(row['distance'])
            graph.setdefault(start, []).append((end, distance))
            graph.setdefault(end, [])

    _graph = graph
    return _graph


def _load_heuristics():
    global _heuristics
    if _heuristics is not None:
        return _heuristics

    heuristics = {}
    with open(heuristicFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = int(row['node'])
            heuristics[node] = {int(k): float(v) for k, v in row.items() if k != 'node' and v}

    _heuristics = heuristics
    return _heuristics

def _reconstruct_path(parent, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path
def astar(start, end):
    graph = _load_graph()
    heuristics = _load_heuristics()

    if start == end:
        return [start], 0.0, 1

    start_h = heuristics.get(start, {}).get(end, 0.0)
    pq = [(start_h, 0.0, start)]   # (f, g, node)

    parent = {start: None}
    best_g = {start: 0.0}
    num_visited = 0

    while pq:
        f, g, node = heapq.heappop(pq)

        if g > best_g.get(node, float("inf")):
            continue

        num_visited += 1

        if node == end:
            path = _reconstruct_path(parent, end)
            return path, g, num_visited

        for neighbor, dist in graph.get(node, []):
            new_g = g + dist
            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                parent[neighbor] = node
                h = heuristics.get(neighbor, {}).get(end, 0.0)
                heapq.heappush(pq, (new_g + h, new_g, neighbor))

    return [], float("inf"), num_visited


if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, dist, num_visited = astar(2773409914, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
