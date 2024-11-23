def dfs_labirynt(matrix):
    '''
    Function that works in Deepth first search way to find a way out of the labirynth
    >>> matrix = [
    [1, 1, 1, 1],
    [2, 0, 0, 1],
    [1, 0, 1, 1],
    [1, 3, 1, 1]
    ]
    DDR
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
                if matrix[new_x][new_y] != 0:
                    stack.append((path + d, (new_x, new_y)))
                    matrix[new_x][new_y] = 0

    return "The way not found"
