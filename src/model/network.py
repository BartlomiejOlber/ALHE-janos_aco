from copy import deepcopy


class Network(object):
    def __init__(self, city_list):
        self.graph = dict()
        for city in city_list:
            self.graph[city.get_id()] = city.get_adjacency_dict()
        self._dfs_best_distances = []
        self._dfs_paths = []
        self._dfs_best_path = None

    def _dfs_next_node(self, curr_node, finish_node, path, path_length, visited):

        if curr_node == finish_node:
            self._dfs_best_distances.append(deepcopy(path_length))
            self._dfs_best_path = deepcopy(path)
            self._dfs_paths.append(self._dfs_best_path)
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

    def dfs_solve(self, start, finish, n_routes=1):
        visited = set()
        visited.add(start)
        path = [start]
        self._dfs_next_node(start, finish, path, 0., visited)
        top_n_ids = sorted(range(len(self._dfs_best_distances)), key=lambda i: self._dfs_best_distances[i])[:n_routes]
        top_n_distances = []
        top_n_paths = []
        for index in top_n_ids:
            top_n_distances.append(self._dfs_best_distances[index])
            top_n_paths.append(self._dfs_paths[index])
        return top_n_distances, top_n_paths
