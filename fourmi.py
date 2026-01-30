import random
import time
import threading
 
class AntColony:

    def __init__(self, distances, n_fourmis, n_meilleurs, n_iterations, decroissance, alpha : float=1, beta : float =2): 
        self.distances = distances
        self.pheromones = [[1.0 for _ in range(len(distances))] for _ in range(len(distances))]
        self.n_fourmis = n_fourmis
        self.n_meilleurs = n_meilleurs
        self.n_iterations = n_iterations
        self.decroissance = decroissance
        self.alpha = alpha # importance des pheromones dans le choix
        self.beta = beta # importance de la distance dans le choix
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
        return tous_chemins

    
    def run(self, callback_maj, evenement_arret):
        
        for iteration in range(self.n_iterations):
            if evenement_arret.is_set():
                break
            
            # on génère tous les chemins pour trouver le meilleur
            tous_chemins = self.generer_tous_chemins()
            self.deposer_pheromones(tous_chemins)
            self.meilleur_chemin = min(tous_chemins, key=lambda x: x[1])

            if self.meilleur_chemin[1] < self.meilleure_distance:  # mise à jour de la meilleure distance
                self.meilleure_distance = self.meilleur_chemin[1]
            
            self.pheromones = [[p * self.decroissance for p in ligne] for ligne in self.pheromones] #mise à jour des dépôts de phéromones

            callback_maj(iteration, self.meilleur_chemin, self.pheromones)
            
            time.sleep(0.2*len(self.distances)/10) #on fait une pause avant chaque itération pour permettre la mise à jour des données


if __name__ == "__main__":
    distances = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    
    colonie_fourmis = AntColony(distances, n_fourmis=4, n_meilleurs=5, n_iterations=100, decroissance=0.95, alpha=1, beta=2) #on crée une instance de la classe pour tester
    
    def callback_maj(iteration, meilleur_chemin, pheromones):
        
        if iteration % 10 == 0:
            print(f"Itération {iteration}: Meilleur chemin {meilleur_chemin} avec distance {colonie_fourmis.meilleure_distance}")
            print("Matrice des phéromones:")
            for ligne in pheromones:
                print(ligne)

    
    evenement_arret = threading.Event()
    
    colonie_fourmis.run(callback_maj, evenement_arret)
 
    print(f"Meilleur chemin trouvé : {colonie_fourmis.meilleur_chemin} avec une distance de {colonie_fourmis.meilleure_distance}")
    
    