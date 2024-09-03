from multiprocessing import Manager

from Modules.Vision.BoundaryBox import BoundaryBox

class SharedStateManager:
    def __init__(self, manager):
        self.shared_state = manager.dict()

        # Presets - not really needed but keeping just in case
        self.shared_state['debug_mode'] = False

        self.shared_state['boundary_box'] = BoundaryBox()

        # Calibration specifics
        self.shared_state['calibration_flag'] = False
        self.shared_state['boundary_box_reset'] = False

    def get_shared_state(self):
        """
        Recieve the shared state dictionary
        """
        return self.shared_state
    
    def set_state(self, key, value):
        """
        Setting a value with a key in a shared state dictionary
        """
        self.shared_state[key] = value

    def get_state(self, key):
        """
        Getting a value with a key in a shared state dictionary
        """
        return self.shared_state[key]