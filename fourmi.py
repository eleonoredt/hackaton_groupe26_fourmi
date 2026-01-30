import random

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
        for ville in self.tous_indices:
            if ville in chemin:
                probabilites.append(0)
            else:
                pheromone = self.pheromones[actuelle][ville] ** self.alpha
                heuristique = (1.0 / self.distances[actuelle][ville]) ** self.beta 
                probabilites.append(pheromone * heuristique) # Phéromone^alpha * (1/distance)^beta
        total = sum(probabilites) # pour la normalisation
        return [p / total for p in probabilites] if total > 0 else [0] * len(probabilites)
    
    def choisir_ville_suivante(self, probabilites):
        r = random.random()
        total = 0
        for i, p in enumerate(probabilites):
            total += p
            if total >= r:
                return i
        return len(probabilites) - 1
    
    def deposer_pheromones(self, tous_chemins):
        chemins_tries = sorted(tous_chemins, key=lambda x: x[1]) #car tous_chemins est une liste de tuple qui contient un chemin et sa distance totale et on trie en fonction de la distance
        for chemin, distance in chemins_tries[:self.n_meilleurs]:
            for i in range(len(chemin) - 1):
                self.pheromones[chemin[i]][chemin[i+1]] += 1.0 
    
    def generer_tous_chemins(self):
        tous_chemins = []
        for _ in range(self.n_fourmis):
            chemin = [random.randint(0, len(self.distances) - 1)] # on commence par une ville aléatoire
            while len(chemin) < len(self.distances):
                probabilites_mouvement = self.calculer_probabilites_mouvement(chemin)
                ville_suivante = self.choisir_ville_suivante(probabilites_mouvement)
                chemin.append(ville_suivante)
            tous_chemins.append((chemin, self.calcul_distance_chemin(chemin)))
    
    