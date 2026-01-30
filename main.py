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
    
    # Contrôles UI - Paramètres d'entrée
    nodes_field = ft.TextField(label="Nombre de nœuds", value="10", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="30", width=150)
    best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
    iterations_field = ft.TextField(label="Itérations", value="200", width=150)
    decay_field = ft.TextField(label="Décay", value="0.95", width=150)
    alpha_field = ft.TextField(label="Alpha", value="1", width=150)
    beta_field = ft.TextField(label="Beta", value="2", width=150)