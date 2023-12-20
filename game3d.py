import pygame as pg
import numpy as np
import sys
import random


DEPTH = 600
MOVE_SPACE = 500
FREE_SPACE = 10
PLAYER_R = 30

FPS = 60
GRID_SPEED = -6
PLAYER_SPEED = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

EYE_DISTANCE = 100
SCREEN_DISTANCE = PLAYER_R + FREE_SPACE


def out(xc, yc):  # Характеристики для вывода
    r = EYE_DISTANCE * SCREEN_HEIGHT / 2 / (EYE_DISTANCE + SCREEN_DISTANCE + yc)
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


def image_to_screen(img, x, y, r, ry):
    outc = out(x, y)
    #pg.draw.circle(screen, WHITE, [outc[0], outc[1]], r)
    r = (EYE_DISTANCE * SCREEN_HEIGHT / 2 *
         (1 / (EYE_DISTANCE + SCREEN_DISTANCE + y) - 1 / (EYE_DISTANCE + SCREEN_DISTANCE + y + r)))
    ry = (EYE_DISTANCE * SCREEN_HEIGHT / 2 *
         (1 / (EYE_DISTANCE + SCREEN_DISTANCE + y) - 1 / (EYE_DISTANCE + SCREEN_DISTANCE + y + ry)))
    scaled_img = pg.transform.scale(img, (r * 2, ry * 2))
    r = r * (abs(np.cos(outc[3])) + abs(np.sin(outc[3])))
    ry = ry * (abs(np.cos(outc[3])) + abs(np.sin(outc[3])))
    rotated_img = pg.transform.rotate(scaled_img, 360 * outc[3] / 2 / np.pi)
    screen.blit(rotated_img, (outc[0] - r, outc[1] - ry))


def hittest(obj1, obj2):                        # object should have ctx and cty coordinats
    if obj1.real and obj2.real:                         # some objects not hittable all the time
        if abs(obj1.y - obj2.y) <= 10:                 # firstly height check
            if (abs(obj1.x - obj2.x) <= (obj1.r + obj2.r) * 0.7                             # standart hit
                    or abs(obj1.x - obj2.x) >= MOVE_SPACE - (obj1.r + obj2.r) * 0.7):        # barier hit
                obj1.dead = True
                obj2.dead = True


def run_menu():
    theme_number = 0
    mode = 1
    left_pressed, right_pressed = False, False
    background = backgrounds[theme_number]
    GRID_COLOR = background_colors[theme_number]
    play = False
    bullets = []

    button_mode = Button_mode()
    button_play = Button_play()
    button_style = Button_style()
    button_quit = Button_quit()

    while not play:
        # screen.fill(BLACK)
        screen.blit(background, (0, 0))

        environment.radials(GRID_COLOR)
        environment.circles_move(GRID_COLOR)
        environment.circles_draw(GRID_COLOR)
        button_mode.draw()
        button_play.draw()
        button_style.draw()
        button_quit.draw()

        for bullet in bullets:
            hittest(bullet, button_mode)
            hittest(bullet, button_play)
            hittest(bullet, button_style)
            hittest(bullet, button_quit)
            if bullet.dead:
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw()
        if button_mode.dead:
            mode *= -1
            button_mode.dead = False
        if button_play.dead:
            play = True
            button_play.dead = False
        if button_style.dead:
            theme_number = (theme_number + 1) % len(backgrounds)
            background = backgrounds[theme_number]
            button_style.dead = False
        if button_quit.dead:
            play = True
            mode = 0

        player1.draw()

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
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                bullets.append(Bullet(player1.x))
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        if left_pressed:
            player1.move_left()
        if right_pressed:
            player1.move_right()

        pg.display.flip()
        clock.tick(FPS)

    screen.blit(background, (0, 0))
    if mode == 1:
        run_single_player(background, background_colors[theme_number])
    elif mode == -1:
        run_double_player(background, background_colors[theme_number])
    else:
        pg.quit()


def run_single_player(background, GRID_COLOR):
    left_pressed, right_pressed = False, False
    ticks = 0
    RELOAD = 30
    bullets = []
    obstacles = []
    enemies = []
    while not player1.dead:
        screen.blit(background, (0, 0))

        ticks += 1

        if ticks % RELOAD == 0:
            bullets.append(Bullet(player1.x))
        for bullet in bullets:
            if bullet.dead:
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw()

        if ticks % (2 * RELOAD) == 0:
            obstacles.append(Obstacle(random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2))))
        for obstacle in obstacles:
            hittest(player1, obstacle)
            if obstacle.dead:
                obstacles.remove(obstacle)
            else:
                obstacle.move()
                obstacle.draw()

        if ticks % (2 * RELOAD) == 0:
            enemies.append(Enemy(PLAYER_R, random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2)),
                                 -PLAYER_R-FREE_SPACE, random.randint(round(0.25*MOVE_SPACE), round(0.6*MOVE_SPACE)),
                                 random.randint(round(DEPTH/2), round(DEPTH*3/4)), 0.5, WHITE))
        for enemy in enemies:
            hittest(player1, enemy)
            for bullet in bullets:
                hittest(enemy, bullet)
            if enemy.dead:
                enemies.remove(enemy)
            else:
                enemy.move()
                enemy.draw()

        environment.radials(GRID_COLOR)
        environment.circles_move(GRID_COLOR)
        environment.circles_draw(GRID_COLOR)

        player1.draw()

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
            player1.move_left()
        if right_pressed:
            player1.move_right()

        pg.display.flip()
        clock.tick(FPS)
    player1.dead = False
    run_menu()


def run_double_player(background, GRID_COLOR):
    player2 = Player(test_player2)
    RELOAD = 30
    ticks = 0
    bullets = []
    obstacles = []
    enemies =[]
    a_pressed, d_pressed = False, False
    left_pressed, right_pressed = False, False
    while (not player1.dead) or (not player2.dead):
        screen.blit(background, (0, 0))

        environment.radials(GRID_COLOR)
        environment.circles_move(GRID_COLOR)
        environment.circles_draw(GRID_COLOR)

        ticks += 1

        if ticks % RELOAD == 0:
            if not player1.dead:
                bullets.append(Bullet(player1.x))
            if not player2.dead:
                bullets.append(Bullet(player2.x))
        for bullet in bullets:
            if bullet.dead:
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw()

        if ticks % (5 * RELOAD) == 0:
            obstacles.append(Obstacle(random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2))))
        for obstacle in obstacles:
            hittest(player1, obstacle)
            hittest(player2, obstacle)
            for enemy in enemies:
                hittest(obstacle, enemy)
            if obstacle.dead:
                obstacles.remove(obstacle)
            else:
                obstacle.move()
                obstacle.draw()

        if ticks % (2 * RELOAD) == 0:
            enemies.append(Enemy(PLAYER_R, random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2)),
                                 -PLAYER_R-FREE_SPACE, random.randint(round(0.25*MOVE_SPACE), round(0.6*MOVE_SPACE)),
                                 random.randint(round(DEPTH/2), round(DEPTH*3/4)), 0.5, WHITE))
        for enemy in enemies:
            hittest(player1, enemy)
            hittest(player2, enemy)
            for bullet in bullets:
                hittest(enemy, bullet)
            if enemy.dead:
                enemies.remove(enemy)
            else:
                enemy.move()
                enemy.draw()

        player1.draw()
        player2.draw()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                a_pressed = True
                d_pressed = False
            if event.type == pg.KEYDOWN and event.key == pg.K_d:
                d_pressed = True
                a_pressed = False
            if event.type == pg.KEYUP and event.key == pg.K_a:
                a_pressed = False
            if event.type == pg.KEYUP and event.key == pg.K_d:
                d_pressed = False

            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                left_pressed = True
                right_pressed = False
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                right_pressed = True
                left_pressed = False
            if event.type == pg.KEYUP and event.key == pg.K_LEFT:
                left_pressed = False
            if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                right_pressed = False
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        if left_pressed:
            player2.move_left()
        if right_pressed:
            player2.move_right()
        if a_pressed:
            player1.move_left()
        if d_pressed:
            player1.move_right()

        pg.display.flip()
        clock.tick(FPS)

    player1.dead = False
    run_menu()

class Player:
    def __init__(self, icon,  x=0, y=0):
        self.move_direction = 0
        self.icon = icon
        self.r = PLAYER_R
        self.ry = PLAYER_R
        self.x = x
        self.y = y
        self.color = PURPLE
        self.dead = False
        self.real = True

    def draw(self):
        if not self.dead:
            image_to_screen(self.icon, self.x, self.y, self.r, self.ry)

    def move_left(self):
        self.x -= PLAYER_SPEED
        if self.x < -MOVE_SPACE / 2:
            self.x = MOVE_SPACE + self.x

    def move_right(self):
        self.x += PLAYER_SPEED
        if self.x > MOVE_SPACE / 2:
            self.x = -MOVE_SPACE + self.x


class Bullet:
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

    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)


class Obstacle:
    def __init__(self, x):
        self.r = 40
        self.ry = 40
        self.x = x
        self.y = DEPTH + self.ry
        self.real = True
        self.dead = False
        self.icon = img_asteroid

    def move(self):
        self.y += GRID_SPEED
        if self.y < - PLAYER_R - FREE_SPACE:
            self.dead = True

    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)


class Enemy:
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
        self.icon = test_player2

    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)

    def move(self):
        self.vy -= self.g
        self.y += self.vy
        self.x += self.vx

        if self.y >= DEPTH / 2:
            self.real = True

        if self.y< - PLAYER_R - FREE_SPACE:
            self.dead = True

        if self.x < -MOVE_SPACE / 2:
            self.x = MOVE_SPACE + self.x

        if self.x > MOVE_SPACE / 2:
            self.x = -MOVE_SPACE + self.x


class Environment:
    def __init__(self):
        self.circles_number = round((DEPTH + EYE_DISTANCE) / DEPTH * 3)
        self.rows_crds = [i * (DEPTH + EYE_DISTANCE) / self.circles_number - EYE_DISTANCE
                          for i in range(0, self.circles_number)]

    def colorfunc(self, min, current):
        return (255 * current / min / 10 + 100)

    def circles_draw(self, color):
        #pg.draw.circle(screen, WHITE, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], out(0, 0)[2], 3)
        for yc in self.rows_crds:
            radius = out(0, yc)[2]
            # c = self.colorfunc(DEPTH*2/self.circles_number, rds[i])
            pg.draw.circle(screen, color, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], radius, 1)

    def circles_move(self, color):
        for i in range(0, self.circles_number):
            self.rows_crds[i] += GRID_SPEED
            if self.rows_crds[i] <= - EYE_DISTANCE:
                self.rows_crds[i] = self.rows_crds[i] + EYE_DISTANCE + DEPTH
            else:
                pg.draw.circle(screen, color,
                               [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], out(0, DEPTH)[2], 1)

    def radials(self, color):
        count = 5
        for i in range(-count, count):
            outc = out(MOVE_SPACE / 2 * i / count, -EYE_DISTANCE)
            outc2 = out(MOVE_SPACE / 2 * i / count, DEPTH)
            pg.draw.line(screen, color, [outc[0], outc[1]], [outc2[0], outc2[1]], 1)


class Button_mode:
    def __init__(self):
        self.x = - MOVE_SPACE / 6
        self.y = DEPTH / 4
        self.icon = img_asteroid
        self.r = MOVE_SPACE / 12 - 5
        self.ry = PLAYER_R
        self.real = True
        self.dead = False
    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)


class Button_play:
    def __init__(self):
        self.x = 0
        self.y = DEPTH / 4
        self.icon = img_asteroid
        self.r = MOVE_SPACE / 12 - 5
        self.ry = PLAYER_R
        self.real = True
        self.dead = False
    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)


class Button_style:
    def __init__(self):
        self.x = MOVE_SPACE / 6
        self.y = DEPTH / 4
        self.icon = img_asteroid
        self.r = MOVE_SPACE / 12 - 5
        self.ry = PLAYER_R
        self.real = True
        self.dead = False

    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)


class Button_quit:
    def __init__(self):
        self.x = MOVE_SPACE / 2
        self.y = DEPTH/ 4
        self.icon = img_asteroid
        self.r = MOVE_SPACE / 12 - 5
        self.ry = PLAYER_R
        self.real = True
        self.dead = False

    def draw(self):
        image_to_screen(self.icon, self.x, self.y, self.r, self.ry)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (181, 100, 227)

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()

img_player1 = pg.image.load("icons\\player_1.png")
test_player2 = pg.image.load("icons\\test_player_2.png")
img_bullet = pg.image.load("icons\\bullet.png")
img_asteroid = pg.image.load("icons\\asteroid.png")

background1_img = pg.image.load("backgrounds\\dark_cosmos.jpg")
background1 = pg.transform.scale(background1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_COLOR_1 = (183, 206, 195)

environment = Environment()
player1 = Player(img_player1)
backgrounds = [background1]         # ADD MORE
background_colors = [BACKGROUND_COLOR_1]
pg.display.update()

run_menu()

