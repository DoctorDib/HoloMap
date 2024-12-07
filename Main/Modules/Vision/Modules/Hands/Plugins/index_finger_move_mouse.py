import multiprocessing, pyautogui, requests

from API.Calibration.routes import calibration_routes_app, create_calibration_route
from API.Calibration.sql import CalibrationType
from API.shared_state import BoundaryBoxFactory, HandsFactory, ProjectorBoundaryBoxFactory
from Common.KalmanFilter import KalmanFilter
from Main.Modules.Vision.Modules.Hands.hands_control import HandsControl
from config import Config

class index_finger_move_mouse:
    
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, output: multiprocessing.Queue = None):
        self.shared_state = shared_state
        self.output = output
        
        self.config = Config()
        self.height = self.config.get_int('RESOLUTION_HEIGHT')
        self.width = self.config.get_int('RESOLUTION_WIDTH')
        
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Initialize the Kalman Filter
        self.kalman_filter = KalmanFilter(process_variance=5e-3, measurement_variance=5e-2)

    def run(self):
        with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
        
            with HandsFactory(self.shared_state, read_only=True) as hands_state:
                hands: HandsControl = hands_state.value
                
                finger_tip = hands.get_point("r.index", is_left=False)
                
                if (finger_tip.in_boundaries):
                    # Update Kalman Filter
                    # self.kalman_filter.predict()
                    # self.kalman_filter.update(finger_tip.position)

                    # Get the smoothed estimate from the Kalman Filter
                    # smoothed_position = self.kalman_filter.get_estimate().astype(int)

                    out = boundary_state.value.get_relative_position_from_height_width(self.height, self.width, finger_tip.position)
                    # out = boundary_state.value.get_relative_position_from_height_width(self.height, self.width, finger_tip.position)
                    
                    # Moving PC mouse
                    self.move_pc_mouse(out[0], out[1])
                    
                    # Moving virtual mouse cursor
                    self.output.put({
                        "name": "Moving Virtual Mouse",
                        "tag": "CURSOR_POINT",
                        "data": [out]
                    })
                    
    def move_pc_mouse(self, x: int, y: int):
        with ProjectorBoundaryBoxFactory(self.shared_state, read_only=True) as projector_state:
            # Calculate the mapped width and height of the boundary box
            # top_left, top_right, bottom_left, bottom_right = corners
            boundary_width = projector_state.value.bottom_right[0] - projector_state.value.top_left[0]
            boundary_height = projector_state.value.bottom_right[1] - projector_state.value.top_left[1]
            
            # Calculate the ratio of input coordinates to the projected boundary box
            ratio_x = x / self.width
            ratio_y = y / self.height

            # Map to the projected boundary coordinates
            screen_x = int(projector_state.value.top_left[0] + (ratio_x * boundary_width))
            screen_y = int(projector_state.value.top_left[1] + (ratio_y * boundary_height))

            # Move the mouse cursor
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)