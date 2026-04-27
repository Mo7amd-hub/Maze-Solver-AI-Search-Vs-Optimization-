import numpy as np

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

cromosome_length=maze.size
population_size=100
population=np.random.randint(0,4,(population_size,cromosome_length))

fitness_scores=[]
paths=[]

for chromosome in population:
    print(f"chromosome: {chromosome}")
    
    final_pos,path=simulate(chromosome,maze,goal)
    x,y=final_pos
    paths.append(path)
    print(f"Final position: ({x}, {y})")

    fitness= calculate_fitness(x, y, goal)
    fitness_scores.append(fitness)
    print(f"fitness score: {fitness}")

best_index=np.argmax(fitness_scores)
best_chromosome=population[best_index]
best_path=paths[best_index]
print(f"Best chromosome:\n {best_chromosome}")
print(f"It's fitness score: {fitness_scores[best_index]}")
print(f"It's path: {best_path}")