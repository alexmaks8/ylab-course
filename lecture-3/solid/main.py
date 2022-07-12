from typing import Union
from heroes import Superman, SuperHero, Media, ChackNorris
from places import Kostroma, Tokyo


def save_the_place(hero: SuperHero, place: Union[Kostroma, Tokyo], media: Media):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    media.create_news(place, hero)


if __name__ == '__main__':
    save_the_place(Superman(), Kostroma(), Media())
    print('-' * 20)
    save_the_place(ChackNorris(), Tokyo(), Media())
