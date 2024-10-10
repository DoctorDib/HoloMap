from multiprocessing import Queue
import multiprocessing
from time import sleep
from API.shared_state import BoundaryBoxFactory, CalibrationFlagFactory, CameraFactory, DebugModeFlagFactory
from Common.KalmanFilter import KalmanFilter
from flask import Flask

import os, cv2
import logger
import numpy as np

# from qreader import QReader

from qrdet import QRDetector
# from pyzbar.pyzbar import decode

from Common.ModuleHelper import ModuleHelper

class QR_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape, app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        super().__init__("QR", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        
        self.image_shape= image_shape

        self.frame = None

        self.number_of_qr = 0
        self._detection_threshold = 3
        self.detection_counter = 0

        self.detected_qr = False

        self.kalman_filter = KalmanFilter(process_variance=1e-2, measurement_variance=1e-2)

    def prep(self):
        self.detector = QRDetector(model_size='n', conf_th=.35)

    def new_qr(self, img):
        val = self.detector.detect_and_decode(image=img, is_bgr=True)
        
        for qr in val:
            if (qr is None):
                self.number_of_qr = -1
                return
        pass

    def reset(self):
        self.detection_counter = 0

    # Called from the main thread
    def run(self):    
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():

                with CalibrationFlagFactory(self.shared_state, read_only=True) as flag_instance:
                    # Don't run if calibrating
                    if (flag_instance.value):
                        continue
                    
                try:
                    sleep(.25)
                    img = self.receive_image()

                    if img is None:
                        continue

                    with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
                        img = boundary_state.value.draw_boundary(img)

                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                        # TODO - Image processing? 
                        #      - Need to research the best effective way of reading a QR

                        detected = self.detector.detect(image=img, is_bgr=True)
                        if (len(detected) == 0):
                            if (self.detected_qr):

                                self.detected_qr = False

                                # Remove any boxes from client ui
                                self.output.put({ 
                                    "name": "Clear all QR detections", 
                                    "tag": "CLEAR_QR",
                                })
                            continue

                        for detection in detected:
                            x1, y1, x2, y2 = detection['bbox_xyxy']
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            confidence = detection['confidence']
                            # Drawin square around qr
                            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
                            # Inserting confidence on image
                            cv2.putText(img, f'{confidence:.2f}', (x1, y1 - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale=1, color=(0, 255, 0), thickness=2)

                        if (len(detected) != self.number_of_qr):
                            if (self.detection_counter >= self._detection_threshold or len(detected) < self.number_of_qr):
                                self.number_of_qr = len(detected)
                                self.new_qr(img)
                                self.reset()
                            else:
                                self.detection_counter += 1

                        # Use get_real_coords to transform the quad coordinates
                        out = boundary_state.value.get_real_coords(detected[0]["quad_xy"], img.shape[1], img.shape[0])

                        # Kalman filter processing using the transformed coordinates
                        real_center = np.mean(out, axis=0)  # Find the center from the transformed coordinates
                        self.kalman_filter.predict()  # Predict the next state
                        self.kalman_filter.update(real_center)  # Update with the measurement
                        estimated_position = self.kalman_filter.get_estimate()  # Get the estimated position

                        # Adjust 'out' coordinates based on the smoothed estimated_position
                        offset = estimated_position - real_center  # Calculate the offset from the real center to the estimated position
                        smoothed_out = out + offset  # Apply the offset to all points in 'out'


                        cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
                        cv2.circle(img, tuple(estimated_position.astype(int)), radius=5, color=(255, 0, 0), thickness=-1)


                        self.detected_qr = True

                        self.output.put({ 
                            "name": "Detected QR", 
                            "tag": "QR_DETECTION", 
                            "data": [smoothed_out] # TODO - Array because there will be more than one QR in future
                        })
        
                        with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                            if (flag_state.value):
                                with CameraFactory("qr_camera", self.shared_state) as camera_state:
                                    camera_state.value = img
                        cv2.waitKey(1)
                    
                except Exception as e:
                    logger.error("QR Error: ", e)
        finally:
            cv2.destroyAllWindows()