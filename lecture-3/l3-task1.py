
def my_cache(func):

    cache = dict()

    def wrapper(*args):
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


