'''dijkstra algorithm'''
maze_matrix = [
    [2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 3],
    [1, 1, 1, 1, 1, 1, 1]
]

maze_dict = {
    (0, 0): {(1, 0)},
    (1, 0): {(0, 0), (1, 1)},
    (1, 1): {(1, 0), (1, 2)},
    (1, 2): {(1, 1), (2, 2)},
    (2, 2): {(1, 2), (2, 3)},
    (2, 3): {(2, 2), (3, 3)},
    (3, 3): {(2, 3), (4, 3)},
    (4, 3): {(3, 3), (4, 4)},
    (4, 4): {(4, 3), (4, 5)},
    (4, 5): {(4, 4), (5, 5)},
    (5, 5): {(4, 5), (5, 6)},
    (5, 6): {(5, 5)}
}


def compare_dist(point: tuple[tuple, int], graph: dict) -> bool:
    return point[1] <= graph[point[0]][0]


def get_min_dist_node(graph: dict, queue: list) -> tuple:
    return min(queue, key=lambda el: el[1] if compare_dist(el, graph) else float('inf'))


def dijkstra(maze: dict[tuple: tuple], start: tuple, end: tuple) -> dict:
    graph = {node: [float('inf'), False, None] for node in maze}
    graph[start] = [0, True, start]
    queue = [(start, 0)]
    prev_node = start
    while True:
        cur_node = get_min_dist_node(graph, queue)
        if cur_node[0] == end:
            return graph
        graph[cur_node[0]][2] = prev_node[0]
        queue.remove(cur_node)
        for node in maze[cur_node[0]]:
            if graph[node][1]:
                continue
            if graph[node][0] > cur_node[1] + 1:
                graph[node][0] = cur_node[1] + 1
                graph[node][2] = cur_node[0]
                queue.append((node, graph[node][0]))
        prev_node = cur_node
        if not queue:
            return -1
    return -1


def reconstruct_path(graph: dict, start: tuple, end: tuple) -> list[tuple]:
    path = []
    cur_node = end
    while True:
        path.append(cur_node)
        if cur_node == start:
            break
        cur_node = graph[cur_node][2]
    return list(reversed(path))


def find_shortest_path(maze: dict, start: tuple, end: tuple) -> list[tuple] | int:
    graph = dijkstra(maze, start, end)
    if graph != -1:
        return reconstruct_path(graph, start, end)
    return -1


# print(find_shortest_path(maze_dict, (0, 0), (5, 6)))
