import pygame as pg

from sprites import Player, Sprite
from tools import _State

class MapState(_State):
    """
    Main playing state. Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        
        # Test
        self.all = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        
        self.player = Player(0, 0, 'resting', 'down')
        self.all.add(self.player)
        
        self.obstacle = Sprite('obstacle', 80, 80)
        self.obstacles.add(self.obstacle)
        self.all.add(self.obstacle)
        
        self.grid = pg.sprite.Sprite()
        self.grid.image = pg.image.load('grid.png').convert_alpha()
        self.grid.rect = self.grid.image.get_rect(left=0, top=0)
    
    def update(self, window, keys, dt):
        
        # Test
        self.player.update(keys, dt)
        self.obstacles.update(dt)
        
        if pg.sprite.spritecollideany(self.player, self.obstacles):
            #self.player.action = 'resting'
            # TODO - collisions like before?
            pass
        
        window.fill((0, 0, 0))
        window.blit(self.grid.image, self.grid.rect)
        for sprite in self.all:
            window.blit(sprite.image, sprite.rect)
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        pg.display.flip()
        