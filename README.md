# Labyrinth Wanderer

![alt text](img/LabWanderer.png)

## Maze solving algorithms

- Breadth First Search - Левицький Тарас
- Depth First Search - Лукашенко Поліна
- A* Search - Васильченко Владислав
- Dijkstra’s Algorithm - Засимович Богдан
- Gui & code reviews - Леник Нікіта

---

## Features

- **Uploading maze from csv file** - `#` wall `.` path
- **Generate maze** - creates **empty canvas**, where user can draw. **First, orange cell** - start, **Second, blue cell - end**, next cells represent **barriers(walls)**. **To delete the wall** use **RIGHT MOUSE BUTTON**, also works for start and end.
- **Save Solution** - saves the image of solved labyrinth to `results/solution.jpg`
- **Random generation** - generates the maze of the given size using **DFS**
- **Left drop down menu** - to choose which algorithm to use
- **Right drop down menu** - to choose the size of the labyrinth/empty canvas
- **Right down corner** - timer of algorithm execution in seconds

---
![alt text](</img/gui.png>)

---

## Project Structure

```bash
.
├── main.py # Entry point start this file to run the app
├── requirements.txt
├── results # Directory with labyrinth solutions
│   └── solution.jpg
├── src
│   ├── a_star.py # A*
│   ├── a_star_visual.py # A* implemented with visualisation
│   ├── bfs.py # BFS implemented with visualisation(only)
│   ├── colors.py # constants
│   ├── dfs.py # DFS implemented with visualisation
│   ├── dfs_algorithm.py # DFS
│   ├── dijkstra.py # Dijkstra
│   ├── dijkstra_algorithm.py # Dijkstra implemented with visualisation
│   ├── greedy_a_star.py # Greedy A* implemented with visualisation(only)
│   ├── gui.py # GUI file
│   └── maze.py # GridCell class
├── static
│   └── theme.json
│   # Test labyrinth
├── test_100.csv
├── test_150.csv
└── test_400.csv
```

---

## Requirements

```txt
numpy==2.1.3
pygame==2.6.1
pygame_gui==0.6.12
```

---

## To run the program

```bash
pip install -r requirements.txt

python main.py
```

---

## Звіт

### Проєкт

Наш проєкт представляє застосунок для порівняння та візуалізації виконання алгоритмів. Для реалізації ми вирішили використати бібліотеки `Pygame`, `Pygame_gui` та `NumPy`.

### Складові візуального інтерфейсу

Інтерфейс представляє об'єкт класу `MazeApp`, який має атрибути, зокрема:

Кнопки, що відповідають за завантаження лабіринту через файл, створення порожнього полотна для лабіринту, збереження розв’язаного лабіринту, генерацію лабіринту за допомогою `DFS`.
Спадне меню, яке дозволяє вибрати алгоритм розв’язання лабіринту та задати розмір полотна.
Таймер, який використовується для вимірювання часу виконання алгоритму.

Також для відображення самого лабіринту та його полотна використовується об'єкт класу `MazeWindow`, який створюється лише за умови, що користувач натиснув кнопку, яка відповідає за його створення. Клас відповідає за рендеринг полотна лабіринту та забезпечення взаємодії з користувачем.

### Взаємодія з лабіринтом

Взаємодія з лабіринтом відбувається за допомогою класу `GridCell`, який представляє одну клітинку (вершину) в лабіринті. Всі об'єкти класу `GridCell` зберігаються в атрибуті `grid` класу `MazeWindow`.

#### Grid cell

Об'єкт цього класу представляє єдину вершину в лабіринті, яка має такі атрибути:

- Розташування відносно екрану.
- Координати: колонка та рядок.
- Сусідів, яких може бути лише чотири (зверху, знизу, зліва та справа).
- Колір, який відображає її стани.

##### Стани вершини

- Червоний — вершина відвідана.
- Білий — вершина не була відвідана.
- Чорний — вершина є бар’єром.
- Помаранчевий — вершина є входом у лабіринт.
- Синій — вихід з лабіринту.
- Фіолетовий — правильний шлях від входу до виходу.

Також клас має методи, які дають змогу перевірити та змінити стан кожної клітинки.

Важливим методом для реалізації алгоримту `A*` є

``` python
def __lt__(self, other: object) -> bool:
    """
    Custom comperrison method replaces the '<' operator.
    Compares the current cell with the other
    """
    return False
```

**\__lt\__(less_than)** - гарантує, що будь-яке порівняння двох обʼєктів поверне **False**. Це буде використане у подальшій реалізації алгоритму.

### Випадкова генерація лабіринту

Для випадкової генерації лабіринту використовується пошук в глибину.

1. За допомогою numpy.ones() створюємо квадратну матрицю з одиниць, які відображають стінки.

2. Задаємо координати (вгору, вниз, вліво, вправо), які при кожному виклику функції перемішуються випадковим чином.

3. Ітеруємося по заданим координатам і задаємо нові координати, що віддалені на два кроки від попередніх x, y.

4. Якщо нові координати nx, ny не виходять за межі лабіринту і значення в матриці дорівнює 1, то задаємо клітинці значення 0, що формує майбутній прохід у лабіринті.

5. Викликаємо функцію знову, поки умова з пункту 4 не виконається.
