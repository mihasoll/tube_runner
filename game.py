import pygame as pg
import numpy as np
import sys

#
# Первоначальная конфигурация 
#
DEPTH = 400  # fixme: Поменять на 720
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


def ctx(x):
    return x - SCREEN_WIDTH / 2


def ctx_back(x):
    return x + SCREEN_WIDTH / 2


def cty(y):
    return (SCREEN_HEIGHT - FREESPACE - PLAYER_R) - y


def cty_back(y):
    return (SCREEN_HEIGHT - FREESPACE - PLAYER_R) - y


class Enemy:
    def __init__(self, trajectory='parabola', props=[], color=RED):
        self.move_direction = 0
        self.r = PLAYER_R / 2
        self.color = color
        self.timer = 0
        self.died = False

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
        print(np.random.randint(-MOVESPACE / 2, -MOVESPACE / 2 + MOVESPACE * 0.1))
        c = ym
        p = (ym - ys) / (xm - xs) ** 2
        x = self.timer + xs
        self.x = ctx_back(x)
        self.y = cty_back(-p * (x - xm) ** 2 + ym)

        if cty(self.y) < ys:
            self.died = True
            print('умер')

        self.timer += self.boost


class Player:
    def __init__(self, x=ctx_back(0), y=cty_back(0)):
        self.move_direction = 0
        self.r = PLAYER_R
        self.x = x
        self.y = y
        self.color = PURPLE

    def draw(self):
        pg.draw.circle(screen, self.color, [self.x, self.y], self.r)

    def move_left(self):
        self.x -= PLAYER_SPEED
        self.x = ctx(self.x)
        if self.x < -MOVESPACE / 2:
            self.x = MOVESPACE + self.x
        self.x = ctx_back(self.x)

    def move_right(self):
        self.x += PLAYER_SPEED
        self.x = ctx(self.x)
        if self.x > MOVESPACE / 2:
            self.x = -MOVESPACE + self.x
        self.x = ctx_back(self.x)


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


def gradientrect(window, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)


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

    e2.move()
    e2.draw()

    gradientrect(screen, (0, 255, 0), (0, 100, 0), pygame.Rect(100, 100, 100, 50))
    gradientrect(screen, (255, 255, 0), (0, 0, 255), pygame.Rect(100, 200, 128, 64))

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
