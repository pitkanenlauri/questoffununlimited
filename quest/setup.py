import pygame as pg
import os

import constants as c
import tools

# Center game window.
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'

pg.init()
pg.display.set_caption(c.CAPTION)
window = pg.display.set_mode(c.WINDOW_SIZE)

GFX = tools.load_all_gfx(os.path.join('assets', 'graphics'))
TMX = tools.load_all_tmx(os.path.join('assets', 'tmx'))
FONTS = tools.load_all_fonts(os.path.join('assets', 'fonts'))

pg.display.set_icon(GFX['icon'])