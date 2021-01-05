import time

import numpy as np
from tqdm import tqdm

from src.model.route import Route


class AntColonyOptimizer:

    UNLINKED_COST = 10000.

    def __init__(self, n_ants, rho, pheromone_unit, best_route_p=.1, elitist_weight=10):
        self._n_ants = n_ants
        self._rho = rho
        self._pheromone_unit = pheromone_unit
        self._best_route_p = best_route_p
        self._pheromones = None
        self._distance_weights = None
        self._route_probability = None
        self._map = None
        self._unvisited_cities = None
        self._best_path = None
        self._alltime_min = float("inf")
        self._elitist_weight = elitist_weight

    def _initialize(self):
        num_cities = len(self._map.graph)
        self._pheromones = np.zeros((num_cities, num_cities)) + 0.0001
        self._distance_weights = np.zeros((num_cities, num_cities)) + 0.0001
        for city, links in self._map.graph.items():
            for link in links:
                self._pheromones[city, link] = 1
                self._distance_weights[city, link] = 100 / float(self._map.graph[city][link])

        self._route_probability = self._pheromones * self._distance_weights
        self._unvisited_cities = list(range(num_cities))

    def _update_probabilities(self):
        self._route_probability = self._pheromones * self._distance_weights
        print(f"sum: {self._route_probability.sum()}")

    def _choose_next_city(self, from_city):
        possible_routes = self._route_probability[from_city, self._unvisited_cities]
        if np.random.random() < self._best_route_p:
            next_city = np.argmax(possible_routes)
        else:
            uniform_probabilities = possible_routes / np.sum(possible_routes)
            next_city = np.random.choice(range(len(possible_routes)), p=uniform_probabilities)
        return next_city

    @staticmethod
    def _evaluate(paths):
        min_length = float("inf")
        for path in paths:
            path_length = path.get_length()
            if path_length < min_length:
                min_length = path_length
                best_path = path
        # print(f"bestid: {best}  pathsnum: {len(paths)}  bestscore: {scores[best]} best path: {paths[best]}")
        return best_path, min_length

    def _update(self, best_path, weight):
        self._pheromones *= (1 - self._rho)
        self._add_pheromone(best_path, best_path.get_length(), weight)
        self._update_probabilities()

    def _add_pheromone(self, path, distance, weight):
        pheromone_to_add = self._pheromone_unit / distance * weight
        for i in range(len(path) - 1):
            self._pheromones[path[i], path[i + 1]] += pheromone_to_add

    def _get_distance(self, city, another):
        return float(self._map.graph[city][another]) if another in self._map.graph[city] else AntColonyOptimizer.UNLINKED_COST

    def fit(self, map_matrix, start, finish, iterations=100, early_finish_condition=40):
        self._map = map_matrix
        self._initialize()
        num_equal = 0
        previous_length = 0.
        find_cycle = False
        if start == finish:
            find_cycle = True

        # for i in tqdm(range(iterations)):
        for i in range(iterations):
            paths = []
            for ant in range(self._n_ants):
                current_city = self._unvisited_cities[
                    start if not find_cycle else np.random.randint(0, len(self._unvisited_cities))]
                start_city = current_city
                route = Route([current_city])
                while (find_cycle or current_city != finish) and len(self._unvisited_cities) > 1:
                    self._unvisited_cities.remove(current_city)
                    current_node_index = self._choose_next_city(current_city)
                    current_city = self._unvisited_cities[current_node_index]
                    route.add_city(current_city, self._get_distance(route.get_last_city(), current_city))
                if find_cycle:
                    route.add_city(start_city, self._get_distance(route.get_last_city(), start_city))
                paths.append(route)
                self._add_pheromone(route, route.get_length(), 1)
                self._unvisited_cities = list(range(len(self._map.graph)))

            best_path, min_length = self._evaluate(paths)
            print(min_length)
            if min_length == previous_length:
                num_equal += 1
            else:
                num_equal = 0

            if num_equal == early_finish_condition:
                break
            if min_length < self._alltime_min:
                self._alltime_min = min_length
                self._best_path = best_path

            previous_length = min_length
            self._update(self._best_path, self._elitist_weight)
        return self._best_path
