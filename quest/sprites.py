import pygame as pg
import random

import constants as c

class Sprite(pg.sprite.Sprite):
    def __init__(self, name, x, y, action='resting', direction='down'):
        super().__init__()
        self.name = name
        self.action = action
        self.direction = direction
        self.speed = 1
        self.distance = 0
        self.pixels_moved = 0
        
        self.action_dict = self.create_action_dict()
        self.vector_dict = self.create_vector_dict()
        
        # Test
        self.image = pg.image.load(self.name + '.png').convert_alpha()
        self.rect = self.image.get_rect(left=x, top=y)
    
    def create_action_dict(self):
        action_dict = {'resting': self.resting,
                      'moving':  self.moving,
                      'auto_moving': self.auto_moving
        }
        return action_dict
    
    def create_vector_dict(self):
        vector_dict = {'up': (0, -1),
                       'down': (0, 1),
                       'left': (-1, 0),
                       'right': (1, 0)
        }
        return vector_dict
    
    def update(self, dt):
        self.dt = dt
        
        action_function = self.action_dict[self.action]
        action_function()
    
    def resting(self):
        self.correct_position()
    
    def moving(self):
        """
        Moves sprite from one tile to the next based on direction.
        """
        # Calculate the change in distance based on speed. (s = s_0 + vt)
        self.distance += self.speed * self.dt
        
        # Distance moved is stored in self.distance, but game movement happens 
        # only when distance is over one pixel.
        if self.distance >= 1:
            pixels_to_move = int(round(self.distance))
            
            # move_ip moves rect by given x and y offset to self.direction
            self.rect.move_ip(
                self.vector_dict[self.direction][0] * pixels_to_move,
                self.vector_dict[self.direction][1] * pixels_to_move)
            
            self.pixels_moved += pixels_to_move
            self.distance = 0.0
            
            # Move one tile at a time.
            if self.pixels_moved >= c.TILE_WIDTH:
                self.begin_resting()
                self.pixels_moved = 0
    
    def begin_resting(self):
        self.action = 'resting'
        self.distance = 0
        self.pixels_moved = 0
        self.correct_position()    
    
    def begin_moving(self, direction):
        self.action = 'moving'
        self.direction = direction
    
    def auto_moving(self):
        pass
    
    def correct_position(self):
        """
        Adjusts sprites position to be centered on a tile.
        """
        x_off = self.rect.x % c.TILE_WIDTH
        y_off = self.rect.y % c.TILE_WIDTH
        
        if x_off != 0:
            if x_off <= c.TILE_WIDTH / 2:
                self.rect.x -= x_off
            else:
                self.rect.x += (c.TILE_WIDTH - x_off)
        
        if y_off != 0:
            if y_off <= c.TILE_WIDTH / 2:
                self.rect.y -= y_off
            else:
                self.rect.y += (c.TILE_WIDTH - y_off)
    

class Player(Sprite):
    def __init__(self, x, y, action, direction):
        super().__init__('player', x, y, action, direction)
        self.speed = 2
    
    def update(self, keys, dt):
        self.keys = keys
        self.check_for_input()
        self.dt = dt
        action_function = self.action_dict[self.action]
        action_function()
    
    def check_for_input(self):
        if self.action == 'resting':
            if self.keys[pg.K_UP]:
                self.begin_moving('up')
            elif self.keys[pg.K_DOWN]:
                self.begin_moving('down')
            elif self.keys[pg.K_LEFT]:
                self.begin_moving('left')
            elif self.keys[pg.K_RIGHT]:
                self.begin_moving('right')
    
class Square(Sprite):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.moves = ['up', 'down', 'left', 'right']
        self.speed = 0.5
    
    def auto_moving(self):
        self.begin_moving(self.moves[random.randint(0, 3)])
    
    def update(self, dt):
        self.dt = dt
        if self.action == 'resting':
            self.auto_moving()
        action_function = self.action_dict[self.action]
        action_function()
    