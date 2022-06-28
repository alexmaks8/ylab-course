from itertools import combinations

def bananas(s):
    result = set()
    word = 'banana'
    for comb in combinations(enumerate(s), 6):
        dash = ['-' for _ in range(len(s))]
        count = 0
        for i, k in comb:
            if k == word[count]:
                dash[i] = k
                count += 1
        if count == len(word):
            result.add(''.join(dash))
    return result


if __name__ == '__main__':
    assert bananas("banann") == set()
    assert bananas("banana") == {"banana"}
    assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                        "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                        "-ban--ana", "b-anana--"}
    assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
    assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}

