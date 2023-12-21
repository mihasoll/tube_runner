""" Проверка сталкновений, все спрайты"""

from show import *


def hittest(obj1, obj2):                        # object should have ctx and cty coordinats
    if obj1.real and obj2.real:                         # some objects not hittable all the time
        if abs(obj1.y - obj2.y) <= 10:                 # firstly height check
            if (abs(obj1.x - obj2.x) <= (obj1.r + obj2.r) * 0.7                             # standart hit
                    or abs(obj1.x - obj2.x) >= MOVE_SPACE - (obj1.r + obj2.r) * 0.7):        # barier hit
                obj1.dead = True
                obj2.dead = True


class Sprite():
    def __init__(self):
        self.dead = False

    def draw(self, screen):
        if not self.dead:
            image_to_screen(screen, self.icon, self.x, self.y, self.r, self.ry)


class Player(Sprite):
    def __init__(self, icon, y, x=0):
        self.move_direction = 0
        self.icon = icon
        self.r = PLAYER_R
        self.ry = PLAYER_R
        self.x = x
        self.y = y
        self.color = PURPLE
        self.dead = False
        self.real = True

    def move_left(self):
        self.x -= PLAYER_SPEED
        if self.x < -MOVE_SPACE / 2:
            self.x = MOVE_SPACE + self.x

    def move_right(self):
        self.x += PLAYER_SPEED
        if self.x > MOVE_SPACE / 2:
            self.x = -MOVE_SPACE + self.x


class Bullet(Sprite):
    def __init__(self, x):
        self.x = x
        self.y = PLAYER_R
        self.ry = 40
        self.r = 10
        self.speed = 10
        self.real = True
        self.dead = False
        self.icon = img_bullet

    def move(self):
        self.y += 10
        if self.y > DEPTH - self.ry * 2:
            self.dead = True


class Obstacle(Sprite):
    def __init__(self, x):
        self.r = 50
        self.ry = 50
        self.x = x
        self.y = DEPTH + self.ry
        self.real = True
        self.dead = False
        self.icon = img_asteroid

    def move(self):
        self.y += GRID_SPEED
        if self.y < - PLAYER_R - FREE_SPACE - EYE_DISTANCE / 2:
            self.dead = True


class Enemy(Sprite):
    # xz, yz - начальные координаты
    # g - собственное ускорение свободного падения
    # vx - горизонтальная скорость движения (может быть отрицательной)
    def __init__(self, r, xz, yz, xm, h, g, color):
        self.r = r
        self.ry = self.r
        self.ry = r
        self.x = xz
        self.y = yz
        self.yz = yz
        self.vy = (2*g*(h+PLAYER_R+FREE_SPACE))**0.5
        self.vx = xm/self.vy*g
        self.g = g
        self.color = color
        self.dead = False
        self.real = False
        self.icon = img_enemy

    def move(self):
        self.vy -= self.g
        self.y += self.vy
        self.x += self.vx

        if self.y >= DEPTH / 2:
            self.real = True

        if self.y < - PLAYER_R - FREE_SPACE:
            self.dead = True

        if self.x < -MOVE_SPACE / 2:
            self.x = MOVE_SPACE + self.x

        if self.x > MOVE_SPACE / 2:
            self.x = -MOVE_SPACE + self.x
