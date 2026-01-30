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
    
    def create_line(x1, y1, x2, y2, color, thickness): #cette fontion sert a dessiner les lignes entre les noeuds

        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        return ft.Container(
            width=length,
            height=thickness,
            bgcolor=color,
            left=x1,
            top=y1 - thickness/2,
            rotate=ft.Rotate(angle=angle, alignment=ft.alignment.Alignment(-1, 0))
        )
    
    def draw_graph():
        shapes = []
        
        if pheromones and len(pheromones) > 0:
            max_pheromone = max(max(row) for row in pheromones) if pheromones else 1
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    if pheromones[i][j] > 0.1:  #on définit un seuil minimal pour le dépôt de phéromones
                        opacity = min(1, pheromones[i][j] / max_pheromone)
                        thickness = max(1, (pheromones[i][j] / max_pheromone) * 3)

                        line = create_line(
                            nodes[i][0], nodes[i][1],
                            nodes[j][0], nodes[j][1],
                            ft.Colors.with_opacity(opacity, ft.Colors.BLUE),
                            thickness
                        )
                        shapes.append(line)
        
        # dessin du meilleur chemin 

        if best_path:                                   
            for i in range(len(best_path) - 1):
                start_idx = best_path[i]
                end_idx = best_path[i + 1]
                if start_idx < len(nodes) and end_idx < len(nodes):
                    line = create_line(
                        nodes[start_idx][0], nodes[start_idx][1],
                        nodes[end_idx][0], nodes[end_idx][1],
                        "red",
                        3
                    )
                    shapes.append(line)
        
        # dessin des noeuds 

        for i, (x, y) in enumerate(nodes):
            shapes.append(
                ft.Container(
                    width=20,
                    height=20,
                    bgcolor="green",
                    border_radius=10,
                    left=x-10,
                    top=y-10,
                    content=ft.Text(str(i), size=10, color="white"),
                    alignment=ft.alignment.Alignment(0, 0)
                )
            )
        
        graph_container.content = ft.Stack(controls=shapes, width=600, height=500) #on superpose tous les éléments créés dans notre page d'affichage
        page.update()