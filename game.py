import pygame as pg
import numpy as np
import sys
import random


# parameters
DEPTH = 400
SCREEN_WIDTH = 1280
MOVESPACE = 1200
FPS = 60
GRID_SPEED = -2
PLAYER_SPEED = 10
PLAYER_R = 30
FREESPACE = 10
SCREEN_HEIGHT = (DEPTH + PLAYER_R + FREESPACE)
EYE_DISTANCE = 150
RELOAD = 20


# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (181, 100, 227)
RED = (255, 0, 0)


def ctx(x):                         # recalculating x to playzone coordinate system
    return x - SCREEN_WIDTH / 2


def ctx_back(x):                    # recalculating  x from playzone system to screen coordinate system
    return x + SCREEN_WIDTH / 2


def cty(y):                         # recalculating y to playzone coordinate system
    return (SCREEN_HEIGHT - FREESPACE - PLAYER_R) - y


def cty_back(y):                    # recalculating  y from playzone system to screen coordinate system
    return (SCREEN_HEIGHT - FREESPACE - PLAYER_R) - y


def hittest(obj1, obj2):                        # object should have ctx and cty coordinats
    if obj1.real and obj2.real:                         # some objects not hittable all the time
        if abs(obj1.y - obj2.y) <= obj1.ry + obj2.ry:                 # firstly height check
            if (abs(obj1.x - obj2.x) <= obj1.r + obj2.r                             # standart hit
                    or abs(obj1.x - obj2.x) >= MOVESPACE - obj1.r - obj2.r):        # barier hit
                print('hit')
                obj1.dead = True
                obj2.dead = True

class Enemy:
    # xz, yz - начальные координаты
    # g - собственное ускорение свободного падения
    # vx - горизонтальная скорость движения (может быть отрицательной)
    def __init__(self, r, xz, yz, xm, h, g, color):
        self.r = r
        self.ry = r
        self.x = xz
        self.y = yz
        self.yz = yz
        self.vy = (2*g*(h+PLAYER_R+FREESPACE+EYE_DISTANCE))**0.5
        self.vx = xm/self.vy*g
        self.g = g
        self.color = color
        self.died = False
        self.real = False

    def draw(self):
        pg.draw.circle(screen, self.color, [ctx_back(self.x), cty_back(self.y)], self.r)

    def move(self):
        self.vy -= self.g
        self.y += self.vy
        self.x += self.vx

        if self.y >= DEPTH / 2:
            self.real = True

        if self.y<self.yz:
            self.died = True

        if self.x < -MOVESPACE / 2:
            self.x = MOVESPACE + self.x

        if self.x > MOVESPACE / 2:
            self.x = -MOVESPACE + self.x

class Enemy2:
    def __init__(self, trajectory='parabola', props=[], color=RED):
        self.r = PLAYER_R/2
        self.ry = self.r
        self.color = color
        self.timer = 0
        self.died = False
        self.real = False

        if trajectory == 'parabola':
            self.xs = props[0]
            self.ys = props[1]
            self.x = self.xs
            self.y = self.ys
            self.xm = props[2]
            self.ym = props[3]
            self.vx = props[4]
            self.g = props[5]

        # Все координаты центральные!
        # Начало
        xs = self.xs
        ys = self.ys
        # Максимум
        xm = self.xm
        ym = self.ym

        self.p = (ym - ys) / (xm - xs) ** 2
        
    def draw(self):
        pg.draw.circle(screen, self.color, [ctx_back(self.x), cty_back(self.y)], self.r)
            
    def move(self):

        self.x = self.x + self.vx
        #self.y = -self.p*(self.x-self.xm)**2+self.ym

        if self.x < -MOVESPACE / 2:
            self.x = MOVESPACE + self.x

        if self.x > MOVESPACE / 2:
            self.x = -MOVESPACE + self.x

        if self.y >= DEPTH / 2:
            self.real = True

        if self.y<self.ys:
            self.died = True

class Player:
    def __init__(self, x=0, y=0):       # he lives in playzone coordinate system
        self.move_direction = 0
        self.r = PLAYER_R
        self.ry = self.r
        self.x = x
        self.y = y
        self.color = PURPLE
        self.real = True
        self.dead = False

    def draw(self):
        pg.draw.circle(screen, self.color, [ctx_back(self.x), cty_back(self.y)], self.r)

    def move_left(self):
        self.x -= PLAYER_SPEED
        if self.x < -MOVESPACE / 2:
            self.x = MOVESPACE + self.x

    def move_right(self):
        self.x += PLAYER_SPEED
        if self.x > MOVESPACE / 2:
            self.x = -MOVESPACE + self.x


class Bullet:
    def __init__(self, x):
        self.x = x
        self.y = PLAYER_R
        self.ry = 20
        self.r = 3
        self.speed = 10
        self.real = True
        self.dead = False

    def move(self):
        self.y += 10
        if self.y > DEPTH - self.ry * 2:
            self.dead = True

    def draw(self):
        pg.draw.rect(screen, WHITE,
                     (ctx_back(self.x - self.r), cty_back(self.y + self.ry * 2),
                      self.r * 2, self.ry * 2))


class Obstacle:
    def __init__(self, x):
        self.r = 40
        self.ry = 40
        self.x = x
        self.y = DEPTH + self.ry
        self.real = True
        self.dead = False

    def move(self):
        self.y += GRID_SPEED
        if self.y < - PLAYER_R - FREESPACE - EYE_DISTANCE:
            self.dead = True

    def draw(self):
        pg.draw.rect(screen, WHITE,
                     (ctx_back(self.x - self.r), cty_back(self.y + self.ry),
                      self.r * 2, self.ry * 2))


class Test:
    def __init__(self):
        self.rows_number = 6
        self.rows_crds = [i * DEPTH / self.rows_number for i in range(0, self.rows_number)]

    def boundaries(self):
        count = 5
        pg.draw.line(screen, WHITE, [ctx_back(-MOVESPACE / 2), cty_back(0)],
                     [ctx_back(-MOVESPACE / 2), cty_back(DEPTH)], 3)
        pg.draw.line(screen, WHITE, [ctx_back(MOVESPACE / 2), cty_back(0)],
                     [ctx_back(MOVESPACE / 2), cty_back(DEPTH)], 3)
        for i in range(-count, count):
            pg.draw.line(screen, WHITE, [ctx_back(MOVESPACE / 2 * i / count), cty_back(0)],
                         [ctx_back(MOVESPACE / 2 * i / count), cty_back(DEPTH)], 1)

        pg.draw.line(screen, WHITE, [ctx_back(-MOVESPACE / 2), cty_back(0)],
                     [ctx_back(MOVESPACE / 2), cty_back(0)])
        pg.draw.line(screen, WHITE, [ctx_back(-MOVESPACE / 2), cty_back(DEPTH)],
                     [ctx_back(MOVESPACE / 2), cty_back(DEPTH)])

    def rows_move(self):
        crds = self.rows_crds
        for i in range(0, len(crds)):
            self.rows_crds[i] += GRID_SPEED
            if self.rows_crds[i] <= 0:
                self.rows_crds[i] = self.rows_crds[i] + DEPTH

    def rows_draw(self):
        for el in self.rows_crds:
            pg.draw.line(screen, WHITE, [ctx_back(-MOVESPACE / 2), cty_back(el)],
                         [ctx_back(MOVESPACE / 2), cty_back(el)])


pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT + EYE_DISTANCE])
clock = pg.time.Clock()

test = Test()
player = Player()

pg.display.update()

left_pressed, right_pressed = False, False

pygame = pg

e1 = Enemy(PLAYER_R, -MOVESPACE/2, -PLAYER_R-FREESPACE-EYE_DISTANCE,
           random.randint(round(0.25*MOVESPACE),round(0.6*MOVESPACE)),
           random.randint(round(DEPTH/2),round(DEPTH*3/4)), 0.5, WHITE)

ticks = 0
bullets = []
obstacles = []

while True:
    screen.fill(BLACK)
    ticks += 1

    if e1.died == True:
        e1 = Enemy(PLAYER_R, random.randint(-MOVESPACE / 2, MOVESPACE / 2) , -PLAYER_R - FREESPACE - EYE_DISTANCE,
                   random.randint(round(-0.6 * MOVESPACE), round(0.6 * MOVESPACE)),
                   random.randint(round(DEPTH / 2), round(DEPTH * 3 / 4)), 0.5, WHITE)

    if ticks % RELOAD == 0:
        bullets.append(Bullet(player.x))
    for bullet in bullets:
        if bullet.dead:
            bullets.remove(bullet)
        else:
            bullet.move()
            bullet.draw()

    if ticks % (5 * RELOAD) == 0:
        obstacles.append(Obstacle(random.randint(round(-MOVESPACE/2), round(MOVESPACE/2))))
    for obstacle in obstacles:
        hittest(player, obstacle)
        if obstacle.dead:
            obstacles.remove(obstacle)
        else:
            obstacle.move()
            obstacle.draw()
    hittest(player, e1)


    test.boundaries()
    test.rows_move()
    test.rows_draw()

    player.draw()

    e1.move()
    e1.draw()

    #e2.move()
    #e2.draw()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_a:
            left_pressed = True
            right_pressed = False
        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            right_pressed = True
            left_pressed = False
        if event.type == pg.KEYUP and event.key == pg.K_a:
            left_pressed = False
        if event.type == pg.KEYUP and event.key == pg.K_d:
            right_pressed = False
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if left_pressed:
        player.move_left()
    if right_pressed:
        player.move_right()

    pg.display.flip()
    clock.tick(FPS)
