"""A-start with visualization"""

import heapq

import numpy as np


def a_star_manhattan(grid: license, grid_cells: np.array, draw: callable):
    """
    A* algorithm implementation with Manhattan distance heuristic.

    Parameters:
        grid: 2D list where:
              - 0 represents walkable cells,
              - 1 represents obstacles,
              - 2 represents the starting position,
              - 3 represents the goal position.
    Returns:
        List of tuples representing the
        path from start to goal, or None if no path exists.
    """

    def manhattan_distance(a, b):
        """Calculate the Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Find start and goal positions
    start, goal = None, None
    length_grid = len(grid)
    for i in range(length_grid):
        for j in range(length_grid):
            if grid[i][j] == 2:
                start = (i, j)
            elif grid[i][j] == 3:
                goal = (i, j)

    # Priority queue for nodes to explore
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, position)

    # Tracking paths and costs
    came_from = {}  # To reconstruct the path
    g_score = {start: 0}  # Cost to reach each node
    f_score = {start: manhattan_distance(start, goal)}  # Estimated total cost

    while open_set:
        # Get the node with the smallest f_score
        _, current = heapq.heappop(open_set)

        # If the goal is reached, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                x, y = current
                grid_cells[x][y].make_path()
                draw()
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return reversed path

        # Explore neighbors
        x, y = current
        grid_cells[x][y].make_closed()
        draw()
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for neighbor in neighbors:
            nx, ny = neighbor
            # Check bounds and if the neighbor is walkable
            if (
                0 <= nx < len(grid)
                and 0 <= ny < len(grid[0])
                and grid[nx][ny] in (0, 3)
            ):
                # Calculate tentative g_score
                tentative_g_score = g_score[current] + 1

                if (neighbor not in g_score or
                        tentative_g_score < g_score[neighbor]):
                    # Update scores and add the neighbor to the priority queue
                    grid_cells[nx][ny].make_open()
                    draw()
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(
                        neighbor, goal
                    )
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None
