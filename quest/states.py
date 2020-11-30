import pygame as pg

import constants as c
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
    
    def start_up(self, game_data):
        self.game_data = game_data
        self.state = 'normal'
        
        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()
        
        self.camera = Camera(self.map_rect.width, self.map_rect.height)
        
        self.map_state = self.make_map_state_dict()

        self.player = self.make_player()
        self.sprites = self.make_sprites()
        self.blockers = self.make_blockers()
    
    def make_player(self):
        layer = self.tmx_renderer.get_layer('sprite_info')
        for obj in layer:
            if obj.name == "start point":
                player = Player(
                    obj.x, obj.y, 'resting', obj.properties['direction'])

        return player
    
    def make_sprites(self):
        sprites = pg.sprite.Group()
        
        layer = self.tmx_renderer.get_layer('sprite_info')
        for obj in layer:
            if obj.name == "sprite":
                sprite = Wanderer(
                    'player', obj.x, obj.y, obj.properties['direction'])
                sprites.add(sprite)
        
        return sprites
    
    def make_blockers(self):
        blockers = []
        
        layer = self.tmx_renderer.get_layer('blockers')
        for obj in layer:
            blocker = pg.Rect(obj.x, obj.y, c.TILE_WIDTH, c.TILE_WIDTH)
            blockers.append(blocker)
        
        return blockers
    
    def make_map_state_dict(self):
        map_state_dict = {'normal': self.running_normally
        }
        return map_state_dict
    
    def update(self, window, keys, dt):
        map_state_function = self.map_state[self.state]
        map_state_function(window, keys, dt)    
    
    def running_normally(self, window, keys, dt):
        self.player.update(keys, dt)
        self.sprites.update(dt)      
        self.handle_collisions()  
        self.camera.update(self.player.rect)
        self.update_window(window)

    def update_window(self, window):
        window.blit(self.map_image, self.camera.apply(self.map_rect))
        window.blit(self.player.image, self.camera.apply(self.player.rect))
        
        for sprite in self.sprites:
            window.blit(sprite.image, self.camera.apply(sprite.rect))
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        
        pg.display.flip()
    
    def handle_collisions(self):
        player_collided = False
        collided_sprites = []
        all_sprite_blockers = []
        
        for sprite in self.sprites:
            all_sprite_blockers.extend(sprite.blockers)
        
        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                player_collided = True
        
        for blocker in all_sprite_blockers:
            if self.player.rect.colliderect(blocker):
                player_collided = True
        
        if player_collided:
            self.player.begin_resting()
        
        for sprite in self.sprites:
            for blocker in self.blockers:
                if sprite.rect.colliderect(blocker):
                    collided_sprites.append(sprite)
            if sprite.rect.colliderect(self.player.rect):
                collided_sprites.append(sprite)
            sprite.kill()
            if pg.sprite.spritecollideany(sprite, self.sprites):
                collided_sprites.append(sprite)
            self.sprites.add(sprite)
        
        for sprite in collided_sprites:
            sprite.begin_resting()
        
        