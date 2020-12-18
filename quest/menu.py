import pygame as pg
from tmx_renderer import Renderer

from states import MapState
from setup import MUSIC
from tools import State

from sprites import Sprite
import constants as c

class MainMenu(MapState):
    def __init__(self, name):
        super().__init__(name)
        self.music = MUSIC['intro']
        self.music_title = 'intro'
        self.volume = 1.0

    def start_up(self, game_data):
        self.game_data = game_data
        self.music, self.volume = self.set_music()

        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()

        self.player = self.make_selector()
        self.blockers = self.make_blockers()

    def make_selector(self):
        layer = self.tmx_renderer.get_layer('start_points')
        
        for obj in layer:
            if obj.name == 'start':
                selector = Selector(obj.x, obj.y)
                return selector

    def clean_up(self):
        return State.clean_up(self)
    
    def update(self, window, keys, dt, events):
        self.player.update(events, dt)
        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                self.player.begin_resting()
        window.fill(c.BLACK)
        window.blit(self.player.image, self.player.rect)
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        
        pg.display.flip()

        if self.player.go:
            self.next = c.SANDY_COVE
            self.done = True


class Selector(Sprite):
    def __init__(self, x, y):
        super().__init__('selector', x, y)
        self.speed = 3
        self.go = False
    
    def update(self, events, dt):
        self.check_for_input(events)
        super().update(dt)
    
    def check_for_input(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.begin_moving('down')
                elif event.key == pg.K_UP:
                    self.begin_moving('up')
                elif event.key == pg.K_RETURN:
                    self.go = True

    def do_step(self):
        # selector sound
        pass

