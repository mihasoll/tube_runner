import sys
import random

from models import *
from show import *


def run_menu():
    theme_number = 0
    mode = 1
    left_pressed, right_pressed = False, False
    background = backgrounds[theme_number]
    GRID_COLOR = background_colors[theme_number]
    play = False
    bullets = []

    button_mode = ButtonMode()
    button_play = ButtonPlay()
    button_style = ButtonStyle()
    button_quit = ButtonQuit()

    while not play:
        screen.blit(background, (0, 0))
        img = font.render(f'KILLS: {BODY_COUNT}', True, GRID_COLOR)
        screen.blit(img, (10, 10))

        environment.radials(GRID_COLOR)
        environment.circles_move(GRID_COLOR)
        environment.circles_draw(GRID_COLOR)
        button_mode.draw(font.render(modes[mode + 1], True, GRID_COLOR))
        button_play.draw(font.render('PLAY', True, GRID_COLOR))
        button_style.draw(font.render('CHANGE STYLE', True, GRID_COLOR))
        button_quit.draw(font.render('QUIT', True, GRID_COLOR))

        for bullet in bullets:
            hit_test(bullet, button_mode)
            hit_test(bullet, button_play)
            hit_test(bullet, button_style)
            hit_test(bullet, button_quit)
            if bullet.dead:
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw(screen)
        if button_mode.dead:
            mode *= -1
            button_mode.dead = False
        if button_play.dead:
            play = True
            button_play.dead = False
        if button_style.dead:
            n = random.randint(0, len(loading_screens) - 1)
            for i in range(round(0.7 * FPS)):
                screen.blit(loading_screens[n], (0, 0))
                pg.display.flip()
                clock.tick(FPS)
            theme_number = (theme_number + 1) % len(backgrounds)
            background = backgrounds[theme_number]
            GRID_COLOR = background_colors[theme_number]
            button_style.dead = False
        if button_quit.dead:
            play = True
            mode = 0

        player1.draw(screen)

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
        n = random.randint(0, len(loading_screens) - 1)
        for i in range(FPS):
            screen.blit(loading_screens[n], (0, 0))
            pg.display.flip()
            clock.tick(FPS)
        pg.quit()


def run_single_player(background, GRID_COLOR):
    left_pressed, right_pressed = False, False
    global BODY_COUNT
    BODY_COUNT = 0
    ticks = 0
    RELOAD = 30
    bullets = []
    obstacles = []
    enemies = []
    while not player1.dead:
        screen.blit(background, (0, 0))
        img = font.render(f'KILLS: {BODY_COUNT}', True, GRID_COLOR)
        screen.blit(img, (10, 10))

        ticks += 1

        if ticks % RELOAD == 0:
            bullets.append(Bullet(player1.x))
        for bullet in bullets:
            if bullet.dead:
                if bullet.y < DEPTH - bullet.ry * 2:
                    BODY_COUNT += 1
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw(screen)

        if ticks % (2 * RELOAD) == 0:
            obstacles.append(Obstacle(random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2))))
        for obstacle in obstacles:
            hit_test(player1, obstacle)
            if obstacle.dead:
                obstacles.remove(obstacle)
            else:
                obstacle.move()
                obstacle.draw(screen)

        if ticks % (2 * RELOAD) == 0:
            enemies.append(Enemy(ENEMY_R, random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2)),
                                 -PLAYER_R-FREE_SPACE, random.randint(round(- 0.8*MOVE_SPACE), round(0.8*MOVE_SPACE)),
                                 random.randint(round(DEPTH/2), round(DEPTH*3/4)), 0.5, WHITE))
        for enemy in enemies:
            hit_test(player1, enemy)
            for bullet in bullets:
                hit_test(enemy, bullet)
            if enemy.dead:
                enemies.remove(enemy)
            else:
                enemy.move()
                enemy.draw(screen)

        environment.radials(GRID_COLOR)
        environment.circles_move(GRID_COLOR)
        environment.circles_draw(GRID_COLOR)

        player1.draw(screen)

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
    for i in range(FPS):
        screen.blit(img_gameover, (0, 0))
        pg.display.flip()
        clock.tick(FPS)
    run_menu()


def run_double_player(background, GRID_COLOR):
    player2 = Player(img_player2, 0)
    global BODY_COUNT
    BODY_COUNT = 0
    RELOAD = 30
    ticks = 0
    bullets = []
    obstacles = []
    enemies =[]
    a_pressed, d_pressed = False, False
    left_pressed, right_pressed = False, False
    while (not player1.dead) or (not player2.dead):
        screen.blit(background, (0, 0))
        img = font.render(f'KILLS: {BODY_COUNT}', True, GRID_COLOR)
        screen.blit(img, (10, 10))

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
                if bullet.y < DEPTH - bullet.ry * 2:
                    BODY_COUNT += 1
                bullets.remove(bullet)
            else:
                bullet.move()
                bullet.draw(screen)

        if ticks % (2 * RELOAD) == 0:
            obstacles.append(Obstacle(random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2))))
        for obstacle in obstacles:
            hit_test(player1, obstacle)
            hit_test(player2, obstacle)
            for enemy in enemies:
                hit_test(obstacle, enemy)
            if obstacle.dead:
                obstacles.remove(obstacle)
            else:
                obstacle.move()
                obstacle.draw(screen)

        if ticks % (2 * RELOAD) == 0:
            enemies.append(Enemy(ENEMY_R, random.randint(round(-MOVE_SPACE / 2), round(MOVE_SPACE / 2)),
                                 -PLAYER_R-FREE_SPACE, random.randint(round(-0.8*MOVE_SPACE), round(0.8*MOVE_SPACE)),
                                 random.randint(round(DEPTH/2), round(DEPTH*3/4)), 0.5, WHITE))
        for enemy in enemies:
            hit_test(player1, enemy)
            hit_test(player2, enemy)
            for bullet in bullets:
                hit_test(enemy, bullet)
            if enemy.dead:
                enemies.remove(enemy)
            else:
                enemy.move()
                enemy.draw(screen)

        player1.draw(screen)
        player2.draw(screen)

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
    for i in range(FPS):
        screen.blit(img_gameover, (0, 0))
        pg.display.flip()
        clock.tick(FPS)
    run_menu()


class Environment:
    def __init__(self):
        self.circles_number = round((DEPTH + EYE_DISTANCE) / DEPTH * 3)
        self.rows_crds = [i * (DEPTH + EYE_DISTANCE) / self.circles_number - EYE_DISTANCE
                          for i in range(0, self.circles_number)]

    def colorfunc(self, min, current):
        return (255 * current / min / 10 + 100)

    def circles_draw(self, color):
        for yc in self.rows_crds:
            radius = out(0, yc)[2]
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


class ButtonMode:
    def __init__(self):
        self.x = - MOVE_SPACE / 6
        self.y = DEPTH / 4
        self.r = MOVE_SPACE / 3
        self.ry = PLAYER_R
        self.real = True
        self.dead = False

    def draw(self, icon):
        image_to_screen(screen, icon, self.x, self.y, self.r, self.ry)


class ButtonPlay:
    def __init__(self):
        self.x = 0
        self.y = DEPTH / 5
        self.r = MOVE_SPACE / 6
        self.ry = PLAYER_R * 1.5
        self.real = True
        self.dead = False

    def draw(self, icon):
        image_to_screen(screen, icon, self.x, self.y, self.r, self.ry)


class ButtonStyle:
    def __init__(self):
        self.x = MOVE_SPACE / 6
        self.y = DEPTH / 8
        self.r = MOVE_SPACE / 6
        self.ry = PLAYER_R * 0.8
        self.real = True
        self.dead = False

    def draw(self, icon):
        image_to_screen(screen, icon, self.x, self.y, self.r, self.ry)


class ButtonQuit:
    def __init__(self):
        self.x = MOVE_SPACE / 2
        self.y = DEPTH/ 4
        self.icon = img_asteroid
        self.r = MOVE_SPACE / 8
        self.ry = PLAYER_R * 1.4
        self.real = True
        self.dead = False

    def draw(self, icon):
        icon = pg.transform.rotate(icon, 180)
        image_to_screen(screen, icon, self.x, self.y, self.r, self.ry)


pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()
font = pg.font.SysFont('Comic Sans', 48)

player1 = Player(img_player1, - PLAYER_R / 3)
BODY_COUNT = 0

environment = Environment()
pg.display.update()

n = random.randint(0, len(loading_screens) - 1)
for i in range(FPS):
    screen.blit(loading_screens[n], (0, 0))
    pg.display.flip()
    clock.tick(FPS)
run_menu()
