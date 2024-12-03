"""Maze app"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


if __name__ == "__main__":
    from src.gui import MazeApp
    app = MazeApp()
    app.run()
