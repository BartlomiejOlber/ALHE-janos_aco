import time

import numpy as np
from tqdm import tqdm


class AntColonyOptimizer:
    def __init__(self, n_ants, rho, pheromone_unit, elitist_factor=.1):
        self._n_ants = n_ants
        self._rho = rho
        self._pheromone_unit = pheromone_unit
        self._elitist_factor = elitist_factor
        self._pheromones = None
        self._distance_weights = None
        self._route_probability = None
        self._map = None
        self._unvisited_cities = None
        self._best_path = None
        self._alltime_min = float("inf")

    def _initialize(self):
        num_nodes = len(self._map.graph)
        self._pheromones = np.zeros((num_nodes, num_nodes)) + 0.0001
        self._distance_weights = np.zeros((num_nodes, num_nodes)) + 0.0001
        for node, links in self._map.graph.items():
            for link in links:
                self._pheromones[node, link] = 1
                self._distance_weights[node, link] = 100 / float(self._map.graph[node][link])

        self._route_probability = self._pheromones * self._distance_weights
        self._unvisited_cities = list(range(num_nodes))

    def _update_probabilities(self):
        self._route_probability = self._pheromones * self._distance_weights
        print(f"sum: {self._route_probability.sum()}")

    def _choose_next_node(self, from_node):
        possible_routes = self._route_probability[from_node, self._unvisited_cities]
        if np.random.random() < self._elitist_factor:
            next_node = np.argmax(possible_routes)
        else:
            uniform_probabilities = possible_routes / np.sum(possible_routes)
            next_node = np.random.choice(range(len(possible_routes)), p=uniform_probabilities)
        return next_node

    def _evaluate(self, paths):
        scores = np.zeros(len(paths))
        for index, path in enumerate(paths):
            for i in range(len(path) - 1):
                if path[i + 1] in self._map.graph[path[i]]:
                    score += float(self._map.graph[path[i]][path[i + 1]])
                else:
                    score += 10000.
            scores[index] = score
            best = np.argmin(scores)
        # print(f"bestid: {best}  pathsnum: {len(paths)}  bestscore: {scores[best]} best path: {paths[best]}")
        return paths[best], scores[best]

    def _update(self, best_path):
        self._pheromones *= (1 - self._rho)
        self._add_pheromone(best_path, best_length)
        self._update_probabilities()

    def _add_pheromone(self, path, distance):
        pheromone_to_add = self._pheromone_unit / distance
        for i in range(len(path) - 1):
            self._pheromones[path[i], path[i + 1]] += pheromone_to_add

    def fit(self, map_matrix, start_city, finish_city, iterations=100):
        self._map = map_matrix
        self._initialize()
        num_equal = 0
        find_cycle = False
        if start_city == finish_city:
            find_cycle = True

        for i in tqdm(range(iterations)):
            paths = []
            for ant in range(self._n_ants):
                current_node = self._unvisited_cities[
                    start_city if not find_cycle else np.random.randint(0, len(self._unvisited_cities))]
                start_node = current_node
                path = [current_node]
                while (find_cycle or current_node != finish_city) and len(self._unvisited_cities) > 1:
                    self._unvisited_cities.remove(current_node)
                    current_node_index = self._choose_next_node(current_node)
                    print(f"curr node: {current_node}, curr id: {current_node_index}")
                    current_node = self._unvisited_cities[current_node_index]
                    path.append(current_node)
                if find_cycle:
                    path.append(start_node)  # go back to start
                paths.append(path)
                self._add_pheromone(path, path_length)
                self._unvisited_cities = list(range(len(self._map.graph)))

            best_path, min_length = self._evaluate(paths)
            if min_length == self._alltime_min:
                num_equal += 1
            else:
                num_equal = 0

            if min_length <= alltime_min:
                alltime_min = min_length
                self._best_path = best_path

            self._update(best_path)

        self.best = min(self.best_series)
        return self._best_path
