# Labyrinth Wanderer

![alt text](img/LabWanderer.png)

## Maze solving algorithms

- Breadth First Search - Левицький Тарас
- Depth First Search - Лукашенко Поліна
- A* Search - Васильченко Владислав
- Dijkstra’s Algorithm - Засимович Богдан
- Gui & code reviews - Леник Нікіта

---

## Project Structure

```bash
.
├── results
│   └── solve.jpg # Photos with the correct path to the given maze
├── src
│   ├── colors.py # Constants
│   ├── gui.py # User Interface module
│   ├── maze.py # GridCell class
│   ├── bfs.py # Breadth-First-Search algorithm
│   ├── dfs.py # Depth-First-Search algorithm
│   ├── astar.py # A* algorithm
│   ├── djikstra.py # Djikstra algorithm
│   └── solver.py # Main utility for solving algorithms
├── static
│   └── button.json # Themes for GUI
└── test.csv # Test file for maze solving
```

## Requirements

```txt
numpy==2.1.3
pygame==2.6.1
pygame_gui==0.6.12
```

```bash
pip install -r requirements.txt
```

## IF YOU WANT TO IMPLEMENT ANY ALGORITHM FOLLOW THESE STEPS

    1. Create a branch with the algorithm name
    2. Code the algorithm up to the data structure based on the MAZE class
    3.
        1. Commit
        2. Push
        3, Pull request
    4. Done
