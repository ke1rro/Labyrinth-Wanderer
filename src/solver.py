"""Module with algorithms"""

from queue import PriorityQueue

import numpy as np
import pygame

from maze import GridCell


def characteristic_function(p1: tuple[int], p2: tuple[int]) -> int:
    """
    The distance of two points
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from: dict, current: GridCell, draw: callable) -> None:
    """_summary_

    Args:
        came_from (_type_): _description_
        current (_type_): _description_
        draw (_type_): _description_
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw: callable, grid: np.array, start: GridCell, end: GridCell) -> bool:
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0

    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = characteristic_function(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        # Retrieve the current node with the lowest f_score
        current_node: GridCell = open_set.get()[2]
        open_set_hash.remove(current_node)

        # Check if we have reached the end
        if current_node == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        # Explore neighbors
        for neighbor in current_node.neighbors:
            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + characteristic_function(
                    neighbor.get_pos(), end.get_pos()
                )

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Mark as open

        # Mark the current node as visited
        if current_node != start:
            current_node.make_closed()

        draw()

        pygame.time.wait(20)

    return False
