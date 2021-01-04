from src.aco.ant_colony import AntColonyOptimizer
from src.model.city import City
from src.model.network import Network

import numpy as np


def load_data():
    import xml.etree.ElementTree as ET
    root = ET.parse('data/janos-us--D-D-M-N-S-A-N-S/janos-us.xml').getroot()
    prefix = "{http://sndlib.zib.de/network}"
    city_name = ""
    city_list = []
    index_to_name = dict()
    adjacency_dict = dict()
    index = 0
    for type_tag in root.findall(f"{prefix}networkStructure/{prefix}links/{prefix}link"):
        source = type_tag.find(f"{prefix}source").text
        if source != city_name:
            index_to_name[index] = source
            city_name = source
            index += 1

    city_name = "Seattle"
    index = 0
    for type_tag in root.findall(f"{prefix}networkStructure/{prefix}links/{prefix}link"):
        source = type_tag.find(f"{prefix}source").text
        target = type_tag.find(f"{prefix}target").text
        cost = type_tag.find(f"{prefix}additionalModules/{prefix}addModule/{prefix}cost").text
        if source != city_name:
            city_list.append(City(index, city_name, adjacency_dict))
            adjacency_dict = dict()
            index += 1
            city_name = source
        adjacency_dict[next(key for key, value in index_to_name.items() if value == target)] = cost
    city_list.append(City(index, city_name, adjacency_dict))
    return Network(city_list), index_to_name


def run(start_city, finish_city):
    problem, index_to_name = load_data()
    optimizer = AntColonyOptimizer(n_ants=60, rho=.04, pheromone_unit=.1, alpha=1, beta=1, elitist_factor=0.4)

    start = next(key for key, value in index_to_name.items() if value == start_city)
    finish = next(key for key, value in index_to_name.items() if value == finish_city)
    best = optimizer.fit(problem, start, finish, iterations=300, early_stopping_count=50)
    for city in best:
        print(index_to_name[city])


if __name__ == '__main__':
    network, id_to_name = load_data()
    # print(network.graph[0])
    # print(network.graph[1])
    # print(network.graph[2])
    # print(len(network.graph))
    # print(network.graph)
    print(id_to_name)
    num_nodes = len(network.graph)
    pheromone_matrix = np.zeros((num_nodes, num_nodes))
    heuristic_matrix = np.zeros((num_nodes, num_nodes))
    # Remove the diagonal since there is no pheromone from node i to itself
    for node, links in network.graph.items():
        for link in links:
            pheromone_matrix[node, link] = 1
            heuristic_matrix[node, link] = 100 / float(network.graph[node][link])
    # print(pheromone_matrix)
    # print(heuristic_matrix)
    run("LosAngeles", "Boston")
    # print(network.graph)
