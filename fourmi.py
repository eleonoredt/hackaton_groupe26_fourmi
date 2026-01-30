

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

    def calculer_probabilites_mouvement(self, chemin):
        actuelle = chemin[-1]
        probabilites = []
        # Pour chaque ville, calculer la probabilité de mouvement
        for ville in self.tous_indices:
            # Si la ville est dans le chemin, la probabilité est nulle
            if ville in chemin:
                probabilites.append(0)
            else:
                # Phéromone^alpha * (1/distance)^beta
                pheromone = self.pheromones[actuelle][ville] ** self.alpha
                heuristique = (1.0 / self.distances[actuelle][ville]) ** self.beta
                # Ajouter la probabilité au tableau
                probabilites.append(pheromone * heuristique)
        # Sommer les probabilités pour la normalisation
        total = sum(probabilites)
        # Retourner les probabilités normalisées
        return [p / total for p in probabilites] if total > 0 else [0] * len(probabilites)
    
    