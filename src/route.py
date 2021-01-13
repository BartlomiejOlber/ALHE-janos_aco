
class Route(object):

    def __init__(self, cities):
        self.__length = 0.0
        self.__cities = cities

    def __lt__(self, other):
        return self.get_length() < other.get_length()

    def __gt__(self, other):
        return self.get_length() > other.get_length()

    def __len__(self):
        return len(self.__cities)

    def __getitem__(self, index: int):
        return self.__cities[index]

    def __setitem__(self, index: int, value):
        self.__cities[index] = value

    def add_city(self, city, distance_added):
        self.__cities.append(city)
        self.__length += distance_added

    def get_last_city(self):
        return self.__cities[-1]

    def get_length(self) -> float:
        return self.__length

