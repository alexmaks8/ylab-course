'''
Задача №3. Секция статьи "Задача №3."
Написать метод zeros, который принимает на вход целое число (integer) и
возвращает количество конечных нулей в факториале (N! = 1 * 2 * 3 * ... * N) заданного числа:

Будьте осторожны 1000! имеет 2568 цифр.

Доп. инфо: http://mathworld.wolfram.com/Factorial.html

Подсказка: вы не должны вычислять факториал.
Найдите другой способ найти количество нулей.
'''

import re

def zeros(n):
    factorial = 1
    for i in range(2, n+1):
        factorial *= i
    str1 = str(factorial)
    count = len(''.join(re.findall(r"[0]+$", str1)))
    return count


if __name__ == '__main__':
    assert zeros(0) == 0
    assert zeros(6) == 1
    assert zeros(30) == 7
