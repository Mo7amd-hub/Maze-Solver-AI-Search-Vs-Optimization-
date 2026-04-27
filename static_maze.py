import numpy as np

def simulate (chromosome,maze,goal):
    x,y=0,0

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
            if (x, y) == goal:
                break
    return (x,y)
    

def calculate_fitness(x,y,goal):
    distance = abs(goal[0]-x)+abs(goal[1]-y)
    score= -distance
    if distance==0:
        score+=1000
    return score
#--------------------------- Main Code -----------------------------------

maze=np.random.randint(0,2,(10,10))
maze[0, 0] = 0
maze[9, 9] = 0
goal=(9,9)

cromosome_length=maze.size
population_size=100
population=np.random.randint(0,4,(population_size,cromosome_length))

fitness_scores=[]

for chromosome in population:
    print(f"chromosome: {chromosome}")
    
    x,y=simulate(chromosome,maze,goal)
    print(f"Final position: ({x}, {y})")

    fitness= calculate_fitness(x, y, goal)
    fitness_scores.append(fitness)
    print(f"fitness score: {fitness}")