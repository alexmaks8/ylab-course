import time


def options(call_count: int,
            start_sleep_time: int,
            factor: int,
            border_sleep_time: int):

    def decorator(func):

        def wrapper():
            print(f'Количество запросов = {call_count}\nНачало работы')
            t = start_sleep_time
            count = 0
            for n in range(0, call_count):
                
                if t < border_sleep_time:
                    t = start_sleep_time * factor ** n
                if t > border_sleep_time:
                    t = border_sleep_time
                    
                time.sleep(t)
                count += 1
                print(f'Запуск номер {count}. Ожидание: {t} секунд. '
                      f'Результат декорируемой функций = {func()}.')
            print('Конец работы')

            return

        return wrapper

    return decorator


@options(call_count=5, start_sleep_time=1, factor=2, border_sleep_time=20)
def func_result():
    return 'ok'


if __name__ == '__main__':
    func_result()
