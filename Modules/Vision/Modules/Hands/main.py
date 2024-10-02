import multiprocessing
import logger
import os
import cv2
import numpy as np
from HandTrackingModule import FindHands
from multiprocessing import Queue
from flask import Flask
from Common.ModuleHelper import ModuleHelper
from Modules.Vision.BoundaryBox import BoundaryBox
from API.shared_state import BoundaryBoxFactory, CameraFactory, DebugModeFlagFactory
from Common.KalmanFilter import KalmanFilter

class Hands_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape=(1080, 1920, 3), app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        super().__init__("Hands", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        self.image_shape = image_shape
        self.frame = None

        # Initialize the Kalman Filter
        self.kalman_filter = KalmanFilter(process_variance=1e-2, measurement_variance=1e-2)

    def prep(self):
        self.detector = FindHands()

    # Called from the main thread
    def run(self):
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                try:
                    img = self.receive_image()

                    if img is None:
                        continue

                    hand1_positions = self.detector.getPosition(img, range(21), draw=True)

                    with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
                        frame = boundary_state.value.draw_boundary(img)

                        if (len(hand1_positions) > 0):
                            # Get the position of the index finger tip (key point)
                            finger_tip = np.array(hand1_positions[8][:2])  # x, y

                            in_boundary = boundary_state.value.is_in_boundary(finger_tip[0], finger_tip[1])

                            if (in_boundary):
                                cv2.circle(frame, tuple(finger_tip.astype(int)), 5, (255, 0, 0), cv2.FILLED)

                                # Update Kalman Filter
                                self.kalman_filter.predict()
                                self.kalman_filter.update(finger_tip)

                                # Get the smoothed estimate from the Kalman Filter
                                smoothed_position = self.kalman_filter.get_estimate().astype(int)

                                out = boundary_state.value.get_relative_position(frame, smoothed_position)

                                # Moving virtual mouse cursor
                                self.output.put({
                                    "name": "Moving Virtual Mouse",
                                    "tag": "CURSOR_POINT",
                                    "data": [out]
                                })

                                cv2.circle(frame, tuple(smoothed_position), 10, (0, 255, 0), cv2.FILLED)

                        with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                            if (flag_state.value):
                                with CameraFactory("hands_camera", self.shared_state) as camera_state:
                                    camera_state.value = frame

                                    cv2.imshow("Image", frame)
                                    cv2.waitKey(1)

                except Exception as e:
                    logger.error("Uhh Ohh, e", e)
        finally:
            cv2.destroyAllWindows()
