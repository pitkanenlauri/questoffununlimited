import pygame as pg
import os
import sys

import constants as c
import tools

def main():
    """
    Main loop for the whole program.
    """
    clock = pg.time.Clock()
    
    while True:
        dt = clock.tick(c.FPS)
        for event in pg.event.get():
            if (event.type == pg.QUIT or 
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return
        keys = pg.key.get_pressed()

def setup():
    """ 
    Initializes the pygame and sets up display window.
    """
    pg.init()
    # Centers game window.
    os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
    pg.display.set_caption(c.CAPTION)
    pg.display.set_mode(c.WINDOW_SIZE)
    
if __name__ == '__main__':
    setup()
    main()
    pg.quit()
    sys.exit()
    