import multiprocessing
import logger
import os
import cv2

import mediapipe as mp

from flask import Flask
from multiprocessing import Queue

from Common.ModuleHelper import ModuleHelper
from Common.Plugins import PluginLoader
from Main.Modules.Vision.Modules.Hands.hands_control import FingerPoint, HandsControl
from API.shared_state import BoundaryBoxFactory, CameraFactory, DebugModeFlagFactory, HandsFactory

class Hands_Module(ModuleHelper):
    def __init__(self, memory_name: str, parent_module_name: str, image_shape, app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None,  module_path: str = ""):
        super().__init__("Hands", parent_module_name, parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state, module_path=module_path)

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        self.image_shape = image_shape
        self.frame = None

    def prep(self):
        root_path = os.path.dirname(__file__)
        self.plugin_manager = PluginLoader(root_path, self.shared_state, self.output)
        self.plugin_manager.monitor_plugins() # Watching for new or removed plugins

        with HandsFactory(self.shared_state) as hands_state:
            hands_state.value = HandsControl()
            hands: HandsControl = hands_state.value

            # Left hand
            hands.register_point("l.thumb", 4, is_left=True)
            hands.register_point("l.index", 8, is_left=True)
            hands.register_point("l.middle", 12, is_left=True)
            hands.register_point("l.ring", 16, is_left=True)
            hands.register_point("l.pinky", 20, is_left=True)

            # Right hand
            hands.register_point("r.thumb", 4, is_left=False)
            hands.register_point("r.index", 8, is_left=False)
            hands.register_point("r.middle", 12, is_left=False)
            hands.register_point("r.ring", 16, is_left=False)
            hands.register_point("r.pinky", 20, is_left=False)

        # Setting up detector
        self.mp_hands = mp.solutions.hands
        self.detector = self.mp_hands.Hands()
        
        # self.detector = FindHands()
        super().prep()

    # Called from the main thread
    def run(self):
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                should_run = self.common_run()
                if (not should_run):
                    continue
                
                try:
                    img = self.receive_image()

                    if img is None:
                        continue

                    # Prepping image 
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
                    # Find hands
                    hands = self.detector.process(img)
                    multi_hands = hands.multi_hand_landmarks
                    multi_handedness = hands.multi_handedness
                    
                    if (hands is None or multi_hands is None or multi_handedness is None):
                        # No hands detected
                        continue
                    
                    with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
                    
                        with HandsFactory(self.shared_state) as hands_state:
                            if (hands_state.value is None):
                                continue
                        
                            # Looping through detected hands
                            for idx, hand_landmarks in enumerate(multi_hands):
                                # HACK: This is a quick fix to swap left and right hand... for some reason
                                #       it is the opposite way around, which might be something to do with
                                #       the mirroring of the camera, maybe?
                                is_left = multi_handedness[idx].classification[0].label == 'Right' 
                                
                                for finger_point in hands_state.value.points_dict.values():
                                    finger_point: FingerPoint = finger_point
                                    
                                    if (finger_point.is_left != is_left):
                                        continue
                                    
                                    image_height, image_width, _ = img.shape
                                    
                                    # # Get the position of the finger tip (key point)
                                    point_position = hand_landmarks.landmark[finger_point.id]
                                    x = point_position.x * image_width
                                    y = point_position.y * image_height
                                    
                                    # # Saving new point position
                                    finger_point.set_position((x,y))
                                    finger_point.in_boundaries = boundary_state.value.is_in_boundary(x, y)
                                    
                        # Do any actions based on finger position
                        self.plugin_manager.run_through_plugins()
                        
                        with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                            if (flag_state.value):
                                
                                with HandsFactory(self.shared_state) as hands_state:
                                    if (hands_state.value is None):
                                        continue
                                    
                                    for point in hands_state.value.points_dict.values():
                                        if not point.in_boundaries:
                                            continue
                                        
                                        center = (int(point.position[0]), int(point.position[1]))
                                        radius = 5
                                        color = (0, 255, 0) if point.is_left else (255, 0, 0)
                                        thickness = -1

                                        # Draw the circle on the image
                                        cv2.circle(img, center, radius, color, thickness)
                                    
                                with CameraFactory("hands_camera", self.shared_state) as camera_state:
                                    camera_state.update(boundary_state.value.draw_boundary(img))
                                    
                except Exception as e:
                    logger.error("Hands Module Error:", e)
        finally:
            cv2.destroyAllWindows()
