import numpy as np
from collections import deque
import matplotlib.pyplot as plt


#--------------------------- BFS Algorithm -----------------------------------
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



#---------------------------- Genetic Algorithm -----------------------------------
def generate_population(pop_size, chromosome_length):
    population = np.random.randint(0, 4, (pop_size, chromosome_length))
    return population


def simulate(chromosome, maze, goal):
    x,y=0,0
    path = [(x,y)]

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

        if (0<=newX<maze.shape[0]) and (0<=newY<maze.shape[1]) and (maze[newX][newY]==0):
            x,y=newX,newY
            path.append((x,y))

        if (x,y)==goal:
            break
    
    return (x,y), path


def calculate_fitness(x,y,goal):
    distance = abs(goal[0]-x)+abs(goal[1]-y)
    score= -distance
    if distance==0:
        score+=1000
    return score


def tournament_selection(population, fitness_scores, tournament_size):
    selected_parents=[]
    pop_size=len(population)

    for _ in range(pop_size):
        competitors_indices = np.random.randint(0 , pop_size, tournament_size)
        best_index = competitors_indices[0]

        for idx in competitors_indices:
            if fitness_scores[idx] > fitness_scores[best_index]:
                best_index=idx
        selected_parents.append(population[best_index])
    
    return np.array(selected_parents)



def crossover(p1, p2):

    point = np.random.randint(1, len(p1)-1)

    c1= np.concatenate((p1[:point], p2[point:]))
    c2= np.concatenate((p2[:point], p1[point:]))
    return c1,c2



def mutate(chromosome, mutation_rate):

    for i in range(len(chromosome)):
        if np.random.random() < mutation_rate:
            chromosome[i] = np.random.randint(0, 4)
    return chromosome



def run_genetic_algorithm(maze, goal, pop_size=100, max_generations=150, chromosome_length=200):
    
    population = generate_population(pop_size, chromosome_length)
    
    best_fitness_history = []
    best_overall_path = []
    best_overall_fitness = -float('inf')

    # Evolution loop
    for gen in range(max_generations):
        fitness_scores = []
        paths = []
        
        for chromosome in population:
            final_pos, path = simulate(chromosome, maze, goal)
            fitness = calculate_fitness(final_pos[0], final_pos[1], goal)
            fitness_scores.append(fitness)
            paths.append(path)
            
        current_best_fitness = max(fitness_scores)
        best_index = fitness_scores.index(current_best_fitness)
        best_fitness_history.append(current_best_fitness)
        
        if current_best_fitness > best_overall_fitness:
            best_overall_fitness = current_best_fitness
            best_overall_path = paths[best_index]

        print(f"Generation {gen + 1} | Best Fitness: {current_best_fitness}")

        # Termination conditions
        if current_best_fitness >= 1000:
            print(f"\n Goal Reached at Generation {gen+1}!")
            break

        if len(best_fitness_history) > 10 and len(set(best_fitness_history[-10:])) == 1:
            print(f"\n [TERMINATION] Convergence reached at Generation {gen+1}. Stuck in Local Optima.")
            break

        #next generation    
        parents = tournament_selection(population, fitness_scores, tournament_size=3)    
        next_generation = []
        
        sorted_indices = np.argsort(fitness_scores)[::-1]
        next_generation.extend([population[sorted_indices[0]], population[sorted_indices[1]]])
        for i in range(0, len(parents) - 2, 2):
            p1 = parents[i]
            p2 = parents[i+1] if i+1 < len(parents) else parents[0]
            c1, c2 = crossover(p1, p2)
            
            c1 = mutate(c1, mutation_rate=0.05)
            c2 = mutate(c2, mutation_rate=0.05)
            next_generation.extend([c1, c2])
            
        population = np.array(next_generation[:pop_size])

    return best_overall_path


#--------------------------- Main Code -----------------------------------
maze = np.array([
    [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,1,1,0,1,1,0,1,1,1,1,0,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1,0],
    [0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
    [0,1,0,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0],
    [0,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,0],
    [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
    [1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
])
goal = (19, 19)

bfs_actual_path = bfs(maze, (0, 0), goal)
print("Best path using BFS:", bfs_actual_path)

best_ga_path = run_genetic_algorithm(maze, goal, 100, 100, 200)
print("Best path using Genetic Algorithm:", best_ga_path)

#--------------------------- Visualization -----------------------------------

plt.figure(figsize=(8, 8))
plt.imshow(maze, cmap='binary')

if bfs_actual_path:
    bfs_y = [pos[0] for pos in bfs_actual_path]
    bfs_x = [pos[1] for pos in bfs_actual_path]
    plt.plot(bfs_x, bfs_y, color='blue', linewidth=8, alpha=0.4, label='BFS Path (Optimal)')

if best_ga_path:
    ga_y = [pos[0] for pos in best_ga_path]
    ga_x = [pos[1] for pos in best_ga_path]
    plt.plot(ga_x, ga_y, color='red', linewidth=3, linestyle='-', label='GA Path (Evolved)')

plt.title("Maze Solver 20x20: BFS vs Genetic Algorithm")
plt.legend()
plt.xticks([])
plt.yticks([])
plt.show()