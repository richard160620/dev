import csv
import heapq

edgeFile = 'edges.csv'
_graph = None


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

def _reconstruct_path(parent, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def ucs(start, end):
    graph = _load_graph()

    if start == end:
        return [start], 0.0, 1

    pq = [(0.0, start)]   # (cost, node)
    parent = {start: None}
    best_cost = {start: 0.0}
    num_visited = 0

    while pq:
        cost, node = heapq.heappop(pq)

        if cost > best_cost.get(node, float("inf")):
            continue

        num_visited += 1

        if node == end:
            path = _reconstruct_path(parent, end)
            return path, cost, num_visited

        for neighbor, dist in graph.get(node, []):
            new_cost = cost + dist
            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))

    return [], float("inf"), num_visited


if __name__ == '__main__':
    # Public case 1 in current dataset.
    path, dist, num_visited = ucs(2773409914, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
