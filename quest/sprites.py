import pygame as pg
import random

import constants as c
from setup import GFX

class Sprite(pg.sprite.Sprite):
    def __init__(self, sheet_key, x, y, action='resting', direction='down'):
        super().__init__()
        self.name = sheet_key
        self.action = action
        self.direction = direction

        self.action_dict = self.create_action_dict()
        self.vector_dict = self.create_vector_dict()
        self.spritesheet_dict = self.create_spritesheet_dict(sheet_key)
        self.animation_dict = self.create_animation_dict()
        
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(left=x, top=y)
        
        self.speed = 1
        self.distance = 0
        self.pixels_moved = 0

        self.blockers = self.set_blockers()
        
    def create_spritesheet_dict(self, sheet_key):
        """
        Makes a dictionary of images from sprite sheet.
        """
        image_list = []
        image_dict = {}
        sheet = GFX[sheet_key]
        tw = c.TILE_WIDTH
        
        # u = up, d = down, l = left, r = right
        image_keys = ['u0', 'u1', 'u2', 'u3',
                      'd0', 'd1', 'd2', 'd3',
                      'l0', 'l1', 'l2', 'l3',
                      'r0', 'r1', 'r2', 'r3']

        for row in range(4):
            for column in range(4):
                image = pg.Surface([tw, tw])
                image.blit(sheet, (0, 0), (column*tw, row*tw, tw, tw))
                image.set_colorkey(c.COLORKEY)
                image_list.append(image)
                

        for key, image in zip(image_keys, image_list):
            image_dict[key] = image
        
        return image_dict    
    
    def create_animation_dict(self):
        """
        Returns a dictionary of image lists for animation.
        """
        d = self.spritesheet_dict
        
        up_list     = [d['u0'], d['u1'], d['u2'], d['u3']]
        down_list   = [d['d0'], d['d1'], d['d2'], d['d3']]
        left_list   = [d['l0'], d['l1'], d['l2'], d['l3']]
        right_list  = [d['r0'], d['r1'], d['r2'], d['r3']]


        direction_dict = {'up': up_list,
                          'down': down_list,
                          'left': left_list,
                          'right': right_list}

        return direction_dict
    
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
        self.blockers = self.set_blockers()
        self.dt = dt
        action_function = self.action_dict[self.action]
        action_function()
    
    def resting(self):
        self.correct_position()
    
    def moving(self):
        """
        Moves sprite from one tile to the next based on direction.
        """
        # Change self.image to animate movement based on steps between tiles.
        self.image = self.image_list[self.pixels_moved // (c.TILE_WIDTH // 4)]
        
        # Calculate the change in distance based on speed. (s = s_0 + v*t)
        self.distance += self.speed * self.dt
        
        # Distance moved is stored in self.distance, but game movement happens 
        # only when distance is over one pixel.
        if self.distance >= 1:
            pixels_to_move = int(round(self.distance))
            
            # move_ip moves rect by given x and y offset to self.direction.
            self.rect.move_ip(
                self.vector_dict[self.direction][0] * pixels_to_move,
                self.vector_dict[self.direction][1] * pixels_to_move)
            
            self.pixels_moved += pixels_to_move
            self.distance = 0
            
            # Move one tile at a time.
            if self.pixels_moved >= c.TILE_WIDTH:
                self.begin_resting()
                self.pixels_moved = 0

    def auto_moving(self):
        pass
    
    def begin_resting(self):
        self.action = 'resting'
        self.distance = 0
        self.pixels_moved = 0
        self.correct_position()
        self.image = self.image_list[0]
    
    def begin_moving(self, direction):
        self.action = 'moving'
        self.direction = direction
        self.image_list = self.animation_dict[self.direction]
    
    def correct_position(self):
        """
        Adjusts sprites position to be centered on a tile.
        """
        tw = c.TILE_WIDTH
        x_off = self.rect.x % tw
        y_off = self.rect.y % tw
        
        if x_off != 0:
            if x_off <= tw / 2:
                self.rect.x -= x_off
            else:
                self.rect.x += (tw - x_off)
        
        if y_off != 0:
            if y_off <= tw / 2:
                self.rect.y -= y_off
            else:
                self.rect.y += (tw - y_off)
    
    def set_blockers(self):
        """
        Create blocker rects to prevent collision with other sprites.
        If sprite is resting, blocker is sprite.rect.
        If sprite is moving, blockers are the source and
        the destination tile sprite is moving in between.
        """
        blockers = []
        
        tw = c.TILE_WIDTH
        x = self.rect.x
        y = self.rect.y
        
        if self.pixels_moved == 0:
            blockers.append(pg.Rect(self.rect.topleft, (tw, tw)))
        else:
            if self.rect.x % tw != 0:
                tile1 = ( (x // tw) * tw , y)
                tile2 = ( ((x + tw) // tw ) * tw , y)
                tile1_rect = pg.Rect(tile1, (tw, tw))
                tile2_rect = pg.Rect(tile2, (tw, tw))
                blockers.extend([tile1_rect, tile2_rect])
            elif self.rect.y & tw:
                tile1 = ( x, (y // tw) * tw )
                tile2 = ( x, ((y + tw) // tw ) * tw)
                tile1_rect = pg.Rect(tile1, (tw, tw))
                tile2_rect = pg.Rect(tile2, (tw, tw))
                blockers.extend([tile1_rect, tile2_rect])

        return blockers
                
class Player(Sprite):
    def __init__(self, x, y, action, direction):
        super().__init__('player', x, y, action, direction)
        self.speed = 1
    
    def update(self, keys, dt):
        self.blockers = self.set_blockers()
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
    
class Wanderer(Sprite):
    def __init__(self, name, x, y, direction):
        super().__init__(name, x, y, direction=direction)
        self.moves = ['up', 'down', 'left', 'right']
        self.speed = 0.5
    
    def auto_moving(self):
        self.begin_moving(self.moves[random.randint(0, 3)])
    
    def update(self, dt):
        self.blockers = self.set_blockers()
        self.dt = dt
        if self.action == 'resting':
            self.auto_moving()
        action_function = self.action_dict[self.action]
        action_function()
    
