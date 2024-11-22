'''dijkstra algorithm'''
from queue import PriorityQueue

maze_matrix = [
    [2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 3],
    [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
]


def matrix_to_adj_dict(maze: list[list[int]]):
    n = len(maze)
    adjacent_dict = {}
    start = None
    end = None
    for row in range(n):
        for col in range(n):
            if maze[row][col] == 1:
                continue
            if maze[row][col] == 2:
                start = (row, col)
            elif maze[row][col] == 3:
                end = (row, col)
            adjacent_dict[(row, col)] = set()
            if row != 0:
                if maze[row-1][col] != 1:
                    adjacent_dict[(row, col)].add((row-1, col))
            if row != n-1:
                if maze[row+1][col] != 1:
                    adjacent_dict[(row, col)].add((row+1, col))
            if col != 0:
                if maze[row][col-1] != 1:
                    adjacent_dict[(row, col)].add((row, col-1))
            if col != n-1:
                if maze[row][col+1] != 1:
                    adjacent_dict[(row, col)].add((row, col+1))
    return adjacent_dict, start, end


# def compare_dist(point: tuple[tuple, int], graph: dict) -> bool:
#     return point[1] <= graph[point[0]][0]


# def get_min_dist_node(graph: dict, queue: list) -> tuple:
#     return min(queue, key=lambda el: el[1] if compare_dist(el, graph) else float('inf'))


# def dijkstra(maze: dict[tuple: tuple], start: tuple, end: tuple) -> dict:
#     graph = {node: [float('inf'), False, None] for node in maze}
#     graph[start] = [0, True, start]
#     queue = [(start, 0)]
#     while True:
#         cur_node = get_min_dist_node(graph, queue)
#         if cur_node[0] == end:
#             return graph
#         graph[cur_node[0]][1] = True
#         queue.remove(cur_node)
#         for node in maze[cur_node[0]]:
#             if graph[node][1]:
#                 continue
#             if graph[node][0] > cur_node[1] + 1:
#                 graph[node][0] = cur_node[1] + 1
#                 graph[node][2] = cur_node[0]
#                 queue.append((node, graph[node][0]))
#         if not queue:
#             return -1


def dijkstra(maze: dict[tuple: tuple], start: tuple, end: tuple) -> dict:
    graph = {node: [float('inf'), False, None] for node in maze}
    graph[start] = [0, True, start]
    nodes_queue = PriorityQueue()
    nodes_queue.put((0, start))
    while True:
        dist_to_cur_node, cur_node = nodes_queue.get(timeout=5)
        if cur_node == end:
            return graph
        graph[cur_node][1] = True
        for node in maze[cur_node]:
            if graph[node][1]:
                continue
            if graph[node][0] > dist_to_cur_node + 1:
                dist_to_node = dist_to_cur_node + 1
                graph[node][0] = dist_to_node
                graph[node][2] = cur_node
                nodes_queue.put((dist_to_node, node))
        if nodes_queue.empty():
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


def find_shortest_path(maze_matr: list[list[int]]) -> list[tuple] | int:
    maze_dict, start, end = matrix_to_adj_dict(maze_matr)
    graph = dijkstra(maze_dict, start, end)
    if graph != -1:
        return reconstruct_path(graph, start, end)
    return -1


# print(find_shortest_path(maze_matrix))
