import pygame as pg

import constants as c
import sprites as s
from tools import State, Camera, Portal
from setup import TMX, GFX, FONTS
from tmx_renderer import Renderer

class MapState(State):
    """
    Main playing state. Handles creation of map, sprites and objects from
    tmx data, manages their interactions and draws & updates game window.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.tmx_map = TMX[name]
        self.font = pg.font.Font(FONTS['SuperLegendBoy'], 8)
    
    def start_up(self, game_data):
        self.game_data = game_data
        self.state = 'normal'
        self.map_state = self.make_map_state_dict()
        
        self.show_inventory = True
        self.inventory = self.game_data['player_inventory']
        
        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()
        self.camera = Camera(self.map_rect.width, self.map_rect.height)

        self.player = self.make_player()
        self.sprites = self.make_sprites()
        self.blockers = self.make_blockers()
        self.portals = self.open_portals()
        self.map_objects = self.make_map_objects()
        self.map_items = self.make_map_items()
    
    def make_player(self):
        layer = self.tmx_renderer.get_layer('start_points')
        
        for obj in layer:
            if obj.name == self.previous:
                player = s.Player(obj.x, obj.y, obj.properties['direction'])
            
            if obj.name == 'start':
                player = s.Player(obj.x, obj.y, obj.properties['direction'])

        return player
    
    def make_sprites(self):
        sprites = pg.sprite.Group()
        layer = self.tmx_renderer.get_layer('sprites')
        
        for obj in layer:
            if obj.name == "wanderer":
                sprite = s.Wanderer(
                    'player_f', obj.x, obj.y, obj.properties['direction'])
                sprites.add(sprite)
            
            if obj.name == 'mover':
                sprite = s.Mover('uncle', obj.x, obj.y)
                sprites.add(sprite)

            if obj.name == 'chicken':
                sprite = s.Chicken(obj.x, obj.y, obj.properties['direction'])
                sprites.add(sprite)
                
            if obj.name == 'uncle':
                sprite = s.Sprite(obj.name, obj.x, obj.y)
                sprites.add(sprite)
        
        return sprites
    
    def make_blockers(self):
        blockers = []
        layer = self.tmx_renderer.get_layer('blockers')
        
        for obj in layer:
            blocker = pg.Rect(obj.x, obj.y, c.TILE_WIDTH, c.TILE_WIDTH)
            blockers.append(blocker)
        
        return blockers
    
    def make_map_objects(self):
        map_objects = pg.sprite.Group()
        layer = self.tmx_renderer.get_layer('map_objects')
        
        for obj in layer:
            map_object = s.MapObject(
                obj.name, obj.x, obj.y, obj.properties['frames'], 
                                        obj.properties['frame_width'],
                                        obj.properties['frame_height'])
            map_objects.add(map_object)
        
        return map_objects
    
    def make_map_items(self):
        map_items = pg.sprite.Group()
        found_items = self.inventory['found_items']
        layer = self.tmx_renderer.get_layer('map_items')
        
        for obj in layer:
            if obj.id not in found_items:
                item = s.MapObject(
                    obj.name, obj.x, obj.y, obj.properties['frames'], 
                                            obj.properties['frame_width'],
                                            obj.properties['frame_height'],
                                            obj.id)
                map_items.add(item)
        
        return map_items
    
    def open_portals(self):
        portals = []
        layer = self.tmx_renderer.get_layer('portals')
        
        for obj in layer:
            portal = Portal(obj.name, obj.x, obj.y)
            portals.append(portal)
        
        return portals
    
    def check_for_portals(self):
        for portal in self.portals:
            if self.player.rect.colliderect(portal.rect):
                self.next = portal.name
                self.done = True
    
    def check_for_items(self):
        found_items = self.inventory['found_items']
        
        for item in self.map_items:
            if self.player.rect.colliderect(item.rect):
                if item.name == 'coin':
                    found_items.add(item.tiled_id)
                    self.inventory['gold'] += 1
                    item.kill()
            
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
        self.check_for_items()
        self.camera.update(self.player.rect)
        self.map_objects.update()
        self.map_items.update()
        self.check_key_actions(keys)
        self.update_window(window)
        self.check_for_portals()

    def update_window(self, window):
        window.blit(self.map_image, self.camera.apply(self.map_rect))
        
        for obj in self.map_objects:
            window.blit(obj.image, self.camera.apply(obj.rect))
        
        for item in self.map_items:
            window.blit(item.image, self.camera.apply(item.rect))
        
        window.blit(self.player.image, self.camera.apply(self.player.rect))
        
        for sprite in self.sprites:
            window.blit(sprite.image, self.camera.apply(sprite.rect))
        
        if self.show_inventory:
            self.draw_inventory(window)
        
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
    
    def draw_inventory(self, window):
        tw = c.TILE_WIDTH
        i = 0 # Inventory slot index from top down.
        x, y = 2, 3 # Text x and y offsets.
        
        window.blit(GFX['gold'], (0, i * tw))
        coin_amount = self.font.render(
            'x' + str(self.inventory['gold']), True, c.WHITE)
        window.blit(coin_amount, (tw + x, (i * tw)+ y))
        i += 1
        
        if self.inventory['chickens']['show']:
            window.blit(GFX['chickens'], (0, i * tw))
            chickens_catched = self.font.render(
                str(self.inventory['chickens']['amount']) + '/' + 
                str(self.inventory['chickens']['max']), True, c.WHITE)
            window.blit(chickens_catched, (tw + x, (i * tw) + y))
            i += 1
    
    def check_key_actions(self, keys):
        if keys[pg.K_TAB]:
            self.show_inventory = True
        if keys[pg.K_q]:
            self.show_inventory = False


class ChickenCatch(MapState):
    def __init__(self, name):
        super().__init__(name)
    
    def start_up(self, game_data):
        super().start_up(game_data)
        self.chickens_catched = (
            game_data['quest_data']['chicken_catch']['chickens_catched'])
        self.make_chickens()
        
    def make_chickens(self):
        max_chickens = 0
        layer = self.tmx_renderer.get_layer('runaway_chickens')
        
        for obj in layer:
            max_chickens += 1
            if obj.id not in self.chickens_catched:
                chicken = s.Chicken(obj.x, obj.y, obj.properties['direction'],
                                  obj.id)
                self.sprites.add(chicken)
                
        self.inventory['chickens']['max'] = max_chickens
    
    def handle_collisions(self):
        for sprite in self.sprites:
            if sprite.name == 'chicken_move':
                if self.player.rect.colliderect(sprite.rect):
                    self.chickens_catched.add(sprite.tiled_id)
                    self.inventory['chickens']['amount'] += 1
                    sprite.kill()
        
        super().handle_collisions()
    

