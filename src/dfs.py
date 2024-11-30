"""DFS"""

import numpy as np


def visualize_path(grid: np.array,
                   path: list[tuple[int, int]], draw: callable) -> None:
    """
    Visualizes the path on the maze grid.

    Args:
        grid (np.array): The grid containing the maze.
        path (list[tuple[int, int]]):
        The list of coordinates representing the path.
        draw (callable): A function to refresh the display after updates.
    """
    for step in path:
        row, col = step
        cell = grid[row][col]
        if not cell.is_start() and not cell.is_end():
            cell.make_path()
        draw()


def res_dfs(
    str_path: str, grid: np.array, draw: callable, start: tuple[int]
) -> tuple[int]:
    """
    Function to interpret the result of the dfs algorithm

    Args:
        str_path (str): path given as "DDRDL"
        grid (np.array): the numpy array with GridCell instances
        draw (callable): function to draw the maze
        start (tuple): the start coordinates of the function

    Returns:
        tuple[int]: tuple with the correct path coordinates
    """
    outp = [(start)]
    outp.append((start))

    for i in str_path:
        f = outp[-1]
        if i == "U":
            outp.append(((int(f[0]) - 1), f[1]))
        elif i == "D":
            outp.append(((int(f[0]) + 1), f[1]))
        elif i == "L":
            outp.append((f[0], (int(f[1]) - 1)))
        elif i == "R":
            outp.append((f[0], (int(f[1] + 1))))

    return visualize_path(grid, outp, draw)


def dfs_labirynt(matrix: list, grid: np.array, draw: callable) -> str:
    """
    Function that works in Deepth first search
    way to find a way out of the labirynth
    """
    start, end = None, None
    matrix_len = len(matrix)
    for i in range(matrix_len):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                start = (i, j)
            elif matrix[i][j] == 3:
                end = (i, j)

    directions = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

    stack = [("", start)]

    while stack:
        path_str, (x, y) = stack.pop()

        cell = grid[x][y]
        if not cell.is_start() and not cell.is_end():
            cell.make_closed()
            draw()

        if (x, y) == end:
            return res_dfs(path_str, grid, draw, start)

        for direction, move in directions.items():
            new_x, new_y = x + move[0], y + move[1]

            if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[0]):
                if matrix[new_x][new_y] == 0 or matrix[new_x][new_y] == 3:
                    stack.append((path_str + direction, (new_x, new_y)))
                    if matrix[new_x][new_y] != 3:
                        matrix[new_x][new_y] = -1
                        cell = grid[new_x][new_y]
                        cell.make_closed()
                        draw()
                    if matrix[new_x][new_y] == 3:
                        break

    return -1
