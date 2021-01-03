class Network(object):
    def __init__(self, city_list):
        self.graph = dict()
        for city in city_list:
            self.graph[city.get_name()] = city.get_adjacency_dict()