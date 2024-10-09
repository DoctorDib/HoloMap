from multiprocessing import Queue
from time import sleep
from flask import Flask

import cv2
import logger
import numpy as np
import multiprocessing
import multiprocessing.managers
import cv2.aruco as aruco

from Common.ModuleHelper import ModuleHelper
from Modules.Vision.BoundaryBox import BoundaryBox
from Modules.Vision.OutlierDetection import CalibrationOutlierDetection
from API.shared_state import BoundaryBoxFactory, BoundaryBoxResetFlagFactory, CalibrationFlagFactory, CameraFactory, DebugModeFlagFactory

class Calibration_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape, app: Flask = None, output: Queue = None, 
                 shared_state: multiprocessing.managers.SyncManager.dict = None):
        """
        Initializes the Calibration_Module class.

        Args:
            memory_name (str): The name of the memory shared between processes.
            image_shape (tuple): The shape of the image.
            app (Flask, optional): Flask application instance.
            output (Queue, optional): Queue for sending data to other processes.
            shared_state (multiprocessing.managers.SyncManager.dict, optional): Shared state dictionary.
        """

        super().__init__("Calibration", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.image_shape = image_shape
        self.frame = None

        # Controlling the UI ArUco marker box
        # 0 = top left
        # 1 = top right
        # 2 = bottom right
        # 3 = bottom left
        self.marker_position: int = 0

        self.loop_count = 0
        self.loop_limit = 1

        self.sleep_time = 5 # seconds

        self.outlier_detection = CalibrationOutlierDetection()

    def prep(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.parameters =  cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

        super().prep()

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
        Processes the given frame to detect the aruco marker and update the marker position.

        Args:
            frame (np.ndarray): The image frame to be processed.

        Returns:
            np.ndarray or None: The processed frame if successful; otherwise, None.
        """

        # Detect aruco marker
        coords = self.detect_aruco(frame)
        if (coords is None):
            # If not successful, try it again!
            return None
        
        # Process coords
        success = self.process_coords(coords)
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

    def detect_aruco(self, frame) -> any:
        """
        Detects the ArUco marker in the given frame using HSV color space.

        Args:
            frame (np.ndarray): The image frame in which to detect the aruco marker.

        Returns:
            tuple or None: The coordinates and size of the aruco marker if detected; otherwise, None.
        """

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       
        corners, ids, _ = aruco.detectMarkers(gray, self.dictionary, parameters=self.parameters)

        # If markers are detected, draw them
        if ids is not None and len(ids) == 1 and ids[0] == 0: # TODO - Find a way to not have to hardcode the ArUco marker ID
            # Draw the detected markers and their IDs on the frame
            frame = aruco.drawDetectedMarkers(frame, corners, ids)
            
            # We only care about one of them
            corners = corners[0][0]

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
            
            return (corners[0], corners[1], corners[2], corners[3])
            
        # If we have reached this point then something has gone wrong
        return None

    def process_coords(self, coords: any) -> bool:
        """
        Processes the coordinates and size of the detected arcuo marker to update the boundary box.

        Args:
            coords (any): Coordinates detected ArUco.

        Returns:
            bool: True if coordinates were successfully processed; otherwise, False.

        Dev Note:
            Coords is a tuple of 4 tuples: (top left, top right, bottom right, bottom left)
        """

        # TODO - Implement an average which uses the cycle 

        try:
            with BoundaryBoxFactory(self.shared_state) as boundary_state:
                # Top left condition
                if (self.marker_position == 0):
                    boundary_state.value.insert(0, coords[0])
                # Top right condition
                elif (self.marker_position == 1):
                    boundary_state.value.insert(1, coords[1])
                # Bottom right condition
                elif (self.marker_position == 2):
                    boundary_state.value.insert(2, coords[2])
                # Bottom left condition
                elif (self.marker_position == 3):
                    boundary_state.value.insert(3, coords[3])

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
