"""GUI for maze solving app"""

import csv

import numpy as np
import pygame
import pygame_gui
import pygame_gui.windows.ui_file_dialog
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIWindow


class MazeWindow(UIWindow):
    def __init__(
        self, rows: int, width: int, ui_manager: pygame_gui.UIManager, rect: pygame.Rect
    ):
        super().__init__(
            rect,
            ui_manager,
            window_display_title="Everything Container",
            object_id="#everything_window",
            resizable=False,
        )
        self.rows = rows
        self.width = width

    def update(self, time_delta):
        super().update(time_delta)


class MazeApp:
    """Class that represents a main GUI window"""

    def __init__(self, height=800, width=1200):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.width, self.height = width, height
        self.running = True

        theme_path = "/Users/nikitalenyk/Desktop/maze_solver/static/button.json"
        self.manager = pygame_gui.UIManager((width, height), theme_path=theme_path)

        self.upload_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 - 50, 150, 50),
            text="Upload Maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2, 150, 50),
            text="Generate Maze",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25, self.height // 2 + 50, 150, 50),
            text="Save Solution",
            manager=self.manager,
            object_id=ObjectID(class_id="@menu"),
        )

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
        Start up function
        """

        while self.running:
            time_delta = self.clock.tick(60) / 1000.00
            self.screen.fill((30, 30, 30))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.upload_button:
                            self.file_dialog_window = self.file_dialog()
                            self.file_dialog_window.show()

                        elif event.ui_element == self.generate_button:
                            if not self.maze_window:
                                self.maze_window = MazeWindow(
                                    100,
                                    100,
                                    self.manager,
                                    pygame.Rect(300, 300, 300, 300),
                                )
                        elif event.ui_element == self.save_button:
                            print("Save button pressed")

                    elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                        file_path = event.text
                        matrix = self.read_maze(file_path)

                    elif event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                        if event.ui_element == self.maze_window:
                            print("Maze window closed")
                            self.maze_window = None


                elif event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event.w, event.h)

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    app = MazeApp()
    app.run()
