'''Здесь создаем новости'''

from heroes import SuperHero
from places import Place


class Media:
    @staticmethod
    def create_news(place: Place, hero: SuperHero):
        place_name = getattr(place, 'name', 'place')
        hero_name = getattr(hero, 'name', 'hero')
        print(f'TV: {hero_name}, saved the {place_name}!')
