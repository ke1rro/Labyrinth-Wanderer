"""GUI for maze solving app"""

import csv
import random
import sys
import threading

import numpy as np
import pygame
import pygame.examples
import pygame_gui
import pygame_gui.windows.ui_file_dialog
from pygame_gui.core import ObjectID

import colors
from algos.bfs import bfs_algorithm
from dfs import dfs_labirynt
from maze import GridCell
from solver import algorithm

sys.setrecursionlimit(5000)


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

    def draw(self, grid: np.array) -> None:
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

    def make_list(self) -> list:
        """
        Makes 2D array from self.grid
        where 2 is start
        3 is end
        1 is a wall
        0 is a path
        """

        matrix = []
        for row in self.grid:
            matrix.append([
                1 if cell.is_barrier() else
                2 if cell.is_start() else
                3 if cell.is_end() else
                0
                for cell in row
            ])
        return matrix


class MazeApp:
    """Class that represents a main GUI window"""

    def __init__(self, height=1000, width=1600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.width, self.height = width, height
        self.running = True

        theme_path = "static/button.json"
        self.manager = pygame_gui.UIManager((width, height),
                                            theme_path=theme_path)

        self.upload_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 - 125, 150, 50),
            text="Upload Maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 - 75, 150, 50),
            text="Generate Maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 - 25, 150, 50),
            text="Save Solution",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.close = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 25, 150, 50),
            text="Close Maze Window",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.solve = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 75, 150, 50),
            text="Solve the maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.drop_menu_alg = pygame_gui.elements.UIDropDownMenu(
            options_list=["BFS", "DFS", "A*", "Dijkstra's"],
            starting_option="A*",
            relative_rect=pygame.Rect(25, self.height // 2 - 300, 150, 50),
            manager=self.manager,
            object_id=ObjectID(class_id="@drop"),
        )

        self.drop_menu_size = pygame_gui.elements.UIDropDownMenu(
            options_list=["10x10", "20x20", "25x25",
                          "50x50", "100x100", "150x150"],
            starting_option="50x50",
            relative_rect=pygame.Rect(1350, self.height // 2 - 300, 150, 50),
            manager=self.manager,
            object_id=ObjectID(class_id="@drop"),
        )

        self.random_generate = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 150, 150, 50),
            text="Random generation",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.solve.hide()
        self.close.hide()
        self.file_dialog_window = None
        self.maze_window = None

    def file_dialog(self) -> pygame_gui.windows.UIFileDialog:
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
                    maze.append(
                        [0 if cell.strip() == "." else 1 for cell in row])
            else:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    maze.append([0 if char == "." else 1 for char in line])
        return np.array(maze)

    def handle_solve_button(self, selected_algorithm) -> None:
        """Starts solving algothimn on the separete thread"""
        if (
            self.maze_window is not None
            and self.maze_window.start is not None
            and self.maze_window.end is not None
        ):
            for row in self.maze_window.grid:
                for cell in row:
                    cell.update_neighbors(grid=self.maze_window.grid)

            grid = self.maze_window.grid

            start = self.maze_window.start
            end = self.maze_window.end

            if selected_algorithm == "BFS":
                print("BFS")
                solve_thread = threading.Thread(
                    target=bfs_algorithm,
                    args=(lambda: self.maze_window.draw(grid), grid),
                )
                solve_thread.start()

            elif selected_algorithm == "A*":
                print("A*")
                solve_thread = threading.Thread(
                    target=algorithm,
                    args=(lambda: self.maze_window.draw(grid),
                          grid, start, end),
                )
                solve_thread.start()

            elif selected_algorithm == "DFS":
                print("DFS")
                matrix = self.maze_window.make_list()
                solve_thread = threading.Thread(
                    target=dfs_labirynt,
                    args=(matrix, grid,
                          lambda: self.maze_window.draw(grid))
                    )
                solve_thread.start()

    def generate_maze_array(self, width: int, height: int) -> np.ndarray:
        """
        Generates a maze using recursive DFS algorithm.

        Args:
            width (int): Width of the maze (number of columns).
            height (int): Height of the maze (number of rows).

        Returns:
            np.ndarray: A 2D numpy array representing the maze.
                        0 = path, 1 = wall.
        """
        maze = np.ones((height, width), dtype=int)

        def carve_maze(x, y):
            """Recursive function to carve the maze using DFS."""
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            random.shuffle(directions)
            # Randomize directions for natural-looking mazes

            for dx, dy in directions:
                nx, ny = (
                    x + dx * 2,
                    y + dy * 2,
                )  # Move two steps in the chosen direction
                if (
                    1 <= nx < width - 1
                    and 1 <= ny < height - 1 and maze[ny][nx] == 1
                ):
                    # Carve the path
                    maze[y + dy][x + dx] = 0  # Open the intermediate cell
                    maze[ny][nx] = 0  # Open the target cell
                    carve_maze(nx, ny)  # Recurse

        # Start carving from the top-left corner
        maze[1][1] = 0
        carve_maze(1, 1)

        # Open entrance and exit
        maze[1][0] = 0
        maze[height - 2][width - 1] = 0
        maze[height - 2][width - 2] = 0
        maze[height - 3][width - 2] = 0

        return maze

    def handle_resize(self, new_width, new_height) -> None:
        """Handles window resizing."""
        self.width, self.height = new_width, new_height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.manager.set_window_resolution((self.width, self.height))

    def run(self) -> None:
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

                        elif (
                            event.ui_element == self.close
                            and self.close is not None
                              ):

                            self.maze_window = None
                            self.close.hide()
                            self.solve.hide()

                        elif (
                            event.ui_element == self.solve
                            and self.maze_window is not None
                            and self.maze_window.start is not None
                            and self.maze_window.end is not None
                        ):

                            self.handle_solve_button(
                                self.drop_menu_alg.selected_option[0]
                            )

                        elif event.ui_element == self.random_generate:
                            if not self.maze_window:
                                # Get size from dropdown menu
                                option = int(
                                    self.drop_menu_size.selected_option[0].split("x")[0]
                                )

                                # Generate maze using DFS
                                maze_data = self.generate_maze_array(option,
                                                                     option)

                                # Create MazeWindow and update grid
                                self.maze_window = MazeWindow(option, 600)
                                grid = self.maze_window.make_grid()

                                # Map numpy array to grid cells
                                for i in range(option):
                                    for j in range(option):
                                        if maze_data[i][j] == 1:
                                            grid[i][j].make_barrier()

                                self.maze_window.grid = grid
                                self.close.show()
                                self.solve.show()

                        elif event.ui_element == self.generate_button:

                            if not self.maze_window:
                                option = int(
                                    self.drop_menu_size.selected_option[0].split("x")[0]
                                )
                                size = 600
                                if option > 100:
                                    size = 1200
                                self.maze_window = MazeWindow(option, size)
                                grid = self.maze_window.make_grid()
                                self.maze_window.grid = grid
                                self.close.show()
                                self.solve.show()

                        elif event.ui_element == self.save_button:
                            print("Save button pressed")
                            pygame.image.save(
                                self.maze_window.surface, "results/solve.jpg"
                            )

                    elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                        file_path = event.text
                        matrix = self.read_maze(file_path)
                        if matrix is not None:
                            row, col = matrix.shape
                            if row == col:
                                self.maze_window = MazeWindow(len(matrix), 600)
                                grid = self.maze_window.make_grid()
                                self.maze_window.grid = grid

                                for (i, j), col in np.ndenumerate(matrix):
                                    if col == 1:
                                        self.maze_window.grid[j, i].make_barrier()

                                self.solve.show()
                                self.close.show()

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
                            adjusted_pos = (pos[0] - maze_rect.x,
                                            pos[1] - maze_rect.y)
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
