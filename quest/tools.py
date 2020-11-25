class GameStatesManager:
    """
    Control class for managing game states.
    """
    def __init__(self):
        self.state_dict = {}
        self.state_name = None
        self.state = None
    
    def setup(self, state_dict, start_state):
        """
        Given a dictionary of states and a state to start in, builds the 
        self.state_dict.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    
    def update(self, window, keys, dt):
        """
        Checks if a state is done. Changes state if necessary 
        and state.update is called.
        """
        if self.state.done:
            self.flip_state()
        self.state.update(window, keys, dt)
        
    def flip_state(self):
        """
        Changes to a new state and performs cleanup for exiting state 
        and startup for new state. (Most importantly passing on game data.)
        """
        previous, self.state_name = self.state_name, self.state.next
        game_data = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
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
    Creates a dictionary of game data to be carried 
    between states and for save game functionality.
    """
    data_dict = {'last_location': None,
    }
    return data_dict