from collections import deque
from enum import Enum
import pygame
import numpy as np
from maze import GridCell

class GraphErrorType(Enum):
    '''
    Different types of enum errors.
    '''
    NO_START = 'No starting coordinates found'
    MULTIPLE_STARTS = 'Multiple starting coordinates found'
    NO_EXIT = 'No exit coordinates found'
    MULTIPLE_EXITS = 'Multiple exit coordinates found'
    WRONG_MATRIX_SIZE = ''

class GraphException(Exception):
    '''
    Different exceptions related to graphs.
    '''
    def __init__(self, error: GraphErrorType):
        super().__init__(error.value)

def find_start(coord_matrix: np.array) -> GridCell:
    '''
    Finds the start of a labyrinth.
    The start is given as 2.
    Every labyrinth should
    '''
    start_els=[]
    for row in coord_matrix:
        for el in row:
            if el.is_start():
                start_els.append(el)
    if len(start_els)==0:
        return GraphException(GraphErrorType.NO_START)
    if len(start_els)>2:
        return GraphException(GraphErrorType.MULTIPLE_STARTS)
    return start_els[0]

def backtrace(relations: dict,end_node: GridCell):
    '''
    Highlights the correct path after the search algorithm is done.
    '''
    curr_node = end_node
    while True:
        curr_node.make_path()
        parent = relations[curr_node]
        draw()
        curr_node = parent
        if curr_node.is_start():
            break
def bfs_algorithm(draw: callable, coord_matrix: np.array):
    '''
    Finds the shortest path to the exit using the
    breadth-first-search algorithm.
    '''
    start=find_start(coord_matrix)
    queue = deque(start)
    relations={} #This is needed to be able to highlight the path afterwards.
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr_node = queue.popleft()
        if curr_node.is_end():
            backtrace(relations,curr_node)
            return True
        if not curr_node.is_start():
            curr_node.make_closed()
        curr_node.update_neighbors(coord_matrix)
        for neighbor in curr_node.neighbors:
            if neighbor.is_open() and not neighbor.is_start():
                queue.append(neighbor)
                relations[neighbor] = curr_node
            if neighbor.is_end():
                queue.appendleft(neighbor)
                relations[neighbor] = curr_node
        draw()
    return False
