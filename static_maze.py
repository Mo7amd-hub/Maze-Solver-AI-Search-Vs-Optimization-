import numpy as np
from collections import deque
import matplotlib.pyplot as plt


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


def simulate (chromosome,maze,goal):
    x,y=0,0
    path = [(0, 0)]
    for gene in chromosome:
        newX,newY=x,y

        if gene==0: #up
            newX-=1
        if gene==1: #right
            newY+=1
        if gene==2: #down
            newX+=1
        if gene==3: #left
            newY-=1
        
        if(0<= newX < maze.shape[0]) and (0<= newY < maze.shape[1]) and maze[newX,newY]==0:
            x,y=newX,newY
            path.append((x, y))
            if (x, y) == goal:
                break
    return (x,y), path

def calculate_fitness(x,y,goal):
    distance = abs(goal[0]-x)+abs(goal[1]-y)
    score= -distance
    if distance==0:
        score+=1000
    return score

#--------------------------- Main Code -----------------------------------

maze = np.array([
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
goal=(9,9)


bfs_path = bfs(maze, (0, 0), goal)
print("Best path using BFS:", bfs_path)

fitness_scores=[]
paths=[]

cromosome_length=maze.size
population_size=100
population=np.random.randint(0,4,(population_size,cromosome_length))

for chromosome in population:
    print(f"\n\nchromosome: {chromosome}")
    
    final_pos,path=simulate(chromosome,maze,goal)
    x,y=final_pos
    paths.append(path)
    print(f"Final position: ({x}, {y})")

    fitness= calculate_fitness(x, y, goal)
    fitness_scores.append(fitness)
    print(f"fitness score: {fitness}")

best_index=np.argmax(fitness_scores)
best_chromosome=population[best_index]
ga_best_path=paths[best_index]
print(f"\n\nBest chromosome:\n {best_chromosome}")
print(f"It's fitness score: {fitness_scores[best_index]}")
print(f"It's path: {ga_best_path}")

#--------------------------- Visualization -----------------------------------

plt.imshow(maze, cmap='binary')

if bfs_path:
    bfs_y = [pos[0] for pos in bfs_path]
    bfs_x = [pos[1] for pos in bfs_path]
    plt.plot(bfs_x, bfs_y, color='blue', linewidth=3, label='BFS Path')

ga_y = [pos[0] for pos in ga_best_path]
ga_x = [pos[1] for pos in ga_best_path]
plt.plot(ga_x, ga_y, color='red', linewidth=3, linestyle='--', label='GA Path (Gen 1)')

plt.title("Maze Solver: BFS vs Genetic Algorithm")
plt.legend()
plt.xticks([])
plt.yticks([])
plt.show()