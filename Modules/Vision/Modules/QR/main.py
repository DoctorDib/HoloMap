from multiprocessing import Queue
import multiprocessing
from time import sleep
from Modules.Vision.BoundaryBox import BoundaryBox
from flask import Flask

import os, cv2
import logger
import numpy as np

# from qreader import QReader

from qrdet import QRDetector
# from pyzbar.pyzbar import decode

from Common.ModuleHelper import ModuleHelper

class QR_Module(ModuleHelper):
    def __init__(self, memory_name: str, image_shape=(1080, 1920, 3), app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        super().__init__("QR", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "/Modules"
        
        self.image_shape= image_shape

        self.frame = None

        self.number_of_qr = 0
        self._detection_threshold = 3
        self.detection_counter = 0

    def prep(self):
        self.detector = QRDetector(model_size='n', conf_th=.35)

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

    def new_qr(self, img):
        val = self.detector.detect_and_decode(image=img, is_bgr=True)
        print(val)

        for qr in val:
            print(qr)

            if (qr is None):
                self.number_of_qr = -1
                return

    def reset(self):
        self.detection_counter = 0

    # Called from the main thread
    def run(self):
        if (self.detector is None):
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                try:
                    sleep(.25)
                    img = self.receive_image()

                    if img is None:
                        continue

                    boundary: BoundaryBox = self.shared_state['boundary_box']
                    img = boundary.draw_boundary(img)

                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                    # TODO - Image processing? 
                    #      - Need to research the best effective way of reading a QR

                    detected = self.detector.detect(image=img, is_bgr=True)

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
                            print(detected)
                            self.number_of_qr = len(detected)
                            self.new_qr(img)
                            self.reset()
                        else:
                            self.detection_counter += 1

                    out = boundary.get_real_coords(detected[0]["quad_xy"], img.shape[1], img.shape[0])

                    cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

                    self.output.put({ 
                        "name": "Detected QR", 
                        "tag": "QR_DETECTION", 
                        "data": [out]
                    })
    
                    cv2.imshow("QR", img)
                    cv2.waitKey(1)
                    
                except Exception as e:
                    print("QR Error: ", e)
        finally:
            cv2.destroyAllWindows()