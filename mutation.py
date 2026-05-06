import numpy as np

def mutate(chromosome, mutation_rate=0.05):
    
    for i in range(len(chromosome)):
        if np.random.rand() < mutation_rate:
            chromosome[i] = np.random.randint(0, 4)
            
    return chromosome