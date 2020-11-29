import pygame as pg

from sprites import Player, Sprite, Wanderer
from tools import State, Camera

class MapState(State):
    """
    Main playing state. Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.camera = Camera(640, 480) # Change to map width and height
        
        # Test
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        
        self.player = Player(16, 16, 'resting', 'down')
        self.all_sprites.add(self.player)
        
        self.square = Wanderer('player', 160, 96)
        self.all_sprites.add(self.square)
        
        for i in range(10):
            obstacle = Sprite('red', 80 + i*16, 80)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
        
        for i in range(5):
            obstacle = Sprite('green', 80 + i*16, 112)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)

        for i in range(5):
            obstacle = Sprite('blue', 176, 96 + i*16)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
        

    def update(self, window, keys, dt):
        
        # Test
        self.player.update(keys, dt)
        self.square.update(dt)
        self.obstacles.update(dt)
        
        if pg.sprite.spritecollideany(self.player, self.obstacles):
            self.player.begin_resting()
        
        if pg.sprite.spritecollideany(self.square, self.obstacles):
            self.square.begin_resting()
        
        self.camera.update(self.player.rect)
        
        window.fill((135, 206, 235))
        
        for sprite in self.all_sprites:
            window.blit(sprite.image, self.camera.apply(sprite))
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        pg.display.flip()
        