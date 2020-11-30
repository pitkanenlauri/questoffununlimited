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
        
        # Make these in start_up()
        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()
        
        self.camera = Camera(self.map_rect.width, self.map_rect.height)
        
        # Test
        self.all_sprites = pg.sprite.Group()
        
        self.player = Player(13*16, 9*16, 'resting', 'down')
        self.all_sprites.add(self.player)
        
        self.square = Wanderer('player', 22*16, 13*16)
        self.all_sprites.add(self.square)

    def update(self, window, keys, dt):
        
        # Test
        self.player.update(keys, dt)
        self.square.update(dt)
        
        self.camera.update(self.player.rect)
        
        window.blit(self.map_image, self.camera.apply(self.map_rect))
        
        for sprite in self.all_sprites:
            window.blit(sprite.image, self.camera.apply(sprite.rect))
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))

        pg.display.flip()
        
