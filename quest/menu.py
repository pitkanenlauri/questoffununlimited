import pygame as pg
from tmx_renderer import Renderer

from states import MapState
from setup import update_display, play_sfx, TMX, MUSIC, FONTS
from tools import State

from sprites import Sprite, Chicken
import constants as c

class MainMenu(MapState):
    def __init__(self, name):
        State.__init__(self)
        self.name = name
        self.tmx_map = TMX[name]
        self.previous_music = None
        self.music_title = 'intro'
        self.music = MUSIC[self.music_title]
        self.volume = 1.0

    def start_up(self, game_data):
        self.game_data = game_data
        self.music, self.volume = self.set_music()

        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()

        self.selector = self.make_selector()
        self.blockers = self.make_blockers()
        self.menu_sprites = self.make_menu_sprites()

    def make_selector(self):
        layer = self.tmx_renderer.get_layer('start_points')
        
        for obj in layer:
            if obj.name == 'start':
                selector = Selector(obj.x, obj.y)
                return selector

    def make_menu_sprites(self):
        menu_sprites = pg.sprite.Group()
        layer = self.tmx_renderer.get_layer('sprites')

        for obj in layer:
            if obj.name == 'chicken':
                chicken = Chicken(obj.x, obj.y, 'down', color='red')
                menu_sprites.add(chicken)
        
        return menu_sprites

    def clean_up(self):
        return State.clean_up(self)
    
    def update(self, window, keys, dt, events):
        self.selector.update(events, dt)
        self.menu_sprites.update(dt)
        for blocker in self.blockers:
            if self.selector.rect.colliderect(blocker):
                self.selector.begin_resting()
            for sprite in self.menu_sprites:
                if sprite.rect.colliderect(blocker):
                    sprite.begin_resting()
        
        self.draw(window)
        update_display(window)

        if self.selector.start_game:
            self.next = c.TRANQUIL_CABIN
            self.done = True
    
    def draw(self, window):
        window.fill(c.BLACK)
        window.blit(self.selector.image, self.selector.rect)

        for sprite in self.menu_sprites:
            window.blit(sprite.image, sprite.rect)
        
        self.draw_title(window)
        self.draw_menu(window)

    def draw_title(self, window):
        font = pg.font.Font(FONTS['SuperLegendBoy'], 16)
        title_text = c.CAPTION
        top_x = self.get_top_x(title_text, 16)
        title = font.render(title_text, True, c.WHITE)
        window.blit(title, (top_x, 48))
    
    def draw_menu(self, window):
        font = pg.font.Font(FONTS['SuperLegendBoy'], 8)
        line1_text = 'Start a new game !'
        line1_top_x = self.get_top_x(line1_text, 8)
        line1 = font.render(line1_text, True, c.WHITE)
        window.blit(line1, (line1_top_x, 100))

        line2_text = 'Load game'
        line2_top_x = self.get_top_x(line2_text, 8)
        line2 = font.render(line2_text, True, c.WHITE)
        window.blit(line2, (line2_top_x, 116))

        line3_text = 'Exit'
        line3_top_x = self.get_top_x(line3_text, 8)
        line3 = font.render(line3_text, True, c.WHITE)
        window.blit(line3, (line3_top_x, 132))

    def get_top_x(self, text, font_size):
        font = pg.font.Font(FONTS['SuperLegendBoy'], font_size)
        size = font.size(text)
        return (c.WINDOW_SIZE[0] - size[0]) // 2


class Selector(Sprite):
    def __init__(self, x, y):
        super().__init__('selector', x, y)
        self.speed = 2
        self.start_game = False
    
    def update(self, events, dt):
        self.check_for_input(events)
        super().update(dt)
    
    def check_for_input(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.begin_moving('down')
                    play_sfx('select', 0.5)
                elif event.key == pg.K_UP:
                    self.begin_moving('up')
                    play_sfx('select', 0.5)
                elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.start_game = True

