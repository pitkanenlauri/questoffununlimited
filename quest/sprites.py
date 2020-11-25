import pygame as pg

import constants as c

class Sprite(pg.sprite.Sprite):
    def __init__(self, name, x, y, action='resting', direction='down'):
        super().__init__()
        self.name = name
        self.action = action
        self.direction = direction
        # Keeps track of distance when moving between tiles.
        self.move_distance = 0.0
        self.move_pixel = 0.0
        
        self.action_dict = self.create_action_dict()
        self.vector_dict = self.create_vector_dict()
        
        # Test
        self.image = pg.image.load(self.name + '.png').convert_alpha()
        self.rect = self.image.get_rect(left=x, top=y)
        
        # Location in tile grid coordinates.
        self.tile_x, self.tile_y = self.get_tile_coordinates()
    
    def create_action_dict(self):
        action_dict = {'resting': self.resting,
                      'moving':  self.moving
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
        px = self.vector_dict[self.direction][0] * self.dt
        py = self.vector_dict[self.direction][1] * self.dt
        self.move_pixel += abs(px + py)
        self.move_distance += self.move_pixel
        
        if self.move_pixel >= 1:
            self.rect.move_ip(
                int(self.vector_dict[self.direction][0] * self.move_pixel),
                int(self.vector_dict[self.direction][1] * self.move_pixel))
            self.move_distance = int(self.move_distance)
            self.move_pixel = 0.0
        
        if self.move_distance >= c.TILE_WIDTH:
            self.action = 'resting'
            self.move_distance = 0.0
            self.move_pixel = 0.0
    
    def begin_moving(self, direction):
        self.direction = direction
        self.action = 'moving'
    
    def correct_position(self):
        """
        Adjust sprite position to be centered on tile if not.
        """
        x, y = self.get_tile_coordinates()
        x_off = self.rect.x % c.TILE_WIDTH
        y_off = self.rect.y % c.TILE_WIDTH
        if self.rect.x % c.TILE_WIDTH != 0:
            if x_off <= c.TILE_WIDTH / 2:
                self.rect.x = x
            else:
                self.rect.x = x + c.TILE_WIDTH
        if self.rect.y % c.TILE_WIDTH != 0:
            if y_off <= c.TILE_WIDTH / 2:
                self.rect.y = y
            else:
                self.rect.y = y + c.TILE_WIDTH
    
    def get_tile_coordinates(self):
        """
        Converts pygame coordinates into tile coordinates.
        """
        if self.rect.x == 0:
            tile_x = 0
        elif self.rect.x % c.TILE_WIDTH == 0:
            tile_x = (self.rect.x // c.TILE_WIDTH)
        else:
            tile_x = 0

        if self.rect.y == 0:
            tile_y = 0
        elif self.rect.y % c.TILE_WIDTH == 0:
            tile_y = (self.rect.y // c.TILE_WIDTH)
        else:
            tile_y = 0
        
        return tile_x, tile_y
        

class Player(Sprite):
    def __init__(self, x, y, action, direction):
        super().__init__('player', x, y, action, direction)
        
    
    def update(self, keys, dt):
        self.keys = keys
        self.check_for_input()
        self.dt = dt
        self.tile_x, self.tile_y = self.get_tile_coordinates()
        action_function = self.action_dict[self.action]
        action_function()
        
        # Test - See if tile and rect coords update correctly.
        self.tile_x, self.tile_y = self.get_tile_coordinates()
        xt, yt = self.get_tile_coordinates()
        x, y = self.rect.x, self.rect.y
        print("tile: ", xt, yt)
        print("coord:", x//c.TILE_WIDTH, y//c.TILE_WIDTH, "\n")
    
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
    
                