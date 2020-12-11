import pygame as pg
import random

import constants as c
from setup import GFX, FONTS

class Sprite(pg.sprite.Sprite):
    """
    Base class for all game sprites. Can be used as is to create stationary 
    sprites. Moving and animation included. 
    Moving has to be initiated in children by overriding update method.
    """
    def __init__(self, sheet_key, x, y, direction='down', action='resting'):
        super().__init__()
        self.name = sheet_key
        self.direction = direction
        self.action = action
        
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
                image.set_colorkey(c.WHITE)
                image_list.append(image)
                
        for key, image in zip(image_keys, image_list):
            image_dict[key] = image
        
        return image_dict    
    
    def create_animation_dict(self, d = None):
        """
        Returns a dictionary of image lists for animation.
        """
        if d is None:
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
        Creates blocker rects to prevent collision with other sprites.
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
            else:
                tile1 = ( x, (y // tw) * tw )
                tile2 = ( x, ((y + tw) // tw ) * tw)
                tile1_rect = pg.Rect(tile1, (tw, tw))
                tile2_rect = pg.Rect(tile2, (tw, tw))
                blockers.extend([tile1_rect, tile2_rect])

        return blockers


class Player(Sprite):
    def __init__(self, x, y, direction):
        super().__init__('player', x, y, direction)

    def update(self, keys, dt):
        self.check_for_input(keys)
        super().update(dt)
        
        if keys[pg.K_LSHIFT]:
            self.speed = 3
        elif keys[pg.K_LCTRL]:
            self.speed = 1
    
    def check_for_input(self, keys):
        if self.action == 'resting':
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.begin_moving('up')
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.begin_moving('down')
            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                self.begin_moving('left')
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.begin_moving('right')


class Wanderer(Sprite):
    def __init__(self, name, x, y, direction):
        super().__init__(name, x, y, direction)
        self.speed = 0.5
        self.moves = ['up', 'down', 'left', 'right']
    
    def update(self, dt):
        if self.action == 'resting':
            self.begin_moving(self.moves[random.randint(0, 3)])
        super().update(dt)


class Mover(Sprite):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.speed = 0.5
        self.moves = ['right', 'right', 'right', 'down', 'down',
                      'left', 'left', 'left', 'up', 'up']
        self.index = 0
        
    def auto_moving(self):
        if self.index > 9:
            self.index = 0
        self.begin_moving(self.moves[self.index])
        self.index += 1
    
    def update(self, dt):
        if self.action == 'resting':
            self.auto_moving()
        super().update(dt)


class Chicken(Sprite):
    def __init__(self, x, y, direction, tiled_id=None):
        super().__init__('chicken_move', x, y, direction)
        self.tiled_id = tiled_id
        self.speed = 0.5
        self.moves = ['up', 'down', 'left', 'right']
        self.rest_sheet_dict = self.create_spritesheet_dict('chicken_rest')
        self.rest_animation_dict = self.create_animation_dict(
            self.rest_sheet_dict)
        self.rested = False
        self.rest_counter = 0

    def auto_moving(self):
        self.begin_moving(self.moves[random.randint(0, 3)])

    def resting(self):
        super().resting()
        self.image_list = self.rest_animation_dict[self.direction]
        
        if self.rest_counter > 63:
            self.rest_counter = 0
            self.rested = True
        
        self.image = self.image_list[self.rest_counter // 16]
        self.rest_counter += 1
        
    def update(self, dt):
        # Probability of moving is 1/125 i.e. 48% per second with 60 FPS.
        if (self.action == 'resting' and random.random() < 0.008
            and self.rested):
            self.auto_moving()
            self.rested = False
        super().update(dt)
        

class MapObject(pg.sprite.Sprite):
    def __init__(self, sheet_key, x, y, frames, frame_width, frame_height, 
                 tiled_id=None):
        super().__init__()
        self.name = sheet_key
        self.tiled_id = tiled_id
        self.image_list = self.create_image_list(
            sheet_key, frames, frame_width, frame_height)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(left=x, top=y)
        self.frames = frames
        self.animation_speed = frames * c.ANIMATION_SPEED
        self.counter = random.randint(0, self.animation_speed)
        
    def create_image_list(self, sheet_key, frames, frame_width, frame_height):
        image_list = []
        sheet = GFX[sheet_key]
        fw = frame_width
        fh = frame_height
        
        for i in range(frames):
            image = pg.Surface([fw, fh])
            image.blit(sheet, (0, 0), (i*fw, 0, fw, fh))
            image.set_colorkey((0, 0, 0))
            image_list.append(image)
        
        return image_list
    
    def update(self):
        if self.counter > self.animation_speed - 1:
            self.counter = 0
        
        image_number = self.counter // (self.animation_speed // self.frames)
        self.image = self.image_list[image_number]
        self.counter += 1


class TextBox(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([240, 80])
        self.clear()
        self.rect = self.image.get_rect(midbottom = (160, 240))
        self.font = pg.font.Font(FONTS['SuperLegendBoy'], 8)
        self.index = 0
        self.line_length = 37
        self.lines = []
        self.active = False
        self.show = False
    
    def give_text(self, text):
        lines_generator = self.get_lines(text, self.line_length)
        self.lines = [line for line in lines_generator]
        self.lines.extend([" ", " "])
    
    def update(self, events):
        if self.active:
            n = len(self.lines)
            lines_in_box = n if n < 3 else 3
            
            self.scroll_text_box(events, n)
            
            for i in range(lines_in_box):
                line = self.font.render(
                    self.lines[i + self.index], True, c.BROWN)
                self.image.blit(
                    line, (c.TILE_WIDTH + 3, (i + 1)*c.TILE_WIDTH + 2))
    
    def scroll_text_box(self, events, n_lines):
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if self.show:
                    if self.index < (n_lines - 3) and n_lines > 5:
                        self.index += 3
                        if self.index > n_lines - 3:
                            self.index = n_lines - 3
                        self.clear()
                    else:
                        self.index = 0
                        self.clear()
                        self.active = False
                        self.show = False
                else:
                    self.show = True
                    self.clear()
                    self.index = 0
    
    def clear(self):
        self.image.blit(GFX['text_box'], (0, 0))
        self.image.set_colorkey(c.WHITE)
    
    def get_lines(self, text, line_length):
        start = 0
        end = 0
        while start + line_length < len(text) and end != -1:
            end = text.rfind(" ", start, start + line_length + 1)
            yield text[start:end]
            start = end + 1
        yield text[start:]
    
    
