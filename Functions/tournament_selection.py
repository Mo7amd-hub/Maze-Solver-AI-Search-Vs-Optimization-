import numpy as np

def tournament_selection(population, fitness_scores, tournament_size=3):

    selected_parents = []
    pop_size = len(population)
    
    for _ in range(pop_size):
        competitors_indices = np.random.randint(0, pop_size, tournament_size)
        
        best_idx = competitors_indices[0]
        for idx in competitors_indices:
            if fitness_scores[idx] > fitness_scores[best_idx]:
                best_idx = idx
        selected_parents.append(population[best_idx])
        
    return np.array(selected_parents)