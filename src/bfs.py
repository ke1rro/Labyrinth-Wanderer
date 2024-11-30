'''
BFS
'''
from collections import deque
from functools import lru_cache

import numpy as np

from maze import GridCell


def find_start(coord_matrix: np.array) -> list:
    """
    Returns the start cell in the maze
    Args:
        coord_matrix (np.array): numpy array with Gridcell instances

    Returns:
        list: list with the start cell
    """
    for row in coord_matrix:
        for cell in row:
            if cell.is_start():
                return [cell]


@lru_cache(None)
def cached_neighbors(row: int, col: int, total_rows: int, total_cols: int):
    """
    Cache neighbors for a cell to avoid recalculating repeatedly.
    Neighbors are calculated using only the cell's
    row, col, and grid dimensions.
    """
    neighbors = []

    if row < total_rows - 1:  # DOWN
        neighbors.append((row + 1, col))
    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col < total_cols - 1:  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def backtrace(draw: callable, relations: dict, end_node: GridCell):
    '''
    Highlights the correct path after the search algorithm is done.
    '''
    curr_node = end_node
    while True:
        curr_node.make_path()
        parent = relations[curr_node]
        draw()
        curr_node = parent
        if curr_node.is_start():
            break


def bfs_algorithm(draw: callable, coord_matrix: np.array):
    """
    Finds the shortest path to the exit using the
    breadth-first-search algorithm.
    """
    start = find_start(coord_matrix)
    queue = deque(start)
    relations = {}

    total_rows, total_cols = coord_matrix.shape
    node_update_count = 0
    update_threshold = 10

    while queue:
        curr_node = queue.popleft()

        if curr_node.is_end():
            backtrace(draw, relations, curr_node)
            return True

        if not curr_node.is_start():
            curr_node.make_closed()

        row, col = curr_node.row, curr_node.col
        for neighbor_row, neighbor_col in cached_neighbors(row, col,
                                                           total_rows,
                                                           total_cols):
            neighbor = coord_matrix[neighbor_row][neighbor_col]

            if neighbor.is_unvisited() and not neighbor.is_start():
                queue.append(neighbor)
                relations[neighbor] = curr_node
                neighbor.make_open()
            if neighbor.is_end():
                queue.appendleft(neighbor)
                relations[neighbor] = curr_node

        node_update_count += 1
        if node_update_count % update_threshold == 0:
            draw()

    return False
