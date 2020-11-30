import pygame as pg

import pytmx

class TiledRenderer:
    """
    Renders tile map made in Tiled to pygame surface using pytmx library.
    """
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.map_width = tm.width * tm.tilewidth
        self.map_height = tm.height * tm.tileheight
        self.tmx_data = tm
    
    def render_map(self):
        surface = pg.Surface((self.map_width, self.map_height))
        
        if self.tmx_data.background_color:
            surface.fill(pg.Color(self.tmx_data.background_color))
        
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_tile_layer(surface, layer)
        
        return surface
    
    def render_tile_layer(self, surface, layer):
        """ 
        Renders all TiledTiles in this layer.
        """
        # Dereference these heavily used references for speed.
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit
        
        # Iterate over the tiles in the layer, and blit them.
        for x, y, image in layer.tiles():
            surface_blit(image, (x * tw, y * th))