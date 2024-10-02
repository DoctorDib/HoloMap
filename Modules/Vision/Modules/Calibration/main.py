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
from API.shared_state import BoundaryBoxFactory, BoundaryBoxResetFlagFactory, CalibrationFlagFactory, CameraFactory, DebugModeFlagFactory

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

        # Define lower and uppper limits
        # +-15% of S and V, +-60 on H
        #226,220,85 => 226/2,86%,33% = 113,0.86*255,0.33*255
        self.lower_red1 = np.array([0, 150, 150], np.uint8)  # Lower bound for the darkest red
        self.upper_red1 = np.array([0, 255, 255], np.uint8)   # Upper bound for the lightest red

        # Additional mask for upper red hues
        self.lower_red2 = np.array([170, 115, 115], np.uint8)  # Adjust this if necessary
        self.upper_red2 = np.array([180, 255, 255], np.uint8)  # Adjust this if necessary

        # self.red_lower1 = np.array([0, 50, 50], np.uint8)  # Much broader range for hue, saturation, and value
        # self.red_upper1 = np.array([180, 255, 255], np.uint8)

        # self.red_lower2 = np.array([170, 50, 50], np.uint8)  # Another range for red
        # self.red_upper2 = np.array([180, 255, 255], np.uint8)
        
        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        # self.kernal = np.ones((5, 5), "uint8")

        self.loop_count = 0
        self.loop_limit = 1

        self.sleep_time = 5 # seconds

        self.outlier_detection = CalibrationOutlierDetection()

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
        mask1 = cv2.inRange(hsv_frame, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)

        red_mask = cv2.bitwise_or(mask1, mask2)

        # Apply Gaussian blur to smooth the mask
        red_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)

        # red_mask = mask1 | mask2

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernel = np.ones((5, 5), "uint8")
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        
        # For red color
        # red_mask = cv2.dilate(red_mask, kernel)

        # save results
        with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
            if (flag_state.value):
                with CameraFactory("calibration_mask_camera", self.shared_state) as camera:
                    camera.value = red_mask
        
        # Creating contour to track red color
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if (len(contours) <= 0):
            return None
        
        # Draw contours on the original frame
        for contour in contours:
            cv2.drawContours(frame, [contour], -1, (0, 255, 255), 2)  # Yellow color in BGR (0, 255, 255)

        # largest_contour = max(contours, key=cv2.contourArea)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            print("================")
            print(f"AREA : {area}")
            if area > 1000 and area < 5000:  # Use the adjustable minimum area
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)  # Draw bounding box
                x, y, w, h = cv2.boundingRect(approx)
                
                # Drawing them out
                frame = cv2.circle(frame, (x, y), 10, (255, 0, 255), 2)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                    if (flag_state.value):
                        with BoundaryBoxFactory(self.shared_state) as boundary_state:
                            # Drawing boundaries
                            frame = boundary_state.value.draw_boundary(frame)

                            # font = cv2.FONT_HERSHEY_SIMPLEX
                            # fontScale = 1
                            # color = (0, 255, 0)
                            # thickness = 2
                            
                            # Adding infor for the boundaries
                            # frame = cv2.putText(frame, 'Top Left: ' + str(boundary_state.value.top_left), (500, 900), font, fontScale, color, thickness, cv2.LINE_AA)
                            # frame = cv2.putText(frame, 'Top Right: ' + str(boundary_state.value.top_right), (500, 950), font, fontScale, color, thickness, cv2.LINE_AA)
                            # frame = cv2.putText(frame, 'Bottom Right: ' + str(boundary_state.value.bottom_right), (500, 1000), font, fontScale, color, thickness, cv2.LINE_AA)
                            # frame = cv2.putText(frame, 'Bottom Left: ' + str(boundary_state.value.bottom_left), (500, 1050), font, fontScale, color, thickness, cv2.LINE_AA)

                            with CameraFactory("calibration_camera", self.shared_state) as calibration_camera:
                                calibration_camera.value = frame

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
