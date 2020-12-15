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
MUSIC = tools.load_all_music(os.path.join('assets', 'music'))
SFX = tools.load_all_sfx(os.path.join('assets', 'sfx'))

pg.display.set_icon(GFX['icon'])

def play_sfx(sound_name, volume=0.1):
    sound = SFX[sound_name]
    sound.set_volume(volume)
    sound.play()