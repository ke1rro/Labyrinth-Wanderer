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
Пошук в ширину (breadth-first-search)
Пошук в ширину (також БФС, BFS) гарантовано знаходить найкоротший шлях від початку до кінця графу. Цей алгоритм використовує принцип збереження "перший прийшов - перший вийшов", де всі сусіди теперішнього графу зберігаються в чергу.
БФС в цій програмі працює напряму з об'єктами матриці, що відразу й виводяться - GridCell. Для початку в матриці елементів за допомогою *find_start()* шукається елемент, позначений в пам'яті як старт:
![image](https://github.com/user-attachments/assets/ae79bb5f-f53b-457f-82b8-35c8e6cd83bb)

Черга зберігається в double ended queue (deque), туди відразу додаємо стартовий елемент. Також зберігається словник relations, що необхідний для правильного показу найкоротшого шляху.
Тоді викликається цикл, що діє поки в черзі наявні елементи.
![image](https://github.com/user-attachments/assets/775d4775-5c35-41c1-8240-6d5c585d1a33)

З черги береться елемент ліворуч, тобто той, що "потрапив" до черги першим. Якщо елемент не є стартом, то він позначається як "visited", тобто його вже немає потреби перевіряти. Тоді, за допомогою функції cached_neighbors, знаходяться всі сусіди клітинки на матриці. Тоді лишаємо сусідів, що:
-Не є стіною,
-Не є стартом,
-Не є оглянутими (не visited),
і додаємо їх до черги. Також зберігаємо їх до словника "відносин", де під ключем кожного з цих сусідів зберігаємо теперішній елемент.
![image](https://github.com/user-attachments/assets/51cb5d9c-f423-4a9f-a6da-0ae850003fec)

Якщо ж один з сусідів є кінцем, цей алгоритм ставить цього сусіда попереду черги, оскільки всі інші шляхи можна проігнорувати.
![image](https://github.com/user-attachments/assets/e9c865b2-11bf-45eb-9a4b-c78097c789d4)

Як тільки цикл доходить до кінцевого елемента, викликається функція backtrace(), яка виводить на екран правильний шлях:
![image](https://github.com/user-attachments/assets/53c3b06f-3072-44a3-add7-a23aea4bc0a0)

Оскільки ключем кожного з елементів є його "батьківський" елемент, ця функція, аби знайти правильний шлях, просто циклічно бере "батьківський" елемент кожного наступного "батьківського" елементу доти, доки не знайде початок.
