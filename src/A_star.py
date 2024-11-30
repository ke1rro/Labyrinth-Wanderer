import heapq

def a_star_manhattan(grid, start, goal):
    """
    A* algorithm implementation with Manhattan distance heuristic.
    
    Parameters:
        grid: 2D list where 0 represents walkable cells, and 1 represents obstacles.
        start: Tuple representing the starting position (x, y).
        goal: Tuple representing the goal position (x, y).
        
    Returns:
        List of tuples representing the path from start to goal, or None if no path exists.
    """
    def manhattan_distance(a, b):
        """Calculate the Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Priority queue for nodes to explore
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, position)

    # Tracking paths and costs
    came_from = {}  # To reconstruct the path
    g_score = {start: 0}  # Cost to reach each node
    f_score = {start: manhattan_distance(start, goal)}  # Estimated total cost

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
            return path[::-1]  # Return reversed path

        # Explore neighbors
        x, y = current
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in neighbors:
            nx, ny = neighbor
            # Check bounds and if the neighbor is walkable
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                # Calculate tentative g_score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update scores and add the neighbor to the priority queue
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None