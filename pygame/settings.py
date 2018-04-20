# SETTINGS
import os
import pygame as pg

TITLE = "XXXXXXX"
WIDTH = 700
HEIGHT = 300
FPS = 60

# Player properties
PLAYER_ACC = 0.3
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 10
SPRITESHEET = "spritesheet.png"
FONT_NAME = 'arial'
HS_FILE = "hsc.txt"
BACKGROUND = "img/bk.png"

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 10, WIDTH, 10)] #(x, y, w, h)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (0, 191,  255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)