import constants as c
import states

class GameStatesManager():
    """
    Control class for managing game states.
    """
    def __init__(self):
        self.state_dict = {}
        self.state_name = None
        self.state = None
    
    def setup(self, state_dict, start_state):
        """
        Given a dictionary of States and a State to start in, builds the 
        self.state_dict.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    
    def update(self, window, keys, dt):
        if self.state.done:
            self.flip_state()
        self.state.update(window, keys, dt)
        
    def flip_state(self):
        pass
    

def create_state_dict():
    """
    Creates a dictionary for keeping track of game states.
    """
    state_dict = {c.SANDY_COVE: states.MapState(c.SANDY_COVE)
    }
    
    return state_dict

def create_game_data_dict():
    """
    Creates a dictionary to keep track of game data carried between states 
    and for save game functionality.
    """
    data_dict = {'last_location': None,
    }
    
    return data_dict