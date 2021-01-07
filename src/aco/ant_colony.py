import datetime
import time

import numpy as np
from tqdm import tqdm

from src.model.route import Route


class AntColonyOptimizer:
    UNLINKED_COST = 10000.

    def __init__(self, n_ants, rho, pheromone_unit, best_route_p, elitist_weight, distance_preference_factor):
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
        self._distance_preference_factor = distance_preference_factor
        self._paths = dict()
        self._nth_best = float("inf")

    def _initialize(self):
        num_cities = len(self._map.graph)
        self._pheromones = np.zeros((num_cities, num_cities)) + 0.0001
        self._distance_weights = np.zeros((num_cities, num_cities)) + 0.0001
        for city, links in self._map.graph.items():
            for link in links:
                self._pheromones[city, link] = 1
                self._distance_weights[city, link] = self._distance_preference_factor / float(
                    self._map.graph[city][link])

        self._route_probability = self._pheromones * self._distance_weights / (self._pheromones * self._distance_weights).sum()
        self._unvisited_cities = list(range(num_cities))

    def _update_probabilities(self):
        self._route_probability = self._pheromones * self._distance_weights / (
                self._pheromones * self._distance_weights).sum()
        # self._route_probability = self._pheromones * self._distance_weights
        # print(f"sum: {self._route_probability.sum()}")

    def _choose_next_city(self, from_city):
        possible_routes = self._route_probability[from_city, self._unvisited_cities]
        next_city = np.random.choice(range(len(possible_routes)), p=possible_routes/possible_routes.sum())
        # print(possible_routes)
        # possible_routes = self._route_probability[from_city, self._unvisited_cities]
        # if np.random.random() < self._best_route_p:
        #     next_city = np.argmax(possible_routes)
        # else:
        #     uniform_probabilities = possible_routes / np.sum(possible_routes)
        #     next_city = np.random.choice(range(len(possible_routes)), p=uniform_probabilities)
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
        return float(self._map.graph[city][another]) if another in self._map.graph[
            city] else AntColonyOptimizer.UNLINKED_COST

    def fit(self, map_matrix, start, finish, iterations=100, n_paths=3):
        self._map = map_matrix
        self._initialize()

        a = datetime.datetime.now()
        for i in range(iterations):
            paths = []
            for ant in range(self._n_ants):
                current_city = self._unvisited_cities[start]
                route = Route([current_city])
                while current_city != finish and len(
                        self._unvisited_cities) > 1 and route.get_length() < self._nth_best:
                    self._unvisited_cities.remove(current_city)
                    current_node_index = self._choose_next_city(current_city)
                    current_city = self._unvisited_cities[current_node_index]
                    route.add_city(current_city, self._get_distance(route.get_last_city(), current_city))
                paths.append(route)
                self._add_pheromone(route, route.get_length(), 1)
                self._unvisited_cities = list(range(len(self._map.graph)))
                self._paths[route.get_length()] = route
            best_path, min_length = self._evaluate(paths)
            self._nth_best = sorted(self._paths.keys())[n_paths - 1]
            # print(min_length)

            if min_length < self._alltime_min:
                self._alltime_min = min_length
                self._best_path = best_path

            self._update(self._best_path, self._elitist_weight)

        b = datetime.datetime.now()
        delta = b - a
        print(f" aco: {int(delta.total_seconds() * 1000)} ms")
        best_n_distances = []
        best_n_paths = []
        distances_sorted = sorted(self._paths.keys())
        if len(distances_sorted) < n_paths:
            n_paths = len(distances_sorted)
        for i in range(n_paths):
            key = distances_sorted[i]
            best_n_distances.append(key)
            best_n_paths.append(self._paths[key])
        return best_n_distances, best_n_paths
