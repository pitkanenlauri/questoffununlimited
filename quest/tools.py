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
        self.set_music()
    
    def update(self, window, keys, dt, events):
        """
        Checks if a state is done. Changes state if necessary 
        and state.update is called.
        """
        if self.state.done:
            self.flip_state()
        self.state.update(window, keys, dt, events)
        
    def flip_state(self):
        """
        Changes to a new state and performs clean_up for exiting state 
        and start_up for new state. (Most importantly passing on game data.)
        """
        previous, self.state_name = self.state_name, self.state.next
        previous_music = self.state.music_title
        game_data = self.state.clean_up()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.previous_music = previous_music
        self.state.start_up(game_data)
        self.set_music()
    
    def set_music(self):
        """
        Play correct music for the state.
        """
        if self.state.music_title == self.state.previous_music:
            pass
        elif self.state.music:
            pg.mixer.music.load(self.state.music)
            pg.mixer.music.set_volume(self.state.volume)
            pg.mixer.music.play(-1)
        
class State:
    """
    Template class for all game states to inherit from.
    """
    def __init__(self):
        self.done = False
        self.game_data = None
        self.next = None
        self.previous = 'start'
    
    def start_up(self, game_data):
        self.game_data = game_data
    
    def clean_up(self):
        self.done = False
        return self.game_data
    
    def update(self, window, keys, dt, events):
        """
        Update method for state. Must be overrided in children.
        """
        pass
    

def create_game_data_dict():
    """
    Creates a dictionary of game data to be carried 
    between states and for save game functionality.
    """
    # Items that player has collected and is carrying.
    ##################################################
    player_data = {'gold': 0,
                   'chickens': {'show': False,
                                'amount': 0,
                                'max': 0,
                                'catchable': False,
                                'rescue': False,
                                'catch': False},
                   'found_items': set(),
                   'catched_chickens': set()
                   }
    
    # Data for quests.
    ##################################################
    chicken_rescue = {'class_name': ChickenRescue(),
                      'i': 0,
                      'dialogs': {0: 'start',
                                  1: 'complete'}
    }
    
    chicken_catch = {'class_name': ChickenCatch(),
                     'i': 0,
                     'dialogs': {0: 'run_away',
                                 1: 'thanks'}
    }
    
    quests = {'chicken_rescue': chicken_rescue,
              'chicken_catch': chicken_catch
              }
    
    # Compile the above into game data dictionary.
    ##################################################
    game_data_dict = {'player_data': player_data,
                      'quest_data': quests,
                      'active_quests': {'chicken_rescue'},
                      'current_map': None
                      }
    return game_data_dict

def load_all_gfx(directory, colorkey=c.WHITE, accept=('.png', 'jpg', 'bmp')):
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

def load_all_fonts(directory, accept=('.ttf')):
    return load_all_tmx(directory, accept)

def load_all_music(directory, accept=('.mp3', '.ogg')):
    return load_all_tmx(directory, accept)

def load_all_sfx(directory, accept=('.wav','.ogg',)):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


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
    def __init__(self, name, x, y, sound):
        self.name = name
        self.rect = pg.Rect(x, y, c.TILE_WIDTH, c.TILE_WIDTH)
        self.sound = sound
    
    
class Dialogue:
    """
    Class for storing dialogues and info needed to initiate them 
    in the right time in the right place. (Place assigned in Tiled.)
    """
    def __init__(self, name, x, y, properties):
        self.name = name
        self.rect = pg.Rect(x, y, c.TILE_WIDTH, c.TILE_WIDTH)
        self.dict = properties
        

class Quest:
    def __init__(self):
        self.active = True
        self.completed = False
        self.name = None
    
    def open(self, game_data):
        self.game_data = game_data
        pass
    
    def update(self):
        pass
    
    def deactivate(self):
        pass


class ChickenRescue(Quest):
    def __init__(self):
        super().__init__()
        self.name = 'chicken_rescue'
    
    def open(self, game_data):
        game_data['player_data']['chickens']['show'] = True
        game_data['player_data']['chickens']['max'] = 3
        if game_data['current_map'] == c.MYSTERIOUS_CAVE:
            game_data['player_data']['chickens']['catchable'] = True
            game_data['player_data']['chickens']['rescue'] = True
        self.game_data = game_data
        
        
    def update(self):
        if not self.completed:
            if self.game_data['player_data']['chickens']['amount'] == 3:
                self.completed = True
                self.game_data['quest_data'][self.name]['i'] = 1
    
    def deactivate(self):
        self.active = False
        self.game_data['player_data']['chickens']['catchable'] = False
        self.game_data['player_data']['chickens']['rescue'] = False
        self.game_data['player_data']['chickens']['show'] = False
        self.game_data['player_data']['chickens']['amount'] = 0
        self.game_data['active_quests'].add('chicken_catch')


class ChickenCatch(Quest):
    def __init__(self):
        super().__init__()
        self.name = 'chicken_catch'
    
    def open(self, game_data):
        game_data['player_data']['chickens']['show'] = True
        game_data['player_data']['chickens']['max'] = 23
        if game_data['current_map'] == c.SANDY_COVE:
            game_data['player_data']['chickens']['catchable'] = True
            game_data['player_data']['chickens']['catch'] = True
        self.game_data = game_data
    
    def update(self):
        if not self.completed:
            if self.game_data['player_data']['chickens']['amount'] == 23:
                self.completed = True
                self.game_data['quest_data'][self.name]['i'] = 1
    
    def deactivate(self):
        self.active = False
        self.game_data['player_data']['chickens']['catchable'] = False
        self.game_data['player_data']['chickens']['catch'] = False
        self.game_data['player_data']['chickens']['show'] = False
        self.game_data['player_data']['catched_chickens'].clear()
        self.game_data['player_data']['chickens']['amount'] = 0


