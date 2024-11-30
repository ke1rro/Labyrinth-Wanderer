'''dijkstra_algorithm.py'''
from queue import PriorityQueue
import numpy as np


def matrix_to_adj_dict(maze: np.ndarray) -> dict[tuple, set]:
    """
    Converts a maze represented as a 2D NumPy array into an adjacency dictionary.

    Each key in the adjacency dictionary represents a non-wall cell (as a tuple of coordinates),
    and its value is a set of adjacent non-wall cells.

    The function also identifies the start and end points in the maze. 

    Args:
        maze (np.ndarray): A 2D NumPy array where:
            - 0 represents an empty square,
            - 1 represents a wall,
            - 2 represents the start point,
            - 3 represents the end point.

    Returns:
        tuple: A tuple containing:
            - dict[tuple[int, int], set[tuple[int, int]]]: An adjacency dictionary of the maze.
            - tuple[int, int]: The coordinates of the start point.
            - tuple[int, int]: The coordinates of the end point.
    """
    n = maze.shape[0]
    adjacent_dict = {}
    start = None
    end = None
    for row in range(n):
        for col in range(n):
            if maze[row, col] == 1:
                continue
            if maze[row, col] == 2:
                start = (row, col)
            elif maze[row, col] == 3:
                end = (row, col)

            adjacent_dict[(row, col)] = set()
            if row != 0 and maze[row-1, col] != 1:
                adjacent_dict[(row, col)].add((row-1, col))
            if row != n-1 and maze[row+1, col] != 1:
                adjacent_dict[(row, col)].add((row+1, col))
            if col != 0 and maze[row, col-1] != 1:
                adjacent_dict[(row, col)].add((row, col-1))
            if col != n-1 and maze[row, col+1] != 1:
                adjacent_dict[(row, col)].add((row, col+1))
    return adjacent_dict, start, end


def dijkstra(maze: dict[tuple: set], start: tuple, end: tuple) -> dict[tuple, list] | int:
    """
    Finds the shortest path in a maze from the start to the end point using Dijkstra's algorithm.

    Args:
        maze (dict): An adjacency dictionary where:
            - Keys are non-wall cell coordinates (tuples).
            - Values are sets of adjacent non-wall cell coordinates.
        start (tuple): The coordinates of the start point.
        end (tuple): The coordinates of the end point.

    Returns:
        dict[tuple[int, int], list] | int: If a path exists, returns a dictionary where:
            - Keys are cell coordinates.
            - Values are lists containing:
                - The shortest distance to the cell.
                - A boolean indicating whether the cell has been visited.
                - The previous cell on the shortest path.
            If no path exists, returns -1.
    """
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
    """
    Reconstructs the shortest path from the start to the end point.

    Args:
        graph (dict): A dictionary returned by the `dijkstra` function where:
            - Keys are cell coordinates.
            - Values are lists containing:
                - The shortest distance to the cell.
                - A boolean indicating whether the cell has been visited.
                - The previous cell on the shortest path.
        start (tuple): The coordinates of the start point.
        end (tuple): The coordinates of the end point.

    Returns:
        list[tuple[int, int]]: A list of tuples representing the shortest path, 
        starting from the start point and ending at the end point.
    """
    path = []
    cur_node = end
    while True:
        path.append(cur_node)
        if cur_node == start:
            break
        cur_node = graph[cur_node][2]
    return list(reversed(path))


def find_shortest_path(maze_matrix: np.ndarray) -> list[tuple] | int:
    """
    Finds the shortest path in a maze represented as a 2D NumPy array.

    Args:
        maze_matrix (np.ndarray): A 2D NumPy array where:
            - 0 represents an empty square,
            - 1 represents a wall,
            - 2 represents the start point,
            - 3 represents the end point.

    Returns:
        list[tuple[int, int]] | int: If a path exists, returns a list of tuples representing the 
        shortest path from the start to the end point. If no path exists, returns -1.
    """
    maze_dict, start, end = matrix_to_adj_dict(maze_matrix)
    graph = dijkstra(maze_dict, start, end)
    if graph != -1:
        return reconstruct_path(graph, start, end)
    return -1
