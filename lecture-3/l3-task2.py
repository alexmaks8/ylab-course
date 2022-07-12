import time


def options(call_count: int,
            start_sleep_time: int,
            factor: int,
            border_sleep_time: int):

    def decorator(func):

        def wrapper(*args, **kwargs):
            print(f'Количество запросов = {call_count}\nНачало работы')
            t = start_sleep_time
            for n in range(1, call_count + 1):
                if t < border_sleep_time:
                    time.sleep(t)
                else:
                    t = border_sleep_time
                    time.sleep(t)
                
                func_result = func(*args, **kwargs)
                t *= 2 ** factor
                print(f'Запуск номер {n}. Ожидание: {t} секунд. '
                      f'Результат декорируемой функций = {func_result}.')

            print('Конец работы') 
            return 

        return wrapper

    return decorator


@options(call_count=3, start_sleep_time=2, factor=2, border_sleep_time=10)
def check():
    return 'ok'


if __name__ == '__main__':
    check()
