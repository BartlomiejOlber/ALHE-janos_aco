from copy import deepcopy


class Network(object):
    def __init__(self, city_list):
        self.graph = dict()
        for city in city_list:
            self.graph[city.get_id()] = city.get_adjacency_dict()
        self._dfs_best_distance = float("inf")
        self._dfs_best_path = None

    def _dfs_next_node(self, curr_node, finish_node, path, path_length, visited):
        if path_length > self._dfs_best_distance:
            return

        if curr_node == finish_node:
            if path_length < self._dfs_best_distance:
                self._dfs_best_distance = path_length
                self._dfs_best_path = deepcopy(path)
            return

        for neighbour in self.graph[curr_node]:
            if neighbour not in visited:
                path_length += float(self.graph[curr_node][neighbour])
                path.append(neighbour)
                visited.add(neighbour)
                self._dfs_next_node(neighbour, finish_node, path, path_length, visited)
                visited.remove(neighbour)
                path.pop()
                path_length -= float(self.graph[curr_node][neighbour])

    def dfs_solve(self, start, finish):
        visited = set()
        visited.add(start)
        path = [start]
        self._dfs_next_node(start, finish, path, 0., visited)
        return self._dfs_best_distance, self._dfs_best_path
