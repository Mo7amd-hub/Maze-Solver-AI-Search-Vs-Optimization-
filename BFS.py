from collections import deque

def bfs(maze, start, goal):
    row, col = maze.shape
    visited = {start}
    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        x, y = node

        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < row and 0 <= ny < col:
                if maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = node
                    queue.append((nx, ny))

    return []