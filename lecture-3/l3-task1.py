
def my_cache(func):
    '''
    Функция my_cache внутри себя определяет функцию wrapper.
    + создаем словарь для хранения кэша.
    '''
    cache = dict()

    def wrapper(*args):
        '''Функция wrapper проверяет наличие данных в кэше.'''
        result = func(*args)
        if args in cache:
            return cache[args]
        else:
            cache[args] = result
            return result

    return wrapper


@my_cache
def multiplier(number: int):
    return number * 2


if __name__ == '__main__':
    print(multiplier(3))
    print(multiplier(3))
    print(multiplier(5))
    print(multiplier(5))


