from multiprocessing import Queue
import multiprocessing
import os
from API.shared_state import CameraFactory, DebugModeFlagFactory
import cv2
from flask import Flask
import numpy as np
import logger

from Common.ModuleHelper import ModuleHelper

class Vision_Module(ModuleHelper):
    def __init__(self, memory_name: str = None, memory_size: int = 1920 * 1080 * 3,
                app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\Modules"
        
        super().__init__("Vision", True, self.base_folder_path, "Modules.Vision.Modules.{0}.main.{0}_Module", app=app, output=output, shared_state=shared_state)

        # Shared memory setup
        self.memory_name = memory_name
        self.memory_size = memory_size

    def prep(self):
        if (self.config == None):
            return

        self.detector = cv2.VideoCapture(self.config.get_int("CAMERA_SOURCE"), cv2.CAP_DSHOW)  # this is the magic!

        self.detector.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get_int("RESOLUTION_WIDTH"))
        self.detector.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get_int("RESOLUTION_HEIGHT"))
        self.detector.set(cv2.CAP_PROP_FPS, self.config.get_int("FPS"))
        self.detector.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # Screen friendly
        self.detector.set(cv2.CAP_PROP_AUTO_WB, 0)  # Disable auto white balance
        self.detector.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.4)  # Disable auto exposure (0.25 is manual mode, 0.75 is auto)

        # Manually set exposure and white balance if needed
        # self.detector.set(cv2.CAP_PROP_EXPOSURE, -5)  # Adjust this value as needed
        # self.detector.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)  # Adjust this value as needed

    def run(self):
        if self.detector is None:
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                img = self.camera_stuff()

                if img is not None:
                    try:
                        # Send image over shared memory
                        self.send_img_via_shared_memory(img)
                    except Exception as e:
                        logger.error("send_img_via_shared_memory: ", e)
                        pass

                with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                    if img is not None and flag_state.value:
                        with CameraFactory("main_camera", self.shared_state) as camera_state:
                            camera_state.value = img
                        cv2.waitKey(1)

        except Exception as e:
            logger.error(e)
        finally:
            logger.info("Shutting down CV2 capture")
            self.detector.release()
            cv2.destroyAllWindows()

    def camera_stuff(self):
        if self.detector is None:
            return None
        
        succeed, img = self.detector.read()

        # Flipping camera to specified configuration
        flip_value = self.config.get_int('FLIP_CAMERA')
        if (flip_value > -2 and flip_value <= 1):
            img = cv2.flip(img, flip_value)

        return img if succeed else None

    def send_img_via_shared_memory(self, img):
        # Flatten the image to a 1D array
        flat_img = img.flatten()

        # Create a NumPy array that maps to the shared memory buffer
        shm_array = np.ndarray((self.config.get_int('RESOLUTION_HEIGHT'), self.config.get_int('RESOLUTION_WIDTH'), self.config.get_int('RESOLUTION_CHANELS')), dtype=np.uint8, buffer=self.memory.buf)

        # Copy the image data to the shared memory buffer
        np.copyto(shm_array, img)
