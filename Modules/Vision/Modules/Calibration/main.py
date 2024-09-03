from multiprocessing import Queue
import multiprocessing
import multiprocessing.managers
from time import sleep
from flask import Flask

import cv2
import logger

import numpy as np

from Common.ModuleHelper import ModuleHelper
from Modules.Vision.BoundaryBox import BoundaryBox

class Calibration_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape=(1080, 1920, 3), app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        super().__init__("Calibration", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.image_shape= image_shape

        self.frame = None


        # Controlling the UI red marker box
        # 0 = top left
        # 1 = top right
        # 2 = bottom right
        # 3 = bottom left
        self.marker_position: int = 0


        # Define the BGR color for red
        target_bgr = np.array([0, 0, 255], dtype=np.uint8)

        # Define the HSV range for detecting the specific red color
        # Red color can be in two ranges due to the hue wrap-around in HSV color space
        tolerance = 4  # Adjust this value for sensitivity

        # Lower red range (0-10 degrees on the Hue scale)
        self.red_lower1 = np.array([0, 120, 70])
        self.red_upper1 = np.array([tolerance, 255, 255])

        # Upper red range (170-180 degrees on the Hue scale)
        self.red_lower2 = np.array([180 - tolerance, 120, 70])
        self.red_upper2 = np.array([180, 255, 255])

        # Red colour detection range
        # self.red_lower = np.array([35, 50, 50])
        # self.red_upper = np.array([85, 255, 255])

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        self.kernal = np.ones((5, 5), "uint8")

        self.count = 0
        self.max_count = 3

        self.total_loop = 0

    def set_up_frame(self):
        # Ensure the buffer is large enough for the image
        buffer_size = np.prod(self.image_shape)
        if len(self.parent_memory.buf) < buffer_size:
            raise ValueError("Buffer size is too small for the image. Ensure the shared memory size is correct.")

        self.frame = np.ndarray((1080, 1920, 3), dtype=np.uint8, buffer=self.parent_memory.buf)
        logger.info(f"Attempting to set up Camera")
        
        return self.frame
    
    def receive_image(self):
        if self.frame is not None and self.frame.size > 0 and not np.all(self.frame) and np.any(self.frame):
            return self.frame
        else:
            self.set_up_frame()
            return None

    # Called from the main thread
    def run(self):
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                # Helps preventing overflow!
                sleep(1)

                # Waiting for the calibration to be set
                if (not self.shared_state['calibration_flag']):
                    continue

                if (not self.shared_state['boundary_box_reset']):
                    self.shared_state['boundary_box_reset'] = True
                    ##  Resetting boundary box
                    self.shared_state['boundary_box'] = BoundaryBox()

                try:
                    boundary: BoundaryBox = self.shared_state['boundary_box']

                    sleep(.25)
                    img = self.receive_image()

                    if img is None:
                        continue

                    img = self.process_frame(img)
                    if (img is None):
                        continue

                    if (boundary.has_all_points()):
                        self.shared_state['boundary_box_reset'] = False # Resetting flag to reset
                        self.shared_state['calibration_flag'] = False # Disabling calibration
                        self.complete_calibration()

                        logger.info("Calibration complete")

                    if (self.shared_state['debug_mode']):
                        # Drawing broundaries
                        img = boundary.draw_boundary(img)

                        cv2.imshow("Calibration", img)
                        cv2.waitKey(1)
                except Exception as e:
                    logger.error("Calibration Error: ", e)
        finally:
            cv2.destroyAllWindows()

    def new_calibration(self):
        self.shared_state['boundary_box'] = BoundaryBox()
        self.marker_position = 0
        # Sending marker to the top left position
        self.send_marker_to_position(self.marker_position)

    def process_frame(self, frame):

        # detect red box
        coords_and_size = self.detect_red_box(frame)
        if (coords_and_size is None):
            # If not successful, try it again!
            return None

        # Process coords
        success = self.process_coords(coords_and_size)
        if (not success):
            # If not successful, try it again!
            return None

        # Can only go between 0 and 3
        if (self.marker_position < 3):
            self.marker_position += 1
        else:
            self.marker_position = 0

        # Moving marker
        self.send_marker_to_position(self.marker_position)

        return frame

    def detect_red_box(self, frame) -> any:
        # Convert the imageFrame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Apply red mask
        # Create masks for both red ranges
        mask1 = cv2.inRange(hsv_frame, self.red_lower1, self.red_upper1)
        mask2 = cv2.inRange(hsv_frame, self.red_lower2, self.red_upper2)
        
        # Combine masks
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Creating contour to track red color
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contours) <= 0):
            return None

        largest_contour = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(largest_contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Drawing them out
            frame = cv2.circle(frame, (x, y), 10, (255, 0, 255), 2)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            return ((x, y), (w, h))
        
        # If we have reached this point then something has gone wrong
        return None

    def process_coords(self, coords_and_size: any) -> bool:
        """
        The coordinates are always based on the top left corner of the red marker
        """

        # TODO - Implement a cycle property to go through the calibration process x times
        # TODO - Implement an average which uses the cycle 

        try:
            marker_x = coords_and_size[0][0]
            marker_y = coords_and_size[0][1]
            marker_width = coords_and_size[1][0]
            marker_height = coords_and_size[1][1]


            boundary: BoundaryBox = self.shared_state['boundary_box']

            # Top left condition
            if (self.marker_position == 0):
                boundary.top_left = (marker_x, marker_y)
            # Top right conditionv
            elif (self.marker_position == 1):
                x = marker_x + marker_width
                y = marker_y
                boundary.top_right = (x, y)
            # Bottom right condition
            elif (self.marker_position == 2):
                x = marker_x + marker_width
                y = marker_y + marker_height
                boundary.bottom_right = (x, y)
            # Bottom left condition
            elif (self.marker_position == 3):
                x = marker_x
                y = marker_y + marker_height
                boundary.bottom_left = (x, y)

            self.shared_state['boundary_box'] = boundary
            return True
        except Exception as ex:
            print("<<<<<<", ex)
            logger.error("Error processing coords: " + ex)
            
        # If it has hit this point then something has gone wrong
        return False

    def send_marker_to_position(self, corner_position):
        self.output.put({ 
            "name": "Calibration move marker", 
            "tag": "CALIBRATION_MOVE_MARKER", 
            "data": corner_position
        })

    def complete_calibration(self):
        boundary: BoundaryBox = self.shared_state['boundary_box']
        
        # Sending over to client to be saved to the database
        self.output.put({ 
            "name": "Calibration Complete", 
            "tag": "CALIBRATION_COMPLETE", 
            "data": boundary.get_points_arr()
        })