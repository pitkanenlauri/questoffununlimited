import pygame as pg
import os

import constants as c

class GameStatesManager:
    """
    Control class for managing game states.
    """
    def __init__(self):
        self.state_dict = {}
        self.state_name = None
        self.state = None
    
    def setup(self, state_dict, start_state):
        """
        Given a dictionary of states and a state to start in, builds the 
        self.state_dict.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    
    def update(self, window, keys, dt):
        """
        Checks if a state is done. Changes state if necessary 
        and state.update is called.
        """
        if self.state.done:
            self.flip_state()
        self.state.update(window, keys, dt)
        
    def flip_state(self):
        """
        Changes to a new state and performs clean_up for exiting state 
        and start_up for new state. (Most importantly passing on game data.)
        """
        previous, self.state_name = self.state_name, self.state.next
        game_data = self.state.clean_up()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.start_up(game_data)
        
class State:
    """
    Template class for all game states to inherit from.
    """
    def __init__(self):
        self.done = False
        self.game_data = None
        self.next = None
        self.previous = None
    
    def start_up(self, game_data):
        self.game_data = game_data
    
    def clean_up(self):
        self.done = False
        return self.game_data
    
    def update(self, window, keys, dt):
        """
        Update method for state. Must be overrided in children.
        """
        pass
    

def create_game_data_dict():
    """
    Creates a dictionary of game data to be carried 
    between states and for save game functionality.
    """
    data_dict = {'last_location': None,
    }
    return data_dict

def load_all_gfx(directory, colorkey=c.WHITE, accept=('.png')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics

def load_all_tmx(directory, accept=('.tmx')):
    tmx = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if ext.lower() in accept:
            tmx[name] = os.path.join(directory, file)
    return tmx


class Camera:
    """
    Class to handle world scrolling. Applying moves target rect position so 
    that screen view is centered on source_rect.
    NOTE: 320 and 240 are because used tileset is 16 bits and we scale it 2x.
    Incase you remove 2x scaling change to true window width and height.
    """
    def __init__(self, map_width, map_height):
        self.state = pg.Rect(0, 0, map_width, map_height)
    
    def apply(self, target_rect):
        """
        Offsets target rects position according to camera state.
        """
        return target_rect.move(self.state.topleft)
    
    def update(self, source_rect):
        """
        Updates camera to follow source_rect.
        """
        x = - source_rect.center[0] + 320 // 2
        y = - source_rect.center[1] + 240 // 2
        position = pg.Vector2(self.state.topleft)
        position += (pg.Vector2((x, y)) - position)
        self.state.topleft = (int(position.x), int(position.y))
        self.state.x = max(-(self.state.width - 320), min(0, self.state.x))
        self.state.y = max(-(self.state.height - 240), min(0, self.state.y))


class Portal:
    """
    Used for storing the transportation points between maps.
    """
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pg.Rect(x, y, c.TILE_WIDTH, c.TILE_WIDTH)
    

