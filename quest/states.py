import pygame as pg

from sprites import Player, Wanderer
from tools import State, Camera
from setup import TMX
from tmx_renderer import Renderer

class MapState(State):
    """
    Main playing state. Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.tmx_map = TMX[name]
        
        # Test
        self.all_sprites = pg.sprite.Group()
        self.square = Wanderer('player', 22*16, 13*16)
        self.all_sprites.add(self.square)
    
    def start_up(self, game_data):
        self.game_data = game_data
        self.state = 'normal'
        
        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()
        
        self.camera = Camera(self.map_rect.width, self.map_rect.height)
        
        self.map_state = self.make_map_state_dict()

        # Test
        self.player = self.make_player()
    
    def make_player(self):
        layer = self.tmx_renderer.tmx_data.get_layer_by_name('Object_Layer_1')
        for obj in layer:
            if obj.name == "start point":
                player = Player(obj.x, obj.y, 'resting', obj.properties['direction'])

        return player
    
    def make_sprites(self):
        pass
    
    def make_blockers(self):
        pass
    
    def make_map_state_dict(self):
        map_state_dict = {'normal': self.running_normally
        }
        return map_state_dict
    
    def update(self, window, keys, dt):
        map_state_function = self.map_state[self.state]
        map_state_function(window, keys, dt)    
    
    def running_normally(self, window, keys, dt):
        self.player.update(keys, dt)
        self.square.update(dt)        
        self.camera.update(self.player.rect)
        self.update_window(window)

    def update_window(self, window):
        window.blit(self.map_image, self.camera.apply(self.map_rect))
        window.blit(self.player.image, self.camera.apply(self.player.rect))
        
        for sprite in self.all_sprites:
            window.blit(sprite.image, self.camera.apply(sprite.rect))
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        
        pg.display.flip()
        
    
