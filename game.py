import pygame as pg
import numpy as np
import sys


# parameters
DEPTH = 400
SCREEN_WIDTH = 1280
MOVESPACE = np.pi * DEPTH
FPS = 60
GRID_SPEED = -2
PLAYER_SPEED = 10
PLAYER_R = 30
FREESPACE = 10
SCREEN_HEIGHT = (DEPTH + PLAYER_R + FREESPACE)
EYE_DISTANCE = 150

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
                    or abs(obj1.x - obj2.x) >= MOVESPACE - obj1.r + obj2.r):        # barier hit
                print('hit')
                obj1.dead = True
                obj2.dead = True


class Enemy:
    def __init__(self, trajectory='parabola', props=[], color=RED):
        self.move_direction = 0
        self.r = PLAYER_R/2
        self.ry = self.r
        self.color = color
        self.timer = 0
        self.died = False
        self.real = False

        if trajectory == 'parabola':
            self.xs = props[0]
            self.ys = props[1]
            self.xm = props[2]
            self.ym = props[3]
            self.boost = props[4]
        
    def draw(self):
        pg.draw.circle(screen, self.color, [self.x, self.y], self.r)
            
    def move(self):
        # Вычисление траектории происходит здесь

        # Все координаты центральные!
        # Начало
        xs = self.xs 
        ys = self.ys
        # Максимум 
        xm = self.xm
        ym = self.ym
        #print(np.random.randint(-MOVESPACE/2,-MOVESPACE/2+MOVESPACE*0.1))
        c = ym 
        p = (ym-ys)/(xm-xs)**2
        x = self.timer+xs
        self.x = ctx_back(x)  
        self.y = cty_back(-p*(x-xm)**2+ym)

        if cty(self.y) >= DEPTH / 2:
            self.real = True

        if cty(self.y)<ys: 
            self.died=True
            #print('умер')
        
        self.timer += self.boost


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

e1 = Enemy('parabola', [-500, -200, -100, SCREEN_HEIGHT/2, 5])
e2 = Enemy('parabola', [-600, -300, -100, SCREEN_HEIGHT/2, 10])

e1 = Enemy('parabola', [-500, -200, -100, SCREEN_HEIGHT / 2, 5])
e2 = Enemy('parabola', [-600, -300, -100, SCREEN_HEIGHT / 2, 10])

while True:
    screen.fill(BLACK)

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

    hittest(player, e1)
    #hittest(player, e2)

    pg.display.flip()
    clock.tick(FPS)
