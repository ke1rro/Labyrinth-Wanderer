"""Maze interaction"""

import numpy as np
import pygame

import colors


class GridCell:
    """
    Represents a cell in a maze grid.

    Colors meaning
        RED: visited
        WHITE: can be visited
        BLACK: barrier
        ORANGE: start point
        PURPLE: correct path
        GREENL: possible path
    """

    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.color = colors.WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_maze_pos(self) -> tuple[int]:
        """
        Returns the position of the cell in maze
        """
        return self.row, self.col

    def get_pos(self) -> tuple[int]:
        """
        Returns the position of cell on window
        """
        return self.x, self.y

    # Methods for the state of cell
    def is_unvisited(self) -> bool:
        """Checks if the cell is untracked"""
        return self.color == colors.WHITE

    def is_closed(self) -> bool:
        """Check if the cell is visited."""
        return self.color == colors.RED

    def is_open(self) -> bool:
        """Check if the cell can be visited."""
        return self.color == colors.GREEN

    def is_barrier(self) -> bool:
        """Checks if the cell is the wall of the maze."""
        return self.color == colors.BLACK

    def is_start(self) -> bool:
        """Checks for starting point in the the maze."""
        return self.color == colors.ORANGE

    def is_end(self) -> bool:
        """Checks if the cell if the exit from the maze."""
        return self.color == colors.TURQUIOSE

    def reset(self) -> None:
        """Sets the state of the cell to the passable."""
        self.color = colors.WHITE

    def make_start(self) -> None:
        """Sets the cell state into start"""
        self.color = colors.ORANGE

    def make_closed(self) -> None:
        """Sets the state of the cell into visited."""
        self.color = colors.RED

    def make_open(self) -> None:
        """Turn the cell into"""
        self.color = colors.GREEN

    def make_barrier(self) -> None:
        """Sets the state of the cell int barrier state."""
        self.color = colors.BLACK

    def make_end(self) -> None:
        """Sets the state of the cell as maze exit cell."""
        self.color = colors.TURQUIOSE

    def make_path(self) -> None:
        """Sets the state of the cell as the correct path to the end."""
        self.color = colors.PURPLE

    def draw_cell(self, window: pygame.Surface) -> None:
        """Draw the cell to form the grid of the maze."""
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid: np.array) -> None:
        """Check for the up, down, left, right neighbors"""

        self.neighbors = []
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other: object) -> bool:
        """
        Custom comperrison method replaces the '<' operator.
        Compares the current cell with the other
        """
        return False
