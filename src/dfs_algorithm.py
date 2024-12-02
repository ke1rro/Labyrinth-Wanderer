"""DFS"""


def dfs_labirynt(matrix):
    '''
    Function that works in Deepth first
    search way to find a way out of the labirynth
    >>> matrix = [
    [1, 1, 1, 1],
    [0, 0, 2, 1],
    [1, 0, 1, 1],
    [1, 3, 1, 1]
    ]
    LDD
    '''
    start = None
    end = None
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 2:
                start = (i, j)
            elif matrix[i][j] == 3:
                end = (i, j)

    stack = [("", start)]

    directions = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1)
    }

    while len(stack) > 0:
        path, (x, y) = stack.pop()
        if (x, y) == end:
            return path

        for d, move in directions.items():
            new_x = x + move[0]
            new_y = y + move[1]
            if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[0]):
                if matrix[new_x][new_y] != 1:
                    stack.append((path + d, (new_x, new_y)))
                    matrix[new_x][new_y] = 1

    return "-1"


def res_dfs(matrix):
    """Transfers coordinates as letters into list of tuples

    Args:
        matrix (list): coordinates to transform

    Returns:
        list: list of tuples - coordinates

    """
    outp = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 2:
                start = (i, j)
                outp.append((start))
    path_dfs = dfs_labirynt(matrix)
    for i in path_dfs:
        f = outp[-1]
        if i == "U":
            outp.append(((int(f[0])-1), f[1]))
        elif i == "D":
            outp.append(((int(f[0])+1), f[1]))
        elif i == "L":
            outp.append((f[0], (int(f[1])-1)))
        elif i == "R":
            outp.append((f[0], (int(f[1]+1))))
    return outp


print(dfs_labirynt([[1, 1, 1, 1], [0, 0, 2, 1], [1, 0, 1, 1], [1, 3, 1, 1]]))
print(res_dfs([[1, 1, 1, 1], [0, 0, 2, 1], [1, 0, 1, 1], [1, 3, 1, 1]]))
