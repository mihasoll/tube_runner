""" Выводит координаты и картинки """

from config import *
import numpy as np
import pygame as pg


def out(xc, yc):
    r = EYE_DISTANCE * SCREEN_HEIGHT / 2 / (EYE_DISTANCE + SCREEN_DISTANCE + yc)
    phi = xc * 2 * np.pi / MOVE_SPACE
    x = SCREEN_WIDTH / 2 + r * np.sin(phi)
    y = SCREEN_HEIGHT / 2 + r * np.cos(phi)
    return [x, y, r, phi]


def image_to_screen(screen, img, x, y, r, ry):
    outc = out(x, y)
    r = (EYE_DISTANCE * SCREEN_HEIGHT / 2 *
         (1 / (EYE_DISTANCE + SCREEN_DISTANCE + y) - 1 / (EYE_DISTANCE + SCREEN_DISTANCE + y + r)))
    ry = (EYE_DISTANCE * SCREEN_HEIGHT / 2 *
         (1 / (EYE_DISTANCE + SCREEN_DISTANCE + y) - 1 / (EYE_DISTANCE + SCREEN_DISTANCE + y + ry)))
    scaled_img = pg.transform.scale(img, (r * 2, ry * 2))
    r = r * (abs(np.cos(outc[3])) + abs(np.sin(outc[3])))
    ry = ry * (abs(np.cos(outc[3])) + abs(np.sin(outc[3])))
    rotated_img = pg.transform.rotate(scaled_img, 360 * outc[3] / 2 / np.pi)
    screen.blit(rotated_img, (outc[0] - r, outc[1] - ry))
