""" Конфигурация """
import pygame as pg

DEPTH = 600
FREE_SPACE = 10
MOVE_SPACE = 500
PLAYER_R = 30
ENEMY_R = 40

FPS = 60
GRID_SPEED = - 6
PLAYER_SPEED = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

EYE_DISTANCE = 100
SCREEN_DISTANCE = PLAYER_R + FREE_SPACE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (181, 100, 227)

img_player1 = pg.image.load("icons\\player_1.png")
img_player2 = pg.image.load("icons\\player_2.png")
img_bullet = pg.image.load("icons\\bullet.png")
img_asteroid = pg.image.load("icons\\asteroid.png")
img_enemy = pg.image.load("icons\\enemy.png")

background1_img = pg.image.load("backgrounds\\1.jpg")
background1 = pg.transform.scale(background1_img,
        (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_COLOR_1 = (183, 206, 195)
background2_img = pg.image.load("backgrounds\\2.jpg")
background2 = pg.transform.scale(background2_img,
        (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_COLOR_2 = (167, 131, 138)
background3_img = pg.image.load("backgrounds\\3.jpg")
background3 = pg.transform.scale(background3_img,
        (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_COLOR_3 = (209, 111, 131)
background4_img = pg.image.load("backgrounds\\4.jpg")
background4 = pg.transform.scale(background4_img,
        (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_COLOR_4 = (182, 215, 201)
background6_img = pg.image.load("backgrounds\\6.jpg")
background6 = pg.transform.scale(background6_img,
        (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_COLOR_6 = (166, 232, 237)

loading_screen1 = pg.image.load("backgrounds\\load_screen_1.jpeg")
img_loading_screen1 = pg.transform.scale(loading_screen1,
        (SCREEN_WIDTH, SCREEN_HEIGHT))
loading_screen2 = pg.image.load("backgrounds\\load_screen_2.jpg")
img_loading_screen2 = pg.transform.scale(loading_screen2,
        (SCREEN_WIDTH, SCREEN_HEIGHT))

gameover_screen = pg.image.load('backgrounds\\GAME_OVER.jpg')
img_gameover = pg.transform.scale(gameover_screen,
        (SCREEN_WIDTH, SCREEN_HEIGHT))

modes = ['TWO PLAYERS', ' ', 'ONE PLAYER']
backgrounds = [background1,
               background2,
               background3,
               background4,
               background6]
background_colors = [BACKGROUND_COLOR_1,
                     BACKGROUND_COLOR_2,
                     BACKGROUND_COLOR_3,
                     BACKGROUND_COLOR_4,
                     BACKGROUND_COLOR_6]
loading_screens = [img_loading_screen1, img_loading_screen2]