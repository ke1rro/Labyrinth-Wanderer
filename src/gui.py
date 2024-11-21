"""GUI for maze solving app"""

import csv

import numpy as np
import pygame
import pygame_gui
import pygame_gui.windows.ui_file_dialog
from pygame_gui.core import ObjectID

import colors
from maze import GridCell, algorithm


class MazeWindow:
    """
    Class represents the maze window

    rows: number of rows in maze
    width: width length of the maze
    """

    def __init__(
        self,
        rows: int,
        width: int,
    ):

        self.rows = rows
        self.width = width
        self.surface = pygame.Surface((self.width, self.width))
        self.grid = []
        self.start = None
        self.end = None

    def make_grid(self) -> np.array:
        """
        Converts the cells into custome grid data type.
        Which stores all the cells
        """
        grid = []
        rows_gap = self.width // self.rows

        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                cell = GridCell(i, j, rows_gap, self.rows)
                grid[i].append(cell)

        return np.array(grid)

    def draw_grid(self) -> None:
        """Draws the grid for the maze"""
        rows_gap = self.width // self.rows

        for i in range(self.rows):
            # Horizontal line for gird
            pygame.draw.line(
                self.surface,
                colors.BLACK,
                (0, i * rows_gap),
                (self.width, i * rows_gap),
            )
            for j in range(self.rows):
                # Vertical lines
                pygame.draw.line(
                    self.surface,
                    colors.BLACK,
                    (j * rows_gap, 0),
                    (j * rows_gap, self.width),
                )

    def draw(self, grid):
        """Draws the colors of the each cell and whole grid"""
        self.surface.fill(colors.BLACK)
        for row in grid:
            for cell in row:
                cell.draw_cell(self.surface)
        self.draw_grid()

    def get_mouse_click_pos_on_grid(self, pos: int) -> tuple[int]:
        """
        Get the mouse possition based on grid
        """
        gap = self.width // self.rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col


class MazeApp:
    """Class that represents a main GUI window"""

    def __init__(self, height=1000, width=1600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.width, self.height = width, height
        self.running = True

        theme_path = "/Users/nikitalenyk/Desktop/maze_solver/static/button.json"
        self.manager = pygame_gui.UIManager((width, height), theme_path=theme_path)

        self.upload_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 - 75, 150, 50),
            text="Upload Maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 - 25, 150, 50),
            text="Generate Maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 25, 150, 50),
            text="Save Solution",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.close = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 75, 150, 50),
            text="Close Maze Window",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.solve = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 125, 150, 50),
            text="Solve the maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.solve.hide()
        self.close.hide()
        self.file_dialog_window = None
        self.maze_window = None

    def file_dialog(self):
        """Creates and returns a centered file dialog."""
        dialog_width = 500
        dialog_height = 600
        dialog_x = (self.width - dialog_width) // 2
        dialog_y = (self.height - dialog_height) // 2

        file_dialog = pygame_gui.windows.UIFileDialog(
            rect=pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height),
            window_title="Select CSV file with maze",
            manager=self.manager,
            object_id="#file_dialog",
        )
        return file_dialog

    def read_maze(self, file: str) -> np.ndarray:
        """
        Read a CSV file that represents a maze with "." and "#".
        Handles files with or without commas as delimiters.
        Ignores empty rows.

        Args:
            file (str): Path to the CSV file.

        Returns:
            np.ndarray: 2D array with 0 for paths and 1 for walls.
        """
        maze = []

        with open(file, "r", encoding="utf-8") as f:
            sample = f.read(1024)
            f.seek(0)
            try:
                delimiter = csv.Sniffer().sniff(sample).delimiter
            except csv.Error:
                delimiter = None

            if delimiter:
                data = csv.reader(f, delimiter=delimiter)
                for row in data:
                    if not row or all(cell.strip() == "" for cell in row):
                        continue
                    maze.append([0 if cell.strip() == "." else 1 for cell in row])
            else:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    maze.append([0 if char == "." else 1 for char in line])
        return np.array(maze)

    def handle_resize(self, new_width, new_height):
        """Handles window resizing."""
        self.width, self.height = new_width, new_height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.manager.set_window_resolution((self.width, self.height))

    def run(self):
        """
        Handling events for maze app
        """
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            self.screen.fill((30, 30, 30))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.USEREVENT:

                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if (
                            event.ui_element == self.upload_button
                            and self.maze_window is None
                        ):
                            self.file_dialog_window = self.file_dialog()
                            self.file_dialog_window.show()

                        elif event.ui_element == self.close and self.close is not None:
                            self.maze_window = None
                            self.close.hide()
                            self.solve.hide()

                        elif (
                            event.ui_element == self.solve
                            and self.maze_window is not None
                            and self.maze_window.start is not None
                            and self.maze_window.end is not None
                        ):
                            for row in self.maze_window.grid:
                                for cell in row:
                                    cell.update_neighbors(grid=self.maze_window.grid)

                            grid = self.maze_window.grid
                            start = self.maze_window.start
                            end = self.maze_window.end
                            algorithm(
                                lambda: self.maze_window.draw(grid), grid, start, end
                            )

                        elif event.ui_element == self.generate_button:
                            if not self.maze_window:
                                self.maze_window = MazeWindow(50, 600)
                                grid = self.maze_window.make_grid()
                                self.maze_window.grid = grid
                                self.close.show()
                                self.solve.show()

                        elif event.ui_element == self.save_button:
                            print("Save button pressed")

                    elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                        file_path = event.text
                        matrix = self.read_maze(file_path)

                elif pygame.mouse.get_pressed()[0]:
                    if self.maze_window is not None:
                        pos = pygame.mouse.get_pos()
                        maze_rect = self.maze_window.surface.get_rect()
                        maze_rect.center = (self.width // 2, self.height // 2)

                        if maze_rect.collidepoint(pos):
                            adjusted_pos = (pos[0] - maze_rect.x, pos[1] - maze_rect.y)
                            row, col = self.maze_window.get_mouse_click_pos_on_grid(
                                adjusted_pos
                            )
                            cell: GridCell = self.maze_window.grid[row][col]

                            if (
                                not self.maze_window.start
                                and cell != self.maze_window.end
                            ):
                                self.maze_window.start = cell
                                self.maze_window.start.make_start()
                            elif (
                                not self.maze_window.end
                                and cell != self.maze_window.start
                            ):
                                self.maze_window.end = cell
                                self.maze_window.end.make_end()
                            elif (
                                cell != self.maze_window.start
                                and cell != self.maze_window.end
                            ):
                                cell.make_barrier()
                elif pygame.mouse.get_pressed()[2]:

                    if self.maze_window is not None:
                        pos = pygame.mouse.get_pos()
                        maze_rect = self.maze_window.surface.get_rect()
                        maze_rect.center = (self.width // 2, self.height // 2)
                        if maze_rect.collidepoint(pos):
                            adjusted_pos = (pos[0] - maze_rect.x, pos[1] - maze_rect.y)
                            row, col = self.maze_window.get_mouse_click_pos_on_grid(
                                adjusted_pos
                            )
                            cell: GridCell = self.maze_window.grid[row][col]
                            if self.maze_window.start == cell:
                                self.maze_window.start = None
                            elif self.maze_window.end == cell:
                                self.maze_window.end = None
                            cell.reset()

                elif event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event.w, event.h)

                self.manager.process_events(event)

            if self.maze_window:
                self.maze_window.draw(self.maze_window.grid)
                maze_rect = self.maze_window.surface.get_rect()
                maze_rect.center = (self.width // 2, self.height // 2)
                self.screen.blit(self.maze_window.surface, maze_rect)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    app = MazeApp()
    app.run()
