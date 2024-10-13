import multiprocessing
from API.shared_state import BoundaryBoxFactory, HandsFactory
from Common import Plugins
from Modules.Vision.Modules.Hands.hands_control import HandsControl
from config import Config

class index_finger_move_mouse:
    
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, output: multiprocessing.Queue = None):
        self.shared_state = shared_state
        self.output = output
        
        self.config = Config()
        self.height = self.config.get_int('RESOLUTION_HEIGHT')
        self.width = self.config.get_int('RESOLUTION_WIDTH')

    def run(self):
        with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
        
            with HandsFactory(self.shared_state, read_only=True) as hands_state:
                hands: HandsControl = hands_state.value
                
                finger_tip = hands.get_point("r.index", is_left=False)
                
                if (finger_tip.in_boundaries):
                    # Update Kalman Filter
                    # self.kalman_filter.predict()
                    # self.kalman_filter.update(finger_tip)

                    # Get the smoothed estimate from the Kalman Filter
                    # smoothed_position = self.kalman_filter.get_estimate().astype(int)

                    # out = boundary_state.value.get_relative_position(img, smoothed_position)
                    out = boundary_state.value.get_relative_position_from_height_width(self.height, self.width, finger_tip.position)
                    
                    # Moving virtual mouse cursor
                    self.output.put({
                        "name": "Moving Virtual Mouse",
                        "tag": "CURSOR_POINT",
                        "data": [out]
                    })