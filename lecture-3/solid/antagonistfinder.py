from places import Kostroma, Tokyo
from abc import abstractmethod


class Place():
    @abstractmethod
    def get_antagonist(self):
        pass


class AntagonistFinder(Place):

    def get_antagonist(self, place):
        if isinstance(place, Kostroma):
            place.get_orcs()
        elif isinstance(place, Tokyo):
            place.get_godzilla()
