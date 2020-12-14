import pygame as pg

import constants as c
import sprites as s
from tools import State, Camera, Portal, Dialogue
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
        self.game_data['current_map'] = self.name
        
        self.show_inventory = True
        self.inventory = self.game_data['player_data']
        
        self.tmx_renderer = Renderer(self.tmx_map)
        self.map_image = self.tmx_renderer.render_map()
        self.map_rect = self.map_image.get_rect()
        
        self.camera = Camera(self.map_rect.width, self.map_rect.height)
        self.text_box = s.TextBox()
        
        self.quests = self.open_active_quests()
        
        self.player = self.make_player()
        self.sprites = self.make_sprites()
        self.blockers = self.make_blockers()
        self.portals = self.open_portals()
        self.map_objects = self.make_map_objects()
        self.map_items = self.make_map_items()
        self.dialogues = self.load_dialogues()
        
    def make_player(self):
        layer = self.tmx_renderer.get_layer('start_points')
        
        for obj in layer:
            if obj.name == self.previous:
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
                if self.inventory['chickens']['catch']:
                    if obj.id not in self.inventory['catched_chickens']:
                        sprite = s.Chicken(
                            obj.x, obj.y, obj.properties['direction'], obj.id)
                        sprites.add(sprite)
                else:
                    sprite = s.Chicken(obj.x, obj.y, obj.properties['direction'])
                    sprites.add(sprite)
            
            if obj.name == 'chicken_lost':
                if self.inventory['chickens']['rescue']:
                    if obj.id not in self.inventory['found_items']:
                        sprite = s.Chicken(
                            obj.x, obj.y, obj.properties['direction'], 
                                          obj.id,
                                          obj.properties['color'])
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
        layer = self.tmx_renderer.get_layer('map_items')
        
        for obj in layer:
            if obj.id not in self.inventory['found_items']:
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
    
    def load_dialogues(self):
        dialogues = []
        layer = self.tmx_renderer.get_layer('dialogues')
        
        for obj in layer:
            dialogue = Dialogue(obj.name, obj.x, obj.y, obj.properties)
            dialogues.append(dialogue)
        
        return dialogues
    
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
    
    def check_for_dialogue(self):
        collided = False
        for dialogue in self.dialogues:
            if self.player.rect.colliderect(dialogue.rect):
                # TODO Check for active quests and assign dialogue accordingly.
                self.text_box.active = True
                self.text_box.give_text(dialogue.dict['normal'])
                collided = True
        
        if not collided:
            self.text_box.active = False
            self.text_box.show = False
    
    def make_map_state_dict(self):
        map_state_dict = {'normal': self.running_normally
        }
        return map_state_dict
    
    def update(self, window, keys, dt, events):
        map_state_function = self.map_state[self.state]
        map_state_function(window, keys, dt, events)
    
    def running_normally(self, window, keys, dt, events):
        self.player.update(keys, dt)
        self.sprites.update(dt)
        self.map_objects.update()
        self.map_items.update()
        self.text_box.update(events)
        self.handle_collisions()
        self.check_for_items()
        self.check_for_key_actions(keys)
        self.check_for_dialogue()
        self.check_for_portals()
        self.check_quest_progress()
        self.camera.update(self.player.rect)
        self.update_window(window)
        
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
        
        if self.text_box.show:
            window.blit(self.text_box.image, self.text_box.rect)
        
        new = pg.transform.scale2x(window)
        window.blit(new, (0, 0))
        
        pg.display.flip()
    
    def handle_collisions(self):
        player_collided = False
        collided_sprites = []
        all_sprite_blockers = []
        
        for sprite in self.sprites:
            
            if self.inventory['chickens']['catchable']:
                if self.chicken_catched(sprite):
                    continue
            
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
    
    def check_for_key_actions(self, keys):
        if keys[pg.K_TAB]:
            self.show_inventory = True
        if keys[pg.K_q]:
            self.show_inventory = False
    
    def open_active_quests(self):
        quests = []
        for quest in self.game_data['active_quests']:
            active_quest = self.game_data['quest_data'][quest]
            active_quest.open(self.game_data)
            quests.append(active_quest)
        
        return quests
    
    def check_quest_progress(self):
        for quest in self.quests:
            if quest.active:
                quest.update()
                if not quest.active:
                    self.game_data['active_quests'].remove(quest.name)
                
    def chicken_catched(self, sprite):
        if (sprite.name == 'chicken_move' and self.inventory['chickens']['catch']
            and self.name == c.SANDY_COVE):
            if self.player.rect.colliderect(sprite.rect):
                self.inventory['catched_chickens'].add(sprite.tiled_id)
                self.inventory['chickens']['amount'] += 1
                sprite.kill()
                return True
        
        if (sprite.name == 'red_move' or 
            sprite.name == 'green_move' or sprite.name == 'blue_move'):
            if self.player.rect.colliderect(sprite.rect):
                self.inventory['found_items'].add(sprite.tiled_id)
                self.inventory['chickens']['amount'] += 1
                sprite.kill()
                return True
        
        return False
    
