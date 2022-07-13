from places import Place


class AntagonistFinder:
    '''
    Класс AntagonistFinder запрашивает злодея с конкретной локацией.
    '''
    @staticmethod
    def get_antagonist(place: Place):
        place.get_location()
