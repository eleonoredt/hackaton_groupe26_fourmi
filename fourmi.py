

class AntColony:

    def __init__(self, distances, n_fourmis, n_meilleurs, n_iterations, decroissance, alpha : float=1, beta : float =2): 
        self.distances = distances
        self.pheromones = [[1.0 for _ in range(len(distances))] for _ in range(len(distances))]
        self.n_fourmis = n_fourmis
        self.n_meilleurs = n_meilleurs
        self.n_iterations = n_iterations
        self.decroissance = decroissance
        self.alpha = alpha
        self.beta = beta
        self.tous_indices = range(len(distances))
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')
    
    def calcul_distance_chemin(self, chemin) : 
        total = 0
        for i in range(len(chemin) - 1):
            total += self.distances[chemin[i]][chemin[i+1]]
        return total
    
    