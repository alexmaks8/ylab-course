'''Здесь собираются местоположения совершаемых злодеяний.'''

from abc import ABC, abstractmethod


class Place(ABC):
    '''Класс Place с обязательным методом для настледуемых классов.'''
    @abstractmethod
    def get_location(self):
        pass


class Kostroma(Place):
    name = 'Kostroma'

    def get_orcs(self):
        print('Orcs hid in the forest')

    def get_location(self):
        self.get_orcs()


class Tokyo(Place):
    name = 'Tokyo'

    def get_godzilla(self):
        print('Godzilla stands near a skyscraper')

    def get_location(self):
        self.get_godzilla()
