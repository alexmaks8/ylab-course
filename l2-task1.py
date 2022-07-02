import itertools
import math

# Вычисляем расстояние между вершинами
def distance(a, b):
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

# Вычесляем общее количество маршрутов
def all_routes(all_route):
    all_route = itertools.permutations(points[1:])
    return all_route

#  Вычесляем кратчайший маршрут
def best_routes(routs, start):
    min_dist = math.inf
    the_dist = []
    for way in all_routes(routs):
        base = start
        output = str(start)
        count = 0
        for point in way:
            count += distance(base, point)
            output += f" -> {str(point)}[{str(count)}]"
            base = point
        count += distance(base, start)
        output += f" -> {str(start)}[{str(count)}]"
        if count < min_dist:
            min_dist = count
            the_dist = output

    return f"{the_dist} = {str(min_dist)}"


point_1 = (0, 2) #Почтовое отделение
point_2 = (2, 5) #Ул. Грибоедова, 104/25
point_3 = (5, 2) #Ул. Бейкер стрит, 221б
point_4 = (6, 6) #Ул. Большая Садовая, 302-бис
point_5 = (8, 3) #Вечнозелёная Аллея, 742

points = [point_1, point_2, point_3, point_4, point_5] 


if __name__ == '__main__':
    print(best_routes([point_2, point_3, point_4, point_5], point_1))