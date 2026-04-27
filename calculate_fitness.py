def calculate_fitness(x,y,goal):

    distance = abs(goal[0]-x)+abs(goal[1]-y)
    score= -distance
    if distance==0:
        score+=1000
        
    return score