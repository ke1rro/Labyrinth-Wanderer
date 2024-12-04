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

- **Uploading maze from csv file** - to upload the maze create a `.csv` file with `#` wall `.` path
- **Generate maze** - creates **empty canvas**, where user can draw. **First, orange cell** - start, **Second, blue cell - end**, next cells represent **barriers(walls)**. **To delete the wall** use **RIGHT MOUSE BUTTON**, also works for start and end.
- **Save Solution** - saves the image of solved labyrinth to `results/solution.jpg`
- **Random generation** - generates the maze of the given size using **DFS**
- **Left drop down menu** - to choose which algorithm to use
- **Right drop down menu** - to choose the size of the labyrinth/empty canvas
- **Right down corner** - timer of algorithm execution in seconds

> [!IMPORTANT]
> It is important that the given maze must be square.

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

---

## **Алгоритм Дейкстри**

## **Принцип дії:**

Алгоритм Дейкстри використовується, щоб знайти найкоротший шлях від однієї вершини графа до іншої, а також побудувати цей шлях. Спочатку встановлюється початкова вершина з відстанню 0, а всі інші отримують нескінченність. Алгоритм зберігає набір неперевірених вершин, у вигляді черги з пріоритетом, вибираючи кожного разу вершину з найменшою відстанню. Потім оновлює відстані до її сусідів, якщо новий шлях коротший за поточний, та фіксується попередник – вершина, з якої досягнуто найкоротший шлях. Процес повторюється доки не буде досягнута кінцева точка або не будуть відвідані всі вершини в які можливо потрапити з початкової. В кінці знаходиться найкоротший шлях. Він відновлюється шляхом проходження з кінцевої вершини до початкової через збережених попередників. Якщо були відвідані усі вершини, що мають зв’язок з першою, однак не було досягнуто кінця, то шляху від початкової вершини до кінцевої не існує.

## **Реалізація:**

### **Програма містить наступні функції:**

* ```matrix_to_adj_dict(maze: np.array) -> dict[tuple, sеt]```

    Ця функція приймає лабіринт у вигляді двовимірного NumPy array та переводить його в словник, де ключ це координати клітинки, а значення множина її сусідів, що не є стінкою.
    Вхідний словник містить 0, 1, 2, 3, де
    * 0 - порожня клітинка в лабіринті
    * 1 - стінка
    * 2 - старт
    * 3 - кінець
    (старт та кінець також порожні клітинки)
    Для цього вона ітерується по всіх елементах двовимірного списку ```maze``` та для кожної порожньої клітинки визначає її сусідів, перевіряючи кожну сусідню клітинку на порожність, якщо вона порожня то ця клітинка додається до множину сусідів. Також враховуються крайні випадки, коли клітинка знаходиться в першому/останньому рядку/стовпцю.

    ```python
    adjacent_dict[(row, col)] = set()
    if row != 0 and maze[row-1, col] != 1:
        adjacent_dict[(row, col)].add((row-1, col))
    if row != n-1 and maze[row+1, col] != 1:
        adjacent_dict[(row, col)].add((row+1, col))
    if col != 0 and maze[row, col-1] != 1:
        adjacent_dict[(row, col)].add((row, col-1))
    if col != n-1 and maze[row, col+1] != 1:
        adjacent_dict[(row, col)].add((row, col+1))
    ```

    ```row``` - номер рядка
    ```col``` - номер колонки
    ```n``` - розмір лабіринта
    ```maze``` - вхідний Numpy array
    ```adj_dict``` - словник суміжності, який функція створює
    Також функція визначає старт в лабіринті (позначений двійкою) та кінець (позначений трійкою)

    ```python
    if maze[row, col] == 2:
        start = (row, col)
    elif maze[row, col] == 3:
        end = (row, col)
    ```

    Функція повертає кортеж, що містить 3 елементи: координати старту, кінця та словник суміжності.

* ```dijkstra(maze: dict[tuple: set], start: tuple, end: tuple) -> dict[tuple, list] | int```

    Ця функція приймає словник суміжності отриманий в результаті
    виконання попередньої функції, старт та кінець. Повертає словник ```graph```, створений в результаті виконання цієї функції (його опис нижче), де за клітинкою попередником функція ```reconstruct_path``` відтворить шлях. Якщо шляху від старту до кінця немає, функція повертає -1. Функція використовує алгоритм Дейкстри, описаний вище.
    Для цього спочатку створюється словник ```graph```, де кожній вершині відповідає список, який містить поточну найкоротшу відстань від старту до вершини (При створенні для всіх вершин, крім старту відстань визначається як нескінченність, для старту 0), булеве значення (False для всіх крім старту, для нього True), яке позначає чи була відвідана поточна вершина, координати попередника (при створенні None для всіх крім старту, для нього його координати) - сусіда, ідучи з якого найкоротше потрапити в поточну. Також створюється черга з пріоритетом, яка буде містити кортежі, де перше його значення це відстань до клітинки, вона і буде пріоритетом в черзі (чим менша, тим більший пріоритет) та координати клітинки.

    ```python
    graph = {node: [float('inf'), False, None] for node in maze}
    graph[start] = [0, True, start]
    nodes_queue = PriorityQueue()
    nodes_queue.put((0, start))
    ```

    Потім в циклі ```While``` при кожній його ітерації з черги дістається вершина з найбільшим пріоритетом і вона визначається як поточна. Якщо вона є кінцевою, то найкоротший шлях до неї знайдено і повертається словник ```graph```. Якщо ні, то ця вершина позначається відвіданою і для кожної сусідньої з нею вершиною відстань перезаписується, якщо відстань через поточну вершину до сусідньої коротша ніж відстань записана в сусідній, у цьому випадку також перевизначається попередник і ця вершина разом з новою відстанню до неї поміщається в чергу. Потім відбувається перевірка на те чи вона не є порожньою, якщо вона порожня то це означає, що всі вершини, в які існує шлях зі старту вже були відвідані і серед них не було кінця, а отже шляху зі старту в кінець не існує, тому функція повертає -1.

* ```reconstruct_path(graph: dict, start: tuple, end: tuple) -> list[tuple]```
    Ця функція приймає словник ```graph```, старт та кінець. Та повертає найкоротший шлях у вигляду списку кортежів, де кожен кортеж це координати клітинки, яка відвідується на кожному кроці проходження цього шляху. Для цього функція починаючи з кінця йде до його попередника і додає його координати в список ```path``` потім з цього попередника йде до його попередника і додає його координати в список і так далі поки не буде досягнуто початку, тоді функція повертає список в зворотнбому порядку (зворотньому, бо шлях відбудовувався з кінця).

    ```python
    path = []
    cur_node = end
    while True:
        path.append(cur_node)
        if cur_node == start:
            break
        cur_node = graph[cur_node][2]
    return list(reversed(path))
    ```

* ```find_shortest_path(maze_matrix: np.array) -> list[tuple] | int```
    Ця функція об'єднує три попередні. Вона приймає лабіринт у вигляді двовимірного NumPy array та повертає найкоротший шлях у лабіринті від початку до кінця у вигляді списку кортежів, якщо він існує, інакше -1.

    ```python
    maze_dict, start, end = matrix_to_adj_dict(maze_matrix)
    graph = dijkstra(maze_dict, start, end)
    if graph != -1:
        return reconstruct_path(graph, start, end)
    return -1
    ```

---

## DFS алгоритм

Принцип пошуку у глибину - це алгоритм для обходу (у нашому випадку) графа до моменту знаходження виходу. На відміну від пошуку в ширину використовується stack замість queue.

Складається з двох частин:

1. Основна частина, яка порвертає шлях літерами

``` python
def dfs_labirynt(matrix):
    '''
    Function that works in Deepth first search way to find a way out of the labirynth
    >>> matrix =
    [1, 1, 1, 1],
    [0, 0, 2, 1],
    [1, 0, 1, 1]
    [1, 3, 1, 1]
    DDR
    '''
```

2. Допоміжна щоб перевести літери з список кортежів.

``` python
def res_dfs(matrix):
   '''
   Function that transfers the dfs_algorithm result into list of tuples
   >>> res_dfs([[1, 1, 1, 1],[0, 0, 2, 1],[1, 0, 1, 1],[1, 3, 1, 1]])
   [(1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1)]
   '''
```

## Як працює перша dfs_algorithm

1) задаються початкові координати :

``` python
start = None
   end = None
for i in range(len(matrix)):
       for j in range(len(matrix[i])):
           if matrix[i][j] == 2:
               start = (i, j)
           elif matrix[i][j] == 3:
               end = (i, j)
```

2) Підготовка до пошуку: використовуємо stack, адже для цього алгоритму нам потрібен саме він за принципом “Last in - First out”. Також додаємо словник з літерами координат

``` python
stack = [("", start)]
   directions = {
       "U": (-1, 0),
       "D": (1, 0),
       "L": (0, -1),
       "R": (0, 1)
}
```

3) Основний цикл пошуку шляху

Беремо поточну клітинку і шлях зі стеку, перевіряємо чи не є кінцем. Якщо так, то повертаємо шлях, як ні то продовжуємо цикл:

``` python
while len(stack) > 0:
       path, (x, y) = stack.pop()
       if (x, y) == end:
           return path
```

4) Розглядаємо всі координати та створюємо нові координати х та у. Перевіряємо, чи координати не виходять за межі матриці і чи не є стінкою. Тоді додаємо літеру напрямку та нові координати. Позначаємо відвідану клітинку 1

``` python
for d, move in directions.items():
           new_x = x + move[0]
           new_y = y + move[1]
           if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[0]):
               if matrix[new_x][new_y] != 1:
                   stack.append((path + d, (new_x, new_y)))
                   matrix[new_x][new_y] = 1
```

Якщо шлях не було знайдено, повертаємо ‘-1’.

Таким чином, отримавши таку матрицю на розгляд:

[1, 1, 1, 1]

[0, 0, 2, 1]

[1, 0, 1, 1]

[1, 3, 1, 1]

Ми отримали такий шлях: RDDLL

[(1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1)]

---

## A*

Алгоритм A* реалізує пошук найкоротшого шляху. У даній імплементації коду використовується манхеттенський метод. Алгоритм враховує перешкоди.
Використання бібліотеки heapq

### Використання бібліотеки heapq

Бібліотека використовується для роботи з чергою пріоритетів. В алгоритмі А* нам потрібно обирати вершину з найменшою вартістю кожного разу. `Heapq` дозволяє ефективно отримувати та додавати елементи у чергу, забезпечуючи високу швидкість програми. Його ефективність оцінюється як `O(logn)`.

#### Допоміжна функція

Алгоритм написано за допомогою метода Манхеттена, що вважається найоптимальнішим. Повертається абсолютна сума різниць координат осі х та у

``` python
def manhattan_distance(a, b):
    """Calculate the Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

Програма вважає, що 0 - клітина, якою можна рухатись, 1 - перешкода, 2 - стартова точка, 3 - кінцева точка. Шукаємо початок та кінець:

```python
# Find start and goal positions
start, goal = None, None
length_grid = len(grid)
for i in range(length_grid):
    for j in range(length_grid):
        if grid[i][j] == 2:
            start = (i, j)
        elif grid[i][j] == 3:
            goal = (i, j)
```

#### Робимо чергу пріоритетів

``` python
# Priority queue for nodes to explore
open_set = []
heapq.heappush(open_set, (0, start)) # (priority, position)
```

Пріоритет визначається як сума вартості досягнення точки g_score та як оцінка відстані до цілі

#### Визначаємо вартість шляху

``` python
# Tracking paths and costs
came_from = {} # To reconstruct the path
g_score = {start: 0} # Cost to reach each node
f_score = {start: manhattan_distance(start, goal)} # Estimated total cost
```

**g_score** визначає реальну вартість шляху до кожної клітини
**F_score** оцінює прогнозовану відстань до цілі

Головний цикл буде працювати поки в черзі open_set є точки для обробки

**Вибір клітини з найменшим пріоритетом**
вона стає поточною та видаляється з черги. Якщо поточна клітина є кінцевою ціллю, то програма повертає шлях до неї

```python
while open_set:
    # Get the node with the smallest f_score
    _, current = heapq.heappop(open_set)
    # If the goal is reached, reconstruct the path
    if current == goal:
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start)
        return path[::-1] # Return reversed path
```

Якщо ж ні, то ми шукаємо сусідів цієї клітини та перевіряємо чи знаходяться вони у межах сітки та чи є вони прохідними або кінцевими

```python
# Explore neighbors
x, y = current
neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
for neighbor in neighbors:
    nx, ny = neighbor
    # Check bounds and if the neighbor is walkable
    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] in (0, 3):
```

Далі розраховуємо вартість цієї клітини. Якщо новий шлях до сусіда коротший - оновлюється came_from, g_score та f_score. Сусід додається у чергу open_set

```python
# Calculate tentative g_score

tentative_g_score = g_score[current] + 1
if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
    # Update scores and add the neighbor to the priority queue came_from[neighbor] = current
    g_score[neighbor] = tentative_g_score
    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
    heapq.heappush(open_set, (f_score[neighbor], neighbor))
```

## Пошук в ширину (breadth-first-search)

Пошук в ширину (також БФС, BFS) гарантовано знаходить найкоротший шлях від початку до кінця графу. Цей алгоритм використовує принцип збереження "перший прийшов - перший вийшов", де всі сусіди теперішнього графу зберігаються в чергу.
БФС в цій програмі працює напряму з об'єктами матриці, що відразу й виводяться - GridCell. Для початку в матриці елементів за допомогою *find_start()* шукається елемент, позначений в пам'яті як старт:

```python
def find_start(coord_matrix: np.array) -> list:
    for row in coord_matrix:
        for cell in row:
            if cell.is_start():
                return [cell]
```

Черга зберігається в double ended queue (deque), туди відразу додаємо стартовий елемент. Також зберігається словник relations, що необхідний для правильного показу найкоротшого шляху.
Тоді викликається цикл, що діє поки в черзі наявні елементи.

```python
curr_node = queue.popleft()
```

З черги береться елемент ліворуч, тобто той, що "потрапив" до черги першим. Якщо елемент не є стартом, то він позначається як "visited", тобто його вже немає потреби перевіряти. Тоді, за допомогою функції cached_neighbors, знаходяться всі сусіди клітинки на матриці. Тоді лишаємо сусідів, що:
-Не є стіною,
-Не є стартом,
-Не є оглянутими (не visited),
і додаємо їх до черги. Також зберігаємо їх до словника "відносин", де під ключем кожного з цих сусідів зберігаємо теперішній елемент.

```python
if neighbor.is_unvisited() and not neighbor.is_start:
    queue.append(neighbor)
    relations[neighbor] = curr_node
    neighbor.make_open()
```

Якщо ж один з сусідів є кінцем, цей алгоритм ставить цього сусіда попереду черги, оскільки всі інші шляхи можна проігнорувати.

```python
if neighbor.is_end():
    queue.appendleft(neighbor)
    relations[neighbor] = curr_node
```

Як тільки цикл доходить до кінцевого елемента, викликається функція backtrace(), яка виводить на екран правильний шлях:

```python
def backtrace(draw: callable, relations: dict, end_node: GridCell):
    curr_node = end_node
    while True:
        curr_node.make_path()
        parent = relations[curr_node]
        draw()
        curr_node = parent
        if curr_node.is_start():
            break
```

Оскільки ключем кожного з елементів є його "батьківський" елемент, ця функція, аби знайти правильний шлях, просто циклічно бере "батьківський" елемент кожного наступного "батьківського" елементу доти, доки не знайде початок.
