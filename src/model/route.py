from city import City

from typing import List
import random


class Route(object):

    def __init__(self, start_city, finish_city):
        self._start_city = start_city
        self._finish_city = finish_city
        self.__length = 0.0
        self.__cities = []

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

    def get_length(self) -> float:
        self.__length = 0.0
        prev_city = self.__cities[0]
        for city in self.__cities[1:]:
            self.__length += city.get_distance_from(prev_city.get_name())
            prev_city = city
        return self.__length
