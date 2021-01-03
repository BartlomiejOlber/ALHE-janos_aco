from src.model.city import City
from src.model.network import Network


def load_data():
    import xml.etree.ElementTree as ET
    root = ET.parse('data/janos-us--D-D-M-N-S-A-N-S/janos-us.xml').getroot()
    prefix = "{http://sndlib.zib.de/network}"
    city_name = "Seattle"
    city_list = []
    adjacency_dict = dict()
    for type_tag in root.findall(f"{prefix}networkStructure/{prefix}links/{prefix}link"):
        source = type_tag.find(f"{prefix}source").text
        target = type_tag.find(f"{prefix}target").text
        cost = type_tag.find(f"{prefix}additionalModules/{prefix}addModule/{prefix}cost").text
        if source != city_name:
            city_list.append(City(city_name, adjacency_dict))
            adjacency_dict = dict()
            city_name = source
        adjacency_dict[target] = cost
    city_list.append(City(city_name, adjacency_dict))
    return Network(city_list)


if __name__ == '__main__':
    network = load_data()
    print(network.graph["Seattle"])
    print(network.graph["SanFrancisco"])
