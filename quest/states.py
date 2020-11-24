from tools import _State

class MapState(_State):
    """
    Main playing state - Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def update(self, window, keys, dt):
        pass