def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def way_dist(points):
    count = 0

    for i in range(len(points) - 1):
        count += distance(*points[i], *points[i + 1])
    return count


def full_way(points):
    count = 0
    dist1 = []

    for i in range(len(points) - 1):
        count += distance(*points[i], *points[i + 1])
        dist1.append(count)

    print(f"{points[0]} -> {points[1]}[{dist1[0]}] -> {points[2]}[{dist1[1]}] -> {points[3]}[{dist1[2]}] -> {points[4]}[{dist1[3]}] -> {points[5]}[{dist1[4]}] = {dist1[4]}")


def best_way(start, points):
    listW = []
    distW = -1
    for i in range(0, 4):
        d_count = points[:i] + points[i + 1:]
        for d in range(len(d_count)):
            k_count = d_count[:d] + d_count[d + 1:]
            for k in range(len(k_count)):
                for_listW = [start, points[i], d_count[d], k_count[k], k_count[1 - k], start]
                for_distW = way_dist(for_listW)
                if distW == -1 or for_distW < distW:
                    listW = for_listW[:]
                    distW = for_distW
    full_way(listW)


point_1 = (0, 2) #Почтовое отделение
point_2 = (2, 5) #Грибоедова
point_3 = (5, 2) #Бейкер-стрит
point_4 = (6, 6) #Большая Садовая
point_5 = (8, 3) #Вечнозеленая Аллея

best_way(point_1, [point_2, point_3, point_4, point_5])
