import pygame as pg

from sprites import Player 
from tools import _State

class MapState(_State):
    """
    Main playing state - Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        
        # Test
        self.player = Player(0, 0, 'resting', 'down')
    
    def update(self, window, keys, dt):
        self.player.update(keys, dt)
        window.fill((0,0,0))
        window.blit(self.player.image, self.player.rect)
        pg.display.flip()
        