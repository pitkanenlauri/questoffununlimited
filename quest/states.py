class _State():
    """
    Template class for all game states to inherit from.
    """
    def __init__(self):
        self.done = False
        self.game_data = None
        self.next = None
        self.previous = None
    
    def start_up(self, game_data):
        self.game_data = game_data
    
    def cleanup(self):
        return self.game_data
    
    def update(self, surface, keys, dt):
        pass
        
class MapState(_State):
    """
    Main playing state - Handles player movement, sprite updates, 
    resulting interaction and drawing of the map view.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def clean_up(self):
        pass
    
    def update(self, window, keys, dt):
        pass