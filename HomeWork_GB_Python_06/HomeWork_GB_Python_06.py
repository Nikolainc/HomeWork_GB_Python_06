from http.client import CONTINUE
from random import randint
from time import sleep
import time

#========= НАСТРОЙКИ =========
# 0 - пустое поле, 1 - корабль, 5 - запрет размещения кораблей, 7 - выстрел без попадания, 9 - попадание 

_symbols_print_player = {0:"■",1:"▽",5:"■",7:"X",9:"☑"} # символы для поля игрок
_symbols_print_enemy = {0:"■",1:"■",5:"■",7:"X",9:"☑"} # символы для поля противник
_boat_size = {3:4, 2:3, 1:2, 0:1} # размеры кораблей
_boat_counts_on_map = {3:1, 2:2, 1:3, 0:4} # кол-во кораблей
_start_boat_variants = len(_boat_counts_on_map) - 1 # кол-во вариантов кораблей

def PrintMap(array, view = False): # Вывод карты. 2 атрибута. С видимыми кораблями и скрытыми
    if view:
        print("Y:    ", end="")
        for i in range(len(array)):
            print(f"{i}", end=" ")
        print("")
        print("     ", end=" ")
        for i in range(len(array)):
            print("-", end=" ")
        print("")
        for i in range(len(array)):
            print(f"X: {i}| ", end="")
            for j in range(len(array[i])):
                print(f"{_symbols_print_player.get(array[i][j])}", end = " ")
            print("")
    else:
        print("Y:    ", end="")
        for i in range(len(array)):
            print(f"{i}", end=" ")
        print("")
        print("     ", end=" ")
        for i in range(len(array)):
            print("-", end=" ")
        print("")
        for i in range(len(array)):
            print(f"X: {i}| ", end="")
            for j in range(len(array[i])):
                print(f"{_symbols_print_enemy.get(array[i][j])}", end = " ")
            print("")

def CountOfBoats(array): # подсчет оставшихся кораблей
    counter = 0
    for i in range(0,len(array)):
        for j in range(0, len(array)):
            if array[i][j] == 1:
                counter += 1
    return counter

def IsPositionBlock(array, Y, X, size, horizontal):
    if horizontal:
        for j in range(X - 1, X + size):
            if j < 0 or j > len(array) - 1:
                return False
            if array[Y][j] != 0:
                return False
    else:
        for i in range(Y - 1, Y + size):
            if i < 0 or i > len(array) - 1:
                return False
            if array[i][X] != 0:
                return False
    return True

def PositionOffset(array, value):
    if len(array) - 1 <= value:
        value = 0
        return value
    else:
        value += 1
        return value

def clearMap(array):
    array = [[0] * len(array) for i in range(len(array))]
    return array

def GetRandomBlockPositionForBoat(array, size, count = 100, horizontal = True, Y = -1, X = -1, result = True):
    random_start_Y = randint(0, len(array) - 1) if Y == -1 else Y
    random_start_X = randint(0, len(array) - 1) if X == -1 else X
    while count > 0:
        if IsPositionBlock(array, random_start_Y, random_start_X, size, horizontal):
            return random_start_Y, random_start_X, horizontal, result
        elif IsPositionBlock(array, random_start_Y, random_start_X, size, -horizontal):
            return random_start_Y, random_start_X, -horizontal, result
        else:
            random_start_Y = PositionOffset(array, random_start_Y)
            random_start_X = PositionOffset(array, random_start_X)
        count -= 1
    result = False
    random_start_Y = 0
    random_start_X = 0
    return random_start_Y, random_start_X, horizontal, result
    

def PlaceBoatOnMap(array, position, size):
    if position[2]:
        for i in range(position[0] - 1, position[0] + 2):
            for j in range(position[1] - 1, position[1] + size + 1):
                if i < 0 or i > len(array) - 1 or j < 0 or j > len(array) - 1:
                    continue
                if array[i][j] == 0:
                    array[i][j] = 5

        for j in range(position[1], position[1] + size):
            if j < 0 or j > len(array) - 1:
                continue
            array[position[0]][j] = 1

    else:
        for i in range(position[0] - 1, position[0] + size + 1):
            for j in range(position[1] - 1, position[1] + 2):
                if i < 0 or i > len(array) - 1 or j < 0 or j > len(array) - 1:
                    continue
                if array[i][j] == 0:
                    array[i][j] = 5

        for i in range(position[0], position[0] + size):
            if i < 0 or i > len(array) - 1:
                continue
            array[i][position[1]] = 1

def SetBoatsOnBattleMap(array, _start_boat_variants, _boat_counts_on_map):
    while _start_boat_variants >= 0:
        for count in range(0, _boat_counts_on_map.get(_start_boat_variants)):
            result = GetRandomBlockPositionForBoat(array, _boat_size.get(_start_boat_variants))
            if result[3]:
                PlaceBoatOnMap(array, result, _boat_size.get(_start_boat_variants))
            else:
                array = clearMap(array)
                _start_boat_variants = len(_boat_counts_on_map) - 1
                continue
        _start_boat_variants -= 1

def MakeTurn(array, player = False):
    if player:
        while True:
            Y = int(input("Введите координаты по Y для нанесения удара: "))
            if Y < 0 or Y > len(array) - 1:
                continue
            X = int(input("Введите координаты по X для нанесения удара: "))
            if X < 0 or X > len(array) - 1:
                continue
            if array[X][Y] == 1:
                array[X][Y] = 9
                return True
            else:
                array[X][Y] = 7
                return False
    else:
        Y = randint(0, len(array) - 1)
        X = randint(0, len(array) - 1)
        if array[Y][X] == 1:
            array[Y][X] = 9
            return True
        else:
            array[Y][X] = 7
            return False

map_size = 10 # размер карты
move_counter = 1
map_enemy = [[0] * map_size for i in range(map_size)]
map_palyer = [[0] * map_size for i in range(map_size)]
SetBoatsOnBattleMap(map_palyer, _start_boat_variants, _boat_counts_on_map)
SetBoatsOnBattleMap(map_enemy, _start_boat_variants, _boat_counts_on_map)

print(f"\n================= Поле противника =================\n")
PrintMap(map_enemy, False)
print(f"\n================= Ваше поле =================\n")
PrintMap(map_palyer, True)

while CountOfBoats(map_palyer) > 0 or CountOfBoats(map_enemy) > 0:
    print(f"\n================= Ваш ход {move_counter} =================\n")

    if MakeTurn(map_enemy, True):
        print("\n||||| Вы попали! |||||\n")
    else:
        print("\n||||| Вы промахнулись! |||||\n")
    move_counter += 1

    PrintMap(map_enemy, False)
    time.sleep(randint(2, 5))
    if MakeTurn(map_palyer, False):
        print("\n||||| Попадание по вам! |||||\n")
    else:
        print("\n||||| Промах по вам! |||||\n")

    PrintMap(map_palyer, True)

if CountOfBoats(map_palyer) > 0:
    print("Победа!")
else:
    print("Мы проиграли эту битву..")