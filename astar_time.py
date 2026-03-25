import csv
import heapq

edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
_graph = None
_heuristics = None
_max_speed_mps = None


def _load_graph():
    global _graph, _max_speed_mps
    if _graph is not None:
        return _graph

    graph = {}
    max_speed_mps = 0.0
    with open(edgeFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row['start'])
            end = int(row['end'])
            distance = float(row['distance'])
            speed_kmh = float(row['speed limit'])
            speed_mps = speed_kmh * 1000.0 / 3600.0

            if speed_mps > 0.0:
                travel_time = distance / speed_mps
                graph.setdefault(start, []).append((end, travel_time))
                if speed_mps > max_speed_mps:
                    max_speed_mps = speed_mps

            graph.setdefault(end, [])

    _graph = graph
    _max_speed_mps = max_speed_mps
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


def astar_time(start, end):
    graph = _load_graph()
    heuristics = _load_heuristics()

    if start == end:
        return [start], 0.0, 1

    def h_time(node):
        straight_line_dist = heuristics.get(node, {}).get(end, 0.0)
        return straight_line_dist / _max_speed_mps

    pq = [(h_time(start), 0.0, start)]
    parent = {start: None}
    best_time = {start: 0.0}
    num_visited = 0

    while pq:
        f_time, g_time, node = heapq.heappop(pq)

        if g_time > best_time.get(node, float("inf")):
            continue

        num_visited += 1

        if node == end:
            path = _reconstruct_path(parent, end)
            return path, g_time, num_visited

        for neighbor, edge_time in graph.get(node, []):
            new_time = g_time + edge_time

            if new_time < best_time.get(neighbor, float("inf")):
                best_time[neighbor] = new_time
                parent[neighbor] = node
                heapq.heappush(pq, (new_time + h_time(neighbor), new_time, neighbor))

    return [], float("inf"), num_visited


if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, time, num_visited = astar_time(2773409914, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')