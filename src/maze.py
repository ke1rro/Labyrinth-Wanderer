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

    def get_pos(self) -> int:
        """
        Returns the position of cell
        """
        return self.x, self.y

    # Methods for the state of cell
    def is_closed(self) -> bool:
        """Check if the cell is visited."""
        return self.color == colors.RED

    def is_open(self) -> bool:
        """Check if the cell can be visited."""
        return self.color == colors.WHITE

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

    def make_start(self):
        """Sets the cell state into start"""
        self.color = colors.ORANGE

    def make_closed(self) -> None:
        """Sets the state of the cell into visited."""
        self.color = colors.WHITE

    def make_open(self) -> None:
        """Turn the cell into"""
        self.color = colors.GREEN

    def make_barrier(self) -> None:
        """Sets the state of the cell int barrier state."""
        self.color = colors.BLACK

    def make_end(self):
        """Sets the state of the cell as maze exit cell."""
        self.color = colors.TURQUIOSE

    def make_path(self):
        """Sets the state of the cell as the correct path to the end."""
        self.color = colors.PURPLE

    def draw(self, window: pygame.Surface):
        """Draw the cell to form the grid of the maze."""
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other: object) -> bool:
        """
        Custom comperrison method replaces the '<' operator.
        Compares the current cell with the other
        """
        return False


def characteristic_function(p1: tuple[int], p2: tuple[int]) -> int:
    """
    The distance of two points
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows: int, width: int) -> np.array:
    """
    Converts the cells into custome grid data type.
    Which stores all the cells
    """
    grid = []
    rows_gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = GridCell(i, j, rows_gap, rows)
            grid[i].append(cell)

    return np.array(grid)


def draw_grid(window: pygame.Surface, rows: int, width: int) -> None:
    """Draws the grid for the maze"""
    rows_gap = width // rows

    for i in range(rows):
        # Horizontal line for gird
        pygame.draw.line(window, colors.RED, (0, i * rows_gap), (width, i * rows_gap))
        for j in range(rows):
            # Vertical lines
            pygame.draw.line(window, colors.RED, (j * rows_gap, 0), (j * rows_gap, width))


def draw(window: pygame.Surface, grid: list[GridCell],
         rows: int, width: int) -> None:
    """Draws the cells with thier colors on the grid"""
    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def get_mouse_click_pos_on_grid(pos: int, rows: int, width: int) -> tuple[int]:
    """
    Get the mouse possition based on grid
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def run_maze(surface: pygame.Surface, width: int, rows: int) -> None:
    """
    Draws the maze on a given Pygame surface.

    Args:
        surface (pygame.Surface): The surface where the maze will be drawn.
        width (int): The width of the maze.
    """
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    is_solving_started = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if is_solving_started:
                continue

            # Left mouse click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_click_pos_on_grid(pos, rows, width)
                cell: GridCell = grid[row][col]
                if not start:
                    start = cell
                    start.make_start()
                elif not end:
                    end = cell
                    end.make_end()
                elif cell != end and cell != start:
                    cell.make_barrier()

            # Right mouse click
            if pygame.mouse.get_pressed()[2]:
                pass

        draw(surface, grid, rows, width)

    pygame.quit()
