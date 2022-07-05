import random
import copy
from itertools import count as count_from


def diagonal_chek(field: list, character: str, length: int, ver: int, hor: int) -> bool:
    # проверка по диагонали
    left_c, right_c = 0, 0

    for i in range(length):
        if field[i + ver][i+hor] == character:
            right_c += 1
        if field[i + ver][length - i - 1 + hor] == character:
            left_c += 1

    if left_c == length or right_c == length:
        return True

    return False


def horizontal_chek(field: list, character: str, length: int, ver: int, hor: int) -> bool:
    # проверка по горизонтали
    for i in range(length):
        count = 0
        for j in range(length):
            if field[ver+i][hor+j] == character:
                count += 1

        if count == length:
            return True

    return False


def vertical_chek(field: list, character: str, length: int, ver: int, hor: int) -> bool:
    # проверка по вертикали
    for i in range(length):
        count = 0
        for j in range(length):
            if field[hor+j][ver+i] == character:
                count += 1
        if count == length:
            return True

    return False


def check_lose(field: list, character: str, lose_length: int, ver: int, hor: int) -> bool:
    # проверка по всем направлениям
    for i in range(0, ver - lose_length + 1):
        for j in range(0, hor - lose_length + 1):
            if diagonal_chek(field, character, lose_length, i, j) or \
                horizontal_chek(field, character, lose_length, i, j) or \
                vertical_chek(field, character, lose_length, i, j):
               return True

    return False


def computer(field: list, computer_symbol: str, lose_length: int) -> bool:
    # ход компьютера
    control = available_position(field)
    random.shuffle(control)
    for spot in control:
        copy_field = copy.deepcopy(field)
        copy_field[spot[0]][spot[1]] = computer_symbol
        if check_lose(copy_field, computer_symbol, lose_length, len(field), len(field)) == False:
            field[spot[0]][spot[1]] = computer_symbol
            return True
    
    return False


def player(field: list, player_symbol: str, lose_length: int, point_dict: dict) -> bool:
    # ход игрока
    player_point = None

    while True:
        player_input = input('Введите число: ')
        player_point = point_dict.get(player_input, None)

        if not player_point:
            print('Такой позиции нет на поле, введите число заново: ')
            continue

        if field[player_point[0]][player_point[1]] in  {'X', 'O'}:
            print('Позиция уже занята, введите число заново: ')
        else:
            break
    
    field[player_point[0]][player_point[1]] = player_symbol

    if check_lose(field, player_symbol, lose_length, len(field), len(field)):
        return False
    
    return True


def new_field(ver: int = 10, hor: int = 10) -> tuple:
    # создаем новое поле
    count = count_from(1)
    field, point_dict = [], {}

    for i in range(ver):
        field.append([])
        for j in range(hor):
            number = str(next(count))
            field[i].append(number)
            point_dict[number] = (i, j)

    return field, point_dict


def chose_your_symbol() -> tuple:
    # игрок выбирает символ
    user_symbol = ''
    while True:
        user_symbol = input('Вы будете играть за X или O? ').upper()
        
        if user_symbol in {'X', 'O'}:
            break
        else:
            print('Вам доступны только X или O, ведите заново:')

    computer_symbol = 'O' if user_symbol == 'X' else 'X'
    return user_symbol, computer_symbol


def choose_first_player(user_symbol: str, computer_symbol: str) -> str:
    # определяем ход случайнымобразом
    symbols = [user_symbol, computer_symbol]
    first_player = symbols[random.choice((0, 1))]
    print(f'В этот раз первым ходит игрок {first_player}')

    return first_player


def available_position(field: list) -> list:
    # анализ доступных позиций
    control = []

    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] not in {'O', 'X'}:
                control.append((i, j))

    return control


def check_draw(field: list) -> bool:
    # проверка на ничью
    if len(available_position(field)) == 0:
        return True
    
    return False


def game_move(field: list, user_symbol: str, computer_symbol: str, lose_length: str, point_dict: dict) -> bool:
    # анализ игры (ход игрока и компьютера)
    darw_result = check_draw(field)

    if darw_result:
        print('Ничья.')
        return False

    user_move = player(field, user_symbol, lose_length, point_dict)

    if not user_move:
        print('Вы проиграли!')
        return False

    darw_result = check_draw(field)

    if darw_result:
        print('Ничья!')
        return False

    cpm_point = computer(field, computer_symbol, lose_length)

    if not cpm_point:
        print('Компьютер проиграл')
        return False

    return True


def print_field(field: list) -> None:
    # выводим поле
    result = ''
    for row in field:
        result += '|' + ('-' * (len(row) * 7 - 1)) + '|\n'
        for cell in row:
            result += '|  ' +  cell + (' ' * (4 - len(cell)))
        result += '|\n'
    
    result += '|' + ('-' * (len(row) * 7 - 1)) + '|\n'

    print(result)


def main():
    # запускаем игру
    lose_length = 5
    ver_size = 10
    hor_size = 10

    while True:
        print('Обратные крестики-нолики!')

        # игрок выбирает символ: X или O
        user_symbol, computer_symbol = chose_your_symbol()

        # Определяем ход случайным образом
        first_player = choose_first_player(user_symbol, computer_symbol)

        # создаем новое поле
        field, point_dict = new_field(ver=ver_size, hor=hor_size,
        )

        if first_player == computer_symbol:
            computer(field, computer_symbol, lose_length)
        
        print_field(field)

        while game_move(field, user_symbol, computer_symbol, lose_length, point_dict):
            print_field(field)
        
        while True:
            user_symbol = input('Сыграть ещё раз? (Y/N): ').upper()

            if user_symbol in {'Y', 'N'}:
                break
            else:
                print('Некорректный ответ на вопрос')
        
        if user_symbol == 'N':
            break


if __name__ == '__main__':
    main()