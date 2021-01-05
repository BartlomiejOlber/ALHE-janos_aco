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


def run_aco(start_city, finish_city):
    problem, index_to_name = load_data()
    optimizer = AntColonyOptimizer(n_ants=30, rho=.2, pheromone_unit=400, best_route_p=0.2, elitist_weight=5)

    start = next(key for key, value in index_to_name.items() if value == start_city)
    finish = next(key for key, value in index_to_name.items() if value == finish_city)
    best = optimizer.fit(problem, start, finish, iterations=20, early_finish_condition=10)
    for city in best:
        print(index_to_name[city])
    print(best.get_length())


def run_dfs(start_city, finish_city):
    network, index_to_name = load_data()
    start = next(key for key, value in index_to_name.items() if value == start_city)
    finish = next(key for key, value in index_to_name.items() if value == finish_city)
    best_distance, best_path = network.dfs_solve(start, finish)
    for city in best_path:
        print(index_to_name[city])
    print(best_distance)


if __name__ == '__main__':

    run_dfs("StLouis", "Seattle")
    run_aco("StLouis", "Seattle")
    # print(network.graph)
