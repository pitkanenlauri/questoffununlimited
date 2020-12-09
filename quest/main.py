import pygame as pg
import sys

import setup
import constants as c
import tools
import states

def main():
    game_data = tools.create_game_data_dict()
    # Create a dictionary to keep track of game states.
    state_dict = {c.SANDY_COVE: states.MapState(c.SANDY_COVE),
                  c.MYSTERIOUS_CAVE: states.MapState(c.MYSTERIOUS_CAVE),
                  c.CHICKEN_CATCH: states.ChickenCatch(c.CHICKEN_CATCH)
    }
    gm = tools.GameStatesManager()
    gm.setup(state_dict, c.SANDY_COVE)
    gm.state.start_up(game_data)
    
    clock = pg.time.Clock()
    
    while True:
        dt = clock.tick(c.FPS) / 32
        for event in pg.event.get():
            if (event.type == pg.QUIT or 
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return
        keys = pg.key.get_pressed()
        # Update game state through GameStateManager.
        gm.update(setup.window, keys, dt)
        
        # Show fps in caption.
        fps = clock.get_fps()
        with_fps = "{} - {:.2f} FPS".format(c.CAPTION, fps)
        pg.display.set_caption(with_fps)
        
        
if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()
