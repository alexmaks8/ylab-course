from antagonistfinder import AntagonistFinder
from capabilities import Kick, Laser, Gun


class SuperHero:
    '''
    Родительский класс супергероя с функциями:
    * find - ищем антогониста
    * attack & ultimate - для назначения способности ведения боя.
    '''
    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)

    def attack(self):
        pass

    def ultimate(self):
        pass


class Superman(SuperHero, Laser, Kick):
    '''
    Класс Superman наследуется от супергероя и способностей.
    В данном случае супермен и дерется и пускает лазер.
    '''
    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)

    def attack(self):
        self.roundhouse_kick()

    def ultimate(self):
        self.incinerate_with_lasers()


class ChackNorris(SuperHero, Gun):
    '''
    Класс ChackNorris наследуется от супергероя и способностей.
    Виртуозно владеет пистолетом.
    '''
    def __init__(self):
        super(ChackNorris, self).__init__('Chack Norris', False)

    def attack(self):
        self.fire_a_gun()

