class GameStatesManager:
    """
    Control class for managing game states.
    """
    def __init__(self):
        self.sprite_state_dict = {}
        self.state_name = None
        self.state = None
    
    def setup(self, state_dict, start_state):
        """
        Given a dictionary of States and a State to start in, builds the 
        self.sprite_state_dict.
        """
        self.sprite_state_dict = state_dict
        self.state_name = start_state
        self.state = self.sprite_state_dict[self.state_name]
    
    def update(self, window, keys, dt):
        """
        Checks if a state is done. State is flipped if necessary 
        and state.update is called.
        """
        if self.state.done:
            self.flip_state()
        self.state.update(window, keys, dt)
        
    def flip_state(self):
        """
        Changes current state and performs cleanup for exiting state and 
        startup for new state.
        """
        previous, self.state_name = self.state_name, self.state.next
        game_data = self.state.cleanup()
        self.state = self.sprite_state_dict[self.state_name]
        self.state.startup(game_data)
        self.state.previous = previous
        
class _State:
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
        self.done = False
        return self.game_data
    
    def update(self, surface, keys, dt):
        """
        Update function for state. Must be overloaded in children.
        """
        pass
    

def create_game_data_dict():
    """
    Creates a dictionary to keep track of game data carried between states 
    and for save game functionality.
    """
    data_dict = {'last_location': None,
    }
    return data_dict