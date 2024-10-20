import multiprocessing, pyautogui
from API.shared_state import BoundaryBoxFactory, HandsFactory
from Common import Plugins
from Modules.Vision.Modules.Hands.hands_control import HandsControl
from config import Config

import time
import multiprocessing

class mouse_click:
    
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, output: multiprocessing.Queue = None):
        self.shared_state = shared_state
        self.output = output
        
        self.config = Config()
        self.height = self.config.get_int('RESOLUTION_HEIGHT')
        self.width = self.config.get_int('RESOLUTION_WIDTH')
        
        # Functional variables
        self.timer = 0
        
        self.click_distance_threshold = 20 # Pixels
        self.click_time_threshold = 1  # Seconds
        self.release_time_threshold = 1  # Seconds
        self.has_clicked = False
        
        # Timestamps for click and release
        self.last_click_time = 0
        self.last_release_time = 0

    def run(self):
        with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
            with HandsFactory(self.shared_state, read_only=True) as hands_state:
                hands: HandsControl = hands_state.value
                
                index_tip = hands.get_point("r.index", is_left=False)
                thumb_tip = hands.get_point('r.thumb', is_left=False)
                
                if (index_tip.in_boundaries and thumb_tip.in_boundaries):
                    distance = hands.check_distance_between_two_points(index_tip, thumb_tip)
                    
                    current_time = time.time()
                    
                    if (distance < self.click_distance_threshold and not self.has_clicked):
                        # Check time since last click
                        if (current_time - self.last_click_time >= self.click_time_threshold):
                            # Mouse click
                            self.has_clicked = True
                            self.last_click_time = current_time  # Update last click time
                            
                            self.mouse_down()
                            
                            # Moving virtual mouse cursor
                            self.output.put({
                                "name": "Mouse is down",
                                "tag": "MOUSE_CLICK",
                                "data": [self.has_clicked]
                            })
                        
                    elif (distance > self.click_distance_threshold):
                        # Check time since last release
                        if (self.has_clicked and (current_time - self.last_release_time >= self.release_time_threshold)):
                            # Mouse release
                            self.has_clicked = False
                            self.last_release_time = current_time  # Update last release time
                            
                            self.mouse_up()

                            # Moving virtual mouse cursor
                            self.output.put({
                                "name": "Mouse is up",
                                "tag": "MOUSE_CLICK",
                                "data": [self.has_clicked]
                            })
                            
    def mouse_down(self):
        if (self.config.get_str('MODE') == 'PRODUCTION'):
            pyautogui.mouseDown()
        
    def mouse_up(self):
        if (self.config.get_str('MODE') == 'PRODUCTION'):
            pyautogui.mouseUp()
