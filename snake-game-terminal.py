#!/usr/bin/env python3
import random
from time import sleep
import os
import sys
import re
plat = None
try:
    from smoothIO import raw, nonblocking
    plat = "linux"
except ModuleNotFoundError:
    plat = "win"
    import msvcrt


# author = Sujan Parajuli aka (____) @sujanP100
# github = /sujanP100
# _____________________________________________


RATE = 0.08
WALL = ("|", "-", '+')  # "◙" horizontal and vertical wall and cornor
GROUND = " "
FOOD = "0"  # "◉"
SNAKE_SKIN = "*"  # "■"
ROW = 20
COL = 50
POINTS = 0

# i am not able to add arrow key :( (NOOB). So if somebody with better knowledge
# than I have can solve this issue than please help me
k = {
    "UP": [119, 87],
    "DOWN": [115, 83],
    "RIGHT": [100, 68],
    "LEFT": [97, 65],
    "QUIT": [113]}


def gen_playground():
    # return [[WALL[1] if j == 0 or j == COL - 1 or i == 0 or i ==
    # ROW - 1 else GROUND for j in range(COL)] for i in range(ROW)]
    return [
        [
            WALL[2] if (
                j == 0 and i == 0) or (
                i == 0 and j == COL -
                1) or (
                    i == ROW -
                    1 and j == COL -
                    1) or (
                        i == ROW -
                        1 and j == 0) else WALL[0] if (
                            (j == 0 or j == COL -
                             1) and (
                                i != 0 or i != ROW -
                                1)) else WALL[1] if (
                                    i == 0 or i == ROW -
                                    1) and (
                                        j != 0 or j != COL -
                1) else GROUND for j in range(COL)] for i in range(ROW)]


playground = gen_playground()


def put(char, coor, playground=playground):
    x, y = coor
    playground[x][y] = char


class Snake:
    def __init__(self, char):
        self.__char = char
        self.__sl = [(ROW // 2, COL // 2), (ROW // 2, COL //
                                            2 - 1), (ROW // 2, COL // 2 - 2)]
        self.__head = self.__sl[0]
        self.isMoving = False

    def add(self):
        for cr in self.__sl:
            playground[cr[0]][cr[1]] = self.__char

    def get_sl(self):
        return self.__sl

    def set_sl(self, l):
        self.__sl = l

    def get_head(self):
        return self.__head

    def movement(self, key):
        if key == 'r':
            self.isMoving = True
            self.__sl.insert(0, (self.__head[0], self.__head[1] + 1))
        elif key == 'l':
            self.isMoving = True
            self.__sl.insert(0, (self.__head[0], self.__head[1] - 1))
        elif key == 'u':
            self.isMoving = True
            self.__sl.insert(0, (self.__head[0] - 1, self.__head[1]))
        elif key == 'd':
            self.isMoving = True
            self.__sl.insert(0, (self.__head[0] + 1, self.__head[1]))
        try:
            self.add()
        except BaseException:
            pass
        self.__head = self.__sl[0]

    def hasEaten(self, f_c):
        return self.__head == f_c

    def isDead(self):
        try:
            if self.__head[0] >= ROW - \
                    1 or self.__head[0] <= 0 or self.__head[1] >= COL - 1 or self.__head[1] <= 0:
                return True
        except BaseException:
            print("Game Over")
            return

        for i in range(len(self.__sl)):
            if i != 0 and self.__sl[i] == self.__head:
                return True
        return

    def update(self):
        put(GROUND, self.__sl[-1])
        self.__sl.pop()


def d(playground):
    for x in playground:
        print(''.join(x))


def gc(r, c, sl):
    while True:
        x, y = random.randint(1, r - 2), random.randint(1, c - 2)
        if (x, y) not in sl:
            return (x, y)


sn = Snake(SNAKE_SKIN)
sn.add()
f_c = gc(ROW, COL, sn.get_sl())
put(FOOD, f_c)
key = ''

status = 1


game_start = False


def game(q):
    global f_c
    global POINTS
    global key
    global status
    global game_start
    # stats
    print(
        "PLAYGROUND_SIZE({} {}):food coor: {} | snake length: {} | points: {}".format(
            ROW, COL, f_c, len(
                sn.get_sl()), POINTS))

    if q in k["QUIT"]:
        if plat == "linux":
            os.system("clear")
        else:
            os.system('cls')
        print("Thank you for playing :)")
        sys.exit()
    if q in k["UP"] and key != 'd':
        key = 'u'
    elif q in k["DOWN"] and key != 'u':
        key = 'd'
    elif q in k['RIGHT'] and key != 'l':
        key = 'r'
    elif q in k["LEFT"] and key != 'r':
        key = 'l'
    if not game_start:
        if key == 'l':
            key = 'r'
        elif key:
            game_start = True
    sn.movement(key)
    if sn.isDead():
        status = 0
    if sn.hasEaten(f_c):
        f_c = gc(ROW, COL, sn.get_sl())
        put(FOOD, f_c)
        POINTS += 1
    elif not sn.hasEaten(f_c) and sn.isMoving:
        sn.update()

    d(playground)


def linux():
    global status
    with raw(sys.stdin):
        with nonblocking(sys.stdin):
            status = 1
            os.system("clear")
            while status:
                try:
                    q = sys.stdin.read(1) or '~'
                    q = ord(q)
                    game(q)
                except IOError:
                    print('not ready')
                sleep(RATE)
                if status:
                    os.system("clear")
                else:
                    print("GAME OVER!")


def win():
    global status
    os.system('cls')
    q = None
    while status:
        if msvcrt.kbhit():
            q = ord(msvcrt.getch())
        game(q)
        sleep(RATE)
        if status:
            os.system("cls")
        else:
            print("GAME OVER!")


def main():
    if plat == 'linux':
        linux()
    else:
        win()


if __name__ == '__main__':
    main()
