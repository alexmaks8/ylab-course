from antagonistfinder import AntagonistFinder


class SuperHero:

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)
        self.place = place

    def attack(self):
        pass

    def ultimate(self):
        pass


class Attacks:
    def roundhouse_kick(self):
        print('Bump')

    def incinerate_with_lasers(self):
        print('Wzzzuuuup!')

    def fire_a_gun(self):
        print('PIU PIU')


class Superman(SuperHero, Attacks):

    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)

    def ultimate(self):
        self.incinerate_with_lasers()


class ChackNorris(SuperHero, Attacks):

    def __init__(self):
        super(ChackNorris, self).__init__('Chack Norris', False)

    def attack(self):
        self.fire_a_gun()



class Media:
    @staticmethod
    def create_news(place, hero):
        place_name = getattr(place, 'name', 'place')
        hero_name = getattr(hero, 'name', 'hero')
        print(f'TV: {hero_name}, saved the {place_name}!')
