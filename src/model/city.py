
class City(object):

    def __init__(self, id: int, name: str, adjacency_list: dict):
        self.__name = name
        self._id = id
        self.__adjacency_list = adjacency_list

    def __str__(self):
        return self.__name

    def __eq__(self, other):
        return self.__name == other.get_name()

    def __hash__(self):
        return hash(self.__name)

    def get_name(self):
        return self.__name

    def get_id(self):
        return self._id

    def get_adjacency_dict(self):
        return self.__adjacency_list

    def get_distance_from(self, another_city):
        return self.__adjacency_list[another_city]