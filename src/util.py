from src.city import City
from src.network import Network
import argparse


def parse_args() -> vars:
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', "--rho", default=0.13, type=float, help="Value of Rho evaporation rate")
    ap.add_argument('-a', "--ants", default=15, type=int, help="number of ants working")
    ap.add_argument('-p', '--pheromone', default=200, type=int, help="Number of pheromones left by each ant")
    ap.add_argument('-e', '--elitist', default=4.6, type=float, help='improvement of best path yet')
    ap.add_argument('-s', '--starting', type=str, default="Seattle", help="starting city")
    ap.add_argument('-f', '--finishing', type=str, default='Miami', help="finishing city")
    ap.add_argument('-i', '--iterations', default=15, type=int, help='Number of iterations')
    ap.add_argument('-n', '--npaths', default=3, type=int, help="number of paths to be found")
    args = vars(ap.parse_args())
    return args


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
