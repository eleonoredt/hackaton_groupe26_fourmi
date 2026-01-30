import flet as ft
import random
import math
import time
import threading
from fourmi import AntColony

def main(page: ft.Page):
    
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Variables pour le graphe
    nodes = []
    distances = []
    pheromones = []
    best_path = []
    iteration = 0
    running = False
    stop_event = threading.Event()
    
    # Paramètres d'entrée
    nodes_field = ft.TextField(label="Nombre de nœuds", value="10", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="30", width=150)
    best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
    iterations_field = ft.TextField(label="Itérations", value="200", width=150)
    decay_field = ft.TextField(label="Décay", value="0.95", width=150)
    alpha_field = ft.TextField(label="Alpha", value="1", width=150)
    beta_field = ft.TextField(label="Beta", value="2", width=150)

    # Contrôles d'affichage
    graph_container = ft.Container(
        width=600,
        height=500,
        bgcolor="white",
        border=ft.Border.all(1, "black")
    )
    
    iteration_text = ft.Text("Itération: 0", size=16)
    pheromone_text = ft.Text("Phéromones: ", size=14)
    path_text = ft.Text("Meilleur chemin: ", size=14)
    status_text = ft.Text("Prêt", size=14, color="green")
    
    def generer_nodes():
        nonlocal nodes, distances, pheromones
        try:
            num_nodes = int(nodes_field.value)
        except ValueError:
            num_nodes = 50
            
        nodes = []
        for _ in range(num_nodes):
            nodes.append((
                random.uniform(40, 560),
                random.uniform(40, 460)
            ))

        def calculer_distances():
            distances = []
            for i in range(len(nodes)):
                row = []
                for j in range(len(nodes)):
                    if i == j:
                        row.append(0)
                    else:
                        # Distance euclidienne
                        dx = nodes[i][0] - nodes[j][0]
                        dy = nodes[i][1] - nodes[j][1]
                        distance = math.sqrt(dx * dx + dy * dy)
                        row.append(distance)
                distances.append(row)
            return distances
        
        distances = calculer_distances()
        
        # Initialiser la matrice des phéromones
        pheromones = [[1.0 for _ in range(len(nodes))] for _ in range(len(nodes))]
    