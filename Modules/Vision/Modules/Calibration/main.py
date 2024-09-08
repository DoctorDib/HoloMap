from multiprocessing import Queue
from time import sleep
from flask import Flask

import cv2
import logger
import numpy as np
import multiprocessing
import multiprocessing.managers

from Common.ModuleHelper import ModuleHelper
from Modules.Vision.BoundaryBox import BoundaryBox
from Modules.Vision.OutlierDetection import CalibrationOutlierDetection
from API.shared_state import BoundaryBoxFactory, BoundaryBoxResetFlagFactory, CalibrationFlagFactory, DebugModeFlagFactory

class Calibration_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape=(1080, 1920, 3), app: Flask = None, output: Queue = None, 
                 shared_state: multiprocessing.managers.SyncManager.dict = None):
        """
        Initializes the Calibration_Module class.

        Args:
            memory_name (str): The name of the memory shared between processes.
            image_shape (tuple): The shape of the image (default is (1080, 1920, 3)).
            app (Flask, optional): Flask application instance.
            output (Queue, optional): Queue for sending data to other processes.
            shared_state (multiprocessing.managers.SyncManager.dict, optional): Shared state dictionary.
        """

        super().__init__("Calibration", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.image_shape = image_shape
        self.frame = None

        # Controlling the UI red marker box
        # 0 = top left
        # 1 = top right
        # 2 = bottom right
        # 3 = bottom left
        self.marker_position: int = 0

        # Define the HSV range for detecting the specific red color
        # Red color can be in two ranges due to the hue wrap-around in HSV color space
        tolerance = 4  # Adjust this value for sensitivity

        # Lower red range (0-10 degrees on the Hue scale)
        self.red_lower1 = np.array([0, 120, 70])
        self.red_upper1 = np.array([tolerance, 255, 255])

        # Upper red range (170-180 degrees on the Hue scale)
        self.red_lower2 = np.array([180 - tolerance, 120, 70])
        self.red_upper2 = np.array([180, 255, 255])

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        self.kernal = np.ones((5, 5), "uint8")

        self.loop_count = 0
        self.loop_limit = 3

        self.sleep_time = 5 # seconds

        self.outlier_detection = CalibrationOutlierDetection()

    def set_up_frame(self):
        """
        Sets up the frame by linking it to the shared memory buffer.

        Returns:
            np.ndarray: The frame as a NumPy array.
        """
        # Ensure the buffer is large enough for the image
        buffer_size = np.prod(self.image_shape)
        if len(self.parent_memory.buf) < buffer_size:
            raise ValueError("Buffer size is too small for the image. Ensure the shared memory size is correct.")

        self.frame = np.ndarray((1080, 1920, 3), dtype=np.uint8, buffer=self.parent_memory.buf)
        logger.info(f"Attempting to set up Camera")
        
        return self.frame
    
    def receive_image(self):
        """
        Receives the image from the shared memory buffer.

        Returns:
            np.ndarray or None: The image frame if available; otherwise, None.
        """
        if self.frame is not None and self.frame.size > 0 and not np.all(self.frame) and np.any(self.frame):
            return self.frame
        else:
            self.set_up_frame()
            return None

    def run(self):
        """
        Main method that runs the calibration process in a loop until shutdown is triggered.
        """
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                # Helps preventing overflow!
                sleep(1)

                with(CalibrationFlagFactory(self.shared_state, read_only=True)) as flag_state:
                    if (not flag_state.value):
                        sleep(self.sleep_time) # seconds
                        continue

                with(BoundaryBoxResetFlagFactory(self.shared_state, read_only=True)) as flag_state:
                    if (not flag_state.value):
                        self.new_calibration()

                try:
                    img = self.receive_image()

                    if img is None:
                        continue

                    else:
                        img = self.process_frame(img)

                        if (img is None):
                            continue

                        with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                            if (flag_state.value):
                                with BoundaryBoxFactory(self.shared_state) as boundary_state:
                                    # Drawing boundaries
                                    img = boundary_state.value.draw_boundary(img)

                                    font = cv2.FONT_HERSHEY_SIMPLEX
                                    fontScale = 1
                                    color = (0, 255, 0)
                                    thickness = 2
                                    
                                    # Adding infor for the boundaries
                                    img = cv2.putText(img, 'Top Left: ' + str(boundary_state.value.top_left), (500, 900), font, fontScale, color, thickness, cv2.LINE_AA)
                                    img = cv2.putText(img, 'Top Right: ' + str(boundary_state.value.top_right), (500, 950), font, fontScale, color, thickness, cv2.LINE_AA)
                                    img = cv2.putText(img, 'Bottom Right: ' + str(boundary_state.value.bottom_right), (500, 1000), font, fontScale, color, thickness, cv2.LINE_AA)
                                    img = cv2.putText(img, 'Bottom Left: ' + str(boundary_state.value.bottom_left), (500, 1050), font, fontScale, color, thickness, cv2.LINE_AA)

                            cv2.imshow("Calibration", img)
                            cv2.waitKey(1)
                except Exception as e:
                    logger.error("Calibration Error: ", e)

                if (self.loop_count >= self.loop_limit):
                    self.complete_calibration()
        finally:
            cv2.destroyAllWindows()

    def new_calibration(self):
        """
        Resets the calibration process and initializes a new BoundaryBox.
        """

        self.loop_count = 0
        self.marker_position = 0

        # Resetting boundar box flag
        with BoundaryBoxResetFlagFactory(self.shared_state) as flag_instance:
            flag_instance.value = True

        # Resetting Boundary Box
        with BoundaryBoxFactory(self.shared_state) as boundary_state:
            boundary_state.value = BoundaryBox()

        # Sending marker to the top left position
        self.send_marker_to_position(self.marker_position)

    def process_frame(self, frame):
        """
        Processes the given frame to detect the red box and update the marker position.

        Args:
            frame (np.ndarray): The image frame to be processed.

        Returns:
            np.ndarray or None: The processed frame if successful; otherwise, None.
        """

        # Detect red box
        coords_and_size = self.detect_red_box(frame)
        if (coords_and_size is None):
            # If not successful, try it again!
            return None
        
        print("-===============================-")
        print("-===============================-")
        print("-===============================-")
        print("-===============================-")
        print(coords_and_size)

        # Process coords
        success = self.process_coords(coords_and_size)
        if (not success):
            # If not successful, try it again!
            return None

        # Can only go between 0 and 3
        if (self.marker_position < 3):
            self.marker_position += 1
        else:
            # Finished full loop
            self.loop_count += 1 
            self.marker_position = 0

            with BoundaryBoxFactory(self.shared_state) as boundary_state:
                boundary_state.value.new_round()

        # Moving marker
        self.send_marker_to_position(self.marker_position)

        return frame

    def detect_red_box(self, frame) -> any:
        """
        Detects the red box in the given frame using HSV color space.

        Args:
            frame (np.ndarray): The image frame in which to detect the red box.

        Returns:
            tuple or None: The coordinates and size of the red box if detected; otherwise, None.
        """

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
        Processes the coordinates and size of the detected red box to update the boundary box.

        Args:
            coords_and_size (any): Coordinates and size of the detected red box.

        Returns:
            bool: True if coordinates were successfully processed; otherwise, False.

        Dev Note:
            The coordinates are always based on the top left corner of the red marker
        """

        # TODO - Implement a cycle property to go through the calibration process x times
        # TODO - Implement an average which uses the cycle 

        try:
            marker_x = coords_and_size[0][0]
            marker_y = coords_and_size[0][1]
            marker_width = coords_and_size[1][0]
            marker_height = coords_and_size[1][1]

            with BoundaryBoxFactory(self.shared_state) as boundary_state:
                # Top left condition
                if (self.marker_position == 0):
                    boundary_state.value.insert(0, (marker_x, marker_y))
                # Top right condition
                elif (self.marker_position == 1):
                    x = marker_x + marker_width
                    y = marker_y
                    boundary_state.value.insert(1, (x, y))
                # Bottom right condition
                elif (self.marker_position == 2):
                    x = marker_x + marker_width
                    y = marker_y + marker_height
                    boundary_state.value.insert(2, (x, y))
                # Bottom left condition
                elif (self.marker_position == 3):
                    x = marker_x
                    y = marker_y + marker_height
                    boundary_state.value.insert(3, (x, y))

            return True
        except Exception as ex:
            logger.error("Error processing coords: ", ex)
            
        # If it has hit this point then something has gone wrong
        return False

    def send_marker_to_position(self, corner_position: int):
        """
        Sends the UI marker to a specified position.

        Args:
            corner_position (int): Position of the marker.
        """

        self.output.put({ 
            "name": "Calibration move marker", 
            "tag": "CALIBRATION_MOVE_MARKER", 
            "data": corner_position
        })

    def complete_calibration(self):
        """
        Finalizes the calibration process and sends the boundary box data to the client.
        """

        logger.info("Calibration complete")

        # Sending value to client
        with BoundaryBoxFactory(self.shared_state) as boundary_state:

            boundary_state.value.apply()

            # Sending over to client to be saved to the database
            self.output.put({ 
                "name": "Calibration Complete", 
                "tag": "CALIBRATION_COMPLETE", 
                "data": boundary_state.value.get_points_arr()
            })

        # Resetting all flags for next use
        with BoundaryBoxResetFlagFactory(self.shared_state) as flag_instance:
            # Resetting flag to reset
            flag_instance.value = False

        with CalibrationFlagFactory(self.shared_state) as flag_instance:
            # Disabling calibration
            flag_instance.value = False
