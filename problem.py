

class Problem2D:

    def __init__(self, nodes: list, distances: np.ndarray, pheromones):
        self.nodes = nodes
        self.distances = distances
        self.pheromones = pheromones