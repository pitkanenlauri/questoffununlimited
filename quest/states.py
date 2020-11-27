import pygame as pg

from sprites import Player, Sprite, Square
from tools import State, Camera

class MapState(State):
    """
    Main playing state. Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.camera = Camera(320, 240) # 320 240 = test grid.png dimensions
        
        # Test
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        
        self.player = Player(16, 16, 'resting', 'down')
        self.all_sprites.add(self.player)
        
        self.square = Square('square', 160, 96)
        self.all_sprites.add(self.square)
        
        for i in range(10):
            obstacle = Sprite('obstacle_blue', 80 + i*16, 80)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
        
        for i in range(5):
            obstacle = Sprite('obstacle_green', 80 + i*16, 112)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)

        for i in range(5):
            obstacle = Sprite('obstacle_yellow', 176, 96 + i*16)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
        
        self.grid = pg.sprite.Sprite()
        self.grid.image = pg.image.load('grid.png').convert_alpha()
        self.grid.rect = self.grid.image.get_rect(left=0, top=0)
    
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
        
        window.fill((0, 0, 0))
        window.blit(self.grid.image, self.camera.apply(self.grid))
        
        for sprite in self.all_sprites:
            window.blit(sprite.image, self.camera.apply(sprite))
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        pg.display.flip()
        