'''
Задача №5. Секция статьи "Задача №5."
Написать метод count_find_num, который принимает на вход список простых множителей (primesL) и целое число,
предел (limit), после чего попробуйте сгенерировать по порядку все числа.
Меньшие значения предела, которые имеют все и только простые множители простых чисел primesL.

primesL = [2, 5, 7]
limit = 500
List of Numbers Under 500          Prime Factorization
___________________________________________________________
           70                         [2, 5, 7]
          140                         [2, 2, 5, 7]
          280                         [2, 2, 2, 5, 7]
          350                         [2, 5, 5, 7]
          490                         [2, 5, 7, 7]

Скопировать
5 из этих чисел меньше 500, а самое большое из них 490.

primesL = [2, 5, 7]
limit = 500
count_find_num(primesL, val) == [5, 490]
'''

def count_find_num(primesL, limit):
    primesL = sorted(primesL)
    count = 1
    for val in primesL:
        count *= val
    if count > limit:
        return []
    final_value = [count]
    for i in primesL:
        for val in final_value:
            num = val * i
            if (num <= limit) and (num not in final_value):
                final_value.append(num)
                num *= i

    return [len(final_value), max(final_value)]


if __name__ == '__main__':
	primesL = [2, 3]
	limit = 200
	assert count_find_num(primesL, limit) == [13, 192]

	primesL = [2, 5]
	limit = 200
	assert count_find_num(primesL, limit) == [8, 200]

	primesL = [2, 3, 5]
	limit = 500
	assert count_find_num(primesL, limit) == [12, 480]

	primesL = [2, 3, 5]
	limit = 1000
	assert count_find_num(primesL, limit) == [19, 960]

	primesL = [2, 3, 47]
	limit = 200
	assert count_find_num(primesL, limit) == []

