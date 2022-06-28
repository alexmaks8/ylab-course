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

