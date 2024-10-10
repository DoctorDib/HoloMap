from multiprocessing import Queue
import multiprocessing
from time import sleep
from API.shared_state import BoundaryBoxFactory, CameraFactory, DebugModeFlagFactory
from Common.KalmanFilter import KalmanFilter
from Common.helper import convert_tuple_coords
from flask import Flask

import os, cv2
import logger

import cv2.aruco as aruco

from Common.ModuleHelper import ModuleHelper

class ArUco_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape, app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        super().__init__("ArUco", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        
        self.image_shape= image_shape

        self.frame = None

        self.number_of_aruco = 0
        self._detection_threshold = 3
        self.detection_counter = 0

        self.detected_aruco = False

        # self.kalman_filter = KalmanFilter(process_variance=1e-2, measurement_variance=1e-2)

    def prep(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.parameters =  cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)
        super().prep()

    def new_aruco_marker(self, img):
        # TODO - Add decoding by using the ArUco dictionary / Ids
        pass

    def reset(self):
        self.detection_counter = 0

    # Called from the main thread
    def run(self):
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                sleep(self.timeout_buffer)

                # with(CalibrationFlagFactory(self.shared_state, read_only=True)) as flag_state:
                #     if (flag_state.value):
                #         continue

                try:                    
                    img = self.receive_image()

                    if img is None:
                        continue

                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    detected_corners, ids, disguarded = aruco.detectMarkers(gray, self.dictionary, parameters=self.parameters)

                    if (ids is None):
                        # No marker detected
                        continue

                    if (len(ids) == 0):
                        if (self.detected_aruco):

                            self.detected_aruco = False

                            print("Hi")

                            # Remove any boxes from client ui
                            self.output.put({ 
                                "name": "Clear all ARUCO detections", 
                                "tag": "CLEAR_ARUCO",
                            })
                        continue

                    with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                        if (flag_state.value):
                            # Drawing the detected boxes
                            for detected in detected_corners:
                                corners = detected[0]

                                top_left = (int(corners[0][0]), int(corners[0][1]))
                                bottom_right = (int(corners[2][0]), int(corners[2][1]))

                                # Drawing square around ArUco marker
                                cv2.rectangle(img, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=2)
                                cv2.putText(img, f'{ids[0]}', (top_left[0], top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                    fontScale=1, color=(0, 255, 0), thickness=2)

                    if (len(ids) != self.number_of_aruco):
                        if (self.detection_counter >= self._detection_threshold or len(ids) < self.number_of_aruco):
                            self.number_of_aruco = len(ids)
                            self.new_aruco_marker(img)
                            self.reset()
                        else:
                            self.detection_counter += 1


                    # Use get_real_coords to transform the quad coordinates
                    corners = detected_corners[0][0] # TODO - Add support for multiple markers
                    out = convert_tuple_coords(corners)

                    # - We also might want to reduce the resolution of the camera because of the 100% CPU issue...
                    #       I am hoping if we reduce it down to 720p, it shouldn't affect the behaviour, just improve performance!
                    #       (Perhaps look into a way of easily changing the values in the .env file that will affect all of
                    #           image processing modules without breaking anytihng!)

                    # TODO - IMPLEMENT KALMAN FILTER
                    
                    # # Kalman filter processing using the transformed coordinates
                    # real_center = np.mean(out, axis=0)  # Find the center from the transformed coordinates
                    # self.kalman_filter.predict()  # Predict the next state
                    # self.kalman_filter.update(real_center)  # Update with the measurement
                    # estimated_position = self.kalman_filter.get_estimate()  # Get the estimated position

                    # Adjust 'out' coordinates based on the smoothed estimated_position
                    # offset = estimated_position - real_center  # Calculate the offset from the real center to the estimated position
                    # smoothed_out = out + offset  # Apply the offset to all points in 'out'


                    # cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
                    # cv2.circle(img, tuple(estimated_position.astype(int)), radius=5, color=(255, 0, 0), thickness=-1)


                    self.detected_aruco = True

                    self.output.put({ 
                        "name": "Detected ArUco", 
                        "tag": "ARUCO_DETECTION", 
                        "data": [out] # TODO - Array because there will be more than one QR in future
                    })
    
                    with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                        if (flag_state.value):
                            with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
                                img = boundary_state.value.draw_boundary(img)

                                with CameraFactory("aruco_camera", self.shared_state) as camera_state:
                                    camera_state.value = img
                    cv2.waitKey(1)
                    
                except Exception as e:
                    logger.error("ArUco Error: ", e)
        finally:
            cv2.destroyAllWindows()