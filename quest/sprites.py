import pygame as pg

import constants as c

class Sprite(pg.sprite.Sprite):
    def __init__(self, name, x, y, state='resting', direction='down'):
        super().__init__()
        self.tile_x = x
        self.tile_y = y
        self.name = name
        self.state = state
        self.direction = direction
        # Keeps track of distance when moving between tiles.
        self.move_distance = 0
        
        self.sprite_state_dict = self.create_state_dict()
        self.vector_dict = self.create_vector_dict()
        
        self.dt = None
        
        self.image = pg.image.load('cube.png').convert_alpha()
        self.rect = self.image.get_rect(left=x, top=y)
    
    def create_state_dict(self):
        state_dict = {'resting': self.resting,
                      'moving':  self.moving
        }
        return state_dict
    
    def create_vector_dict(self):
        vector_dict = {'up': (0, -1),
                       'down': (0, 1),
                       'left': (-1, 0),
                       'right': (1, 0)
        }
        return vector_dict
    
    def update(self, dt):
        self.dt = dt
        state_function = self.sprite_state_dict[self.state]
        state_function()
    
    def resting(self):
        if self.rect.y % c.TILE_WIDTH != 0:
            self.correct_position(self.rect.y)
        if self.rect.x % c.TILE_WIDTH != 0:
            self.correct_position(self.rect.x)
    
    def moving(self):
        px = self.vector_dict[self.direction][0] * self.dt
        py = self.vector_dict[self.direction][1] * self.dt
        self.move_distance += abs(px + py)
        if self.move_distance >= 1:
            self.rect.move_ip(int(px), int(py))
        if self.move_distance >= c.TILE_WIDTH:
            self.state = 'resting'
            self.move_distance = 0
    
    def begin_moving(self, direction):
        self.direction = direction
        self.state = 'moving'
    
    def correct_position(self, rect_pos):
        """
        Adjust sprite position to be centered on tile.
        """
        diff = rect_pos % c.TILE_WIDTH
        print(diff)
        if diff <= c.TILE_WIDTH // 2:
            rect_pos - diff
        else:
            rect_pos + diff
    
    def get_tile_coordinates(self):
        """
        Converts pygame coordinates into tile coordinates.
        """
        if self.rect.x == 0:
            tile_x = 0
        elif self.rect.x % c.TILE_WIDTH == 0:
            tile_x = (self.rect.x / c.TILE_WIDTH)
        else:
            tile_x = 0

        if self.rect.y == 0:
            tile_y = 0
        elif self.rect.y % c.TILE_WIDTH == 0:
            tile_y = (self.rect.y / c.TILE_WIDTH)
        else:
            tile_y = 0

        return [tile_x, tile_y]
        

class Player(Sprite):
    def __init__(self, x, y, state, direction):
        super().__init__('player', x, y, state, direction)
    
    def update(self, keys, dt):
        self.keys = keys
        self.check_for_input()
        self.dt = dt
        state_function = self.sprite_state_dict[self.state]
        state_function()
    
    def check_for_input(self):
        if self.state == 'resting':
            if self.keys[pg.K_UP]:
                self.begin_moving('up')
                self.tile_y += 1
            elif self.keys[pg.K_DOWN]:
                self.begin_moving('down')
                self.tile_y -= 1
            elif self.keys[pg.K_LEFT]:
                self.begin_moving('left')
                self.tile_x -= 1
            elif self.keys[pg.K_RIGHT]:
                self.begin_moving('right')
                self.tile_x += 1
            