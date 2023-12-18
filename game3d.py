import pygame as pg
import numpy as np
import sys
import random


DEPTH = 1200
MOVE_SPACE = 1000
FREE_SPACE = 10
PLAYER_R = 30

FPS = 60
GRID_SPEED = -10
PLAYER_SPEED = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

EYE_DISTANCE = 150
SCREEN_DISTANCE = PLAYER_R + FREE_SPACE


def out(xc, yc):  # Характеристики для вывода
    r = EYE_DISTANCE * SCREEN_HEIGHT / 2 / (EYE_DISTANCE + SCREEN_DISTANCE + yc)
    phi = xc * 2 * np.pi / MOVE_SPACE
    x = SCREEN_WIDTH / 2 + r * np.sin(phi)
    y = SCREEN_HEIGHT / 2 + r * np.cos(phi)
    return [x, y, r, phi]


def out_stars(xc, yc):  # Характеристики для вывода
    if (EYE_DISTANCE + SCREEN_DISTANCE + yc) != 0:
        r = EYE_DISTANCE * SCREEN_HEIGHT * 1.5 / 2 / (EYE_DISTANCE + SCREEN_DISTANCE + yc)
    else:
        r = EYE_DISTANCE * SCREEN_HEIGHT * 1.5 / 2
    phi = xc * 2 * np.pi / MOVE_SPACE
    x = SCREEN_WIDTH / 2 + r * np.sin(phi)
    y = SCREEN_HEIGHT / 2 + r * np.cos(phi)
    return [x, y, r, phi]


def ctx(x):
    return x - SCREEN_WIDTH / 2


def ctx_back(x):
    return x + SCREEN_WIDTH / 2


def cty(y):
    return (SCREEN_HEIGHT - FREE_SPACE - PLAYER_R) - y


def cty_back(y):
    return (SCREEN_HEIGHT - FREE_SPACE - PLAYER_R) - y


def image_to_screen(img, x, y, r):
    outc = out(x, y)
    #pg.draw.circle(screen, WHITE, [outc[0], outc[1]], r)
    r = (EYE_DISTANCE * SCREEN_HEIGHT / 2 *
         (1 / (EYE_DISTANCE + SCREEN_DISTANCE + y) - 1 / (EYE_DISTANCE + SCREEN_DISTANCE + y + r)))
    scaled_img = pg.transform.scale(img, (r * 2, r * 2))
    r = r * (abs(np.cos(outc[3])) + abs(np.sin(outc[3])))
    rotated_img = pg.transform.rotate(scaled_img, 360 * outc[3] / 2 / np.pi)
    screen.blit(rotated_img, (outc[0] - r, outc[1] - r))


class Player:
    def __init__(self, x=ctx_back(0), y=cty_back(0)):
        self.move_direction = 0
        self.r = PLAYER_R
        self.x = x
        self.y = y
        self.color = PURPLE

    def draw(self):
        image_to_screen(img_player, ctx(self.x), ctx(self.y), self.r)
        #image_to_screen(img_player, ctx(self.x), ctx(self.y), self.r)



    def move_left(self):
        self.x -= PLAYER_SPEED
        self.x = ctx(self.x)
        if self.x < -MOVE_SPACE / 2:
            self.x = MOVE_SPACE + self.x
        self.x = ctx_back(self.x)

    def move_right(self):
        self.x += PLAYER_SPEED
        self.x = ctx(self.x)
        if self.x > MOVE_SPACE / 2:
            self.x = -MOVE_SPACE + self.x
        self.x = ctx_back(self.x)


class Environment:
    def __init__(self):
        self.stars_number = 100
        self.star_length = - 50 * GRID_SPEED
        self.stars_ys = [random.randint(- EYE_DISTANCE * 20, DEPTH - self.star_length) for i in range(self.stars_number)]
        space = MOVE_SPACE/self.stars_number
        self.stars_xs = [-MOVE_SPACE/2 + space*i + random.randint(round(-space/2), round(space/2))
                         for i in range(self.stars_number)]

        self.circles_number = round((DEPTH + EYE_DISTANCE) / DEPTH * 3)
        self.rows_crds = [i * (DEPTH + EYE_DISTANCE) / self.circles_number - EYE_DISTANCE
                          for i in range(0, self.circles_number)]

    def colorfunc(self, min, current):
        return (255 * current / min / 10 + 100)

    def circles_draw(self):
        #pg.draw.circle(screen, WHITE, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], out(0, 0)[2], 3)
        pg.draw.circle(screen, LIGHT_BLUE, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], out(0, DEPTH)[2], 1)
        for yc in self.rows_crds:
            radius = out(0, yc)[2]
            # c = self.colorfunc(DEPTH*2/self.circles_number, rds[i])
            pg.draw.circle(screen, LIGHT_BLUE, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], radius, 1)

    def circles_move(self):
        for i in range(0, self.circles_number):
            self.rows_crds[i] += GRID_SPEED
            if self.rows_crds[i] <= - EYE_DISTANCE:
                self.rows_crds[i] = self.rows_crds[i] + EYE_DISTANCE + DEPTH

    def radials(self):
        count = 5
        for i in range(-count, count):
            outc = out(MOVE_SPACE / 2 * i / count, -EYE_DISTANCE)
            outc2 = out(MOVE_SPACE / 2 * i / count, DEPTH)
            pg.draw.line(screen, LIGHT_BLUE, [outc[0], outc[1]], [outc2[0], outc2[1]], 1)

    def flying_stars(self):
        for i in range(self.stars_number):
            outc = out_stars(self.stars_xs[i], self.stars_ys[i])
            outc2 = out_stars(self.stars_xs[i], self.stars_ys[i] + self.star_length)
            pg.draw.line(screen, LIGHT_BLUE, [outc[0], outc[1]], [outc2[0], outc2[1]], 1)
            self.stars_ys[i] += 3 * GRID_SPEED
            if self.stars_ys[i] <= - EYE_DISTANCE:
                self.stars_ys[i] = self.stars_ys[i] + EYE_DISTANCE + DEPTH

        # def makeLines(coe,count):
        # out1 = out(-MOVE_SPACE*coe/count, 0)
        # out2 = out(-MOVE_SPACE*coe/count, 3*DEPTH)
        # pg.draw.line(screen,WHITE,[out1[0],out1[1]],[out2[0],out2[1]], 2)
        # out1 = out(MOVE_SPACE*coe/count, 0)
        # out2 = out(MOVE_SPACE*coe/count, 3*DEPTH)
        # pg.draw.line(screen,WHITE,[out1[0],out1[1]],[out2[0],out2[1]], 2)
        # [makeLines(i,10) for i in range(0,12)]


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (181, 100, 227)
LIGHT_BLUE = (183, 206, 195)

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()

img_player = pg.image.load("icons\\tetsplayer.png")
background_img = pg.image.load("dark_cosmos.jpg")
background = pg.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

environment = Environment()
player = Player()

pg.display.update()

left_pressed, right_pressed = False, False

while True:
    #screen.fill(BLACK)
    screen.blit(background, (0, 0))

    environment.radials()
    environment.circles_move()
    environment.circles_draw()
    #environment.flying_stars()

    player.draw()

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

