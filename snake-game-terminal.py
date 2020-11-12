#!/usr/bin/env python3
import re
from smoothIO import raw, nonblocking
import random
import sys
import os
from time import sleep

# author = Sujan Parajuli aka (____) @sujanP100
# github = /sujanP100
# _____________________________________________


RATE = 0.08
WALL = "◙"
GROUND = " "
FOOD = "◉"
SNAKE_BODY = "■"
ROW = 50
COL = 80
POINTS = 0
k = {"UP": "w", "DOWN": 's', "RIGHT": 'd', "LEFT": 'a'}

playground = [[WALL if j == 0 or j == COL - 1 or i == 0 or i ==
               ROW - 1 else GROUND for j in range(COL)] for i in range(ROW)]


def put(char, coor, playground=playground):
    x, y = coor
    playground[x][y] = char


class Snake:
    def __init__(self, char, speed):
        self.__char = char
        self.__sl = [(ROW // 2, COL // 2), (ROW // 2 , COL // 2 - 1), (ROW // 2 , COL // 2 - 2)]
        self.__head = self.__sl[0]
        self.isMoving = False

    def add(self):
        for cr in self.__sl:
            playground[cr[0]][cr[1]] = self.__char

    def get_sl(self):
        return self.__sl

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
            if self.__head[0] >= ROW - 1 or self.__head[0] <= 0 or self.__head[1] >= COL - 1 or self.__head[1] <= 0:
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


sn = Snake(SNAKE_BODY, 1)
sn.add()
f_c = gc(ROW, COL, sn.get_sl())
put(FOOD, f_c)


def main():
    global f_c
    global POINTS
    with raw(sys.stdin):
        with nonblocking(sys.stdin):
            status = 1
            os.system("clear")
            key = ''
            while status:
                try:
                    print(
                        "(R: {} , C: {}) : POINTS: {}, FOOD: {}, BODY: {}, WALL: {}".format(
                            ROW, COL, POINTS, FOOD, SNAKE_BODY, WALL))
                    q = sys.stdin.read(1)
                    print(q)
                    if q == "q":
                        os.system("clear")
                        print("Thank you for playing :)")
                        sys.exit()
                    if q == k["UP"] and key != 'd':
                        key = 'u'
                    elif q == k["DOWN"] and key != 'u':
                        key = 'd'
                    elif q == k['RIGHT'] and key != 'l':
                        key = 'r'
                    elif q == k["LEFT"] and key != 'r':
                        key = 'l'
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
                except IOError:
                    print('not ready')
                sleep(RATE)
                if status:
                    os.system("clear")
                else:
                    print("GAME OVER!")


if __name__ == '__main__':
    main()
