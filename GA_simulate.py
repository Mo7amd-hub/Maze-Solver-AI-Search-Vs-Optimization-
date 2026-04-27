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