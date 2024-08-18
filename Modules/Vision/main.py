from multiprocessing import Queue
import os
import cv2
from flask import Flask
from gevent import sleep
import numpy as np
import logger

from Common.ModuleHelper import ModuleHelper
from Modules.Vision.BoundaryBox import BoundaryBox

class Vision_Module(ModuleHelper):
    def __init__(self, memory_name: str = None, memory_size: int = 1920 * 1080 * 3,
                app: Flask = None, output: Queue = None):
        self.prep()

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\Modules"
        
        super().__init__("Vision", True, self.base_folder_path, "Modules.Vision.Modules.{0}.main.{0}_Module", app=app, output=output)

        # Setting up the boundary
        self.cursor_boundary = BoundaryBox(top_left=(0, 0), top_right=(1920, 0), bottom_right=(1920, 1080), bottom_left=(0, 1080))

        # Shared memory setup
        self.memory_name = memory_name
        self.memory_size = memory_size

    def prep(self):
        self.detector = cv2.VideoCapture(2, cv2.CAP_DSHOW)  # this is the magic!

        self.detector.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.detector.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.detector.set(cv2.CAP_PROP_FPS, 30)
        self.detector.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    def run(self):
        if self.detector is None:
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                img = self.camera_stuff()

                sleep(0.1)

                if img is not None:
                    try:
                        # Send image over shared memory
                        self.send_img_via_shared_memory(img)
                    except Exception as e:
                        print("Uhh Ohh", e)
                        pass

                if img is not None:
                    cv2.imshow("Result", img)
                cv2.waitKey(1)
        except Exception as e:
            print(e)
        finally:
            logger.info("Shutting down CV2 capture")
            self.detector.release()
            cv2.destroyAllWindows()

    def camera_stuff(self):
        if self.detector is None:
            return None
        succeed, img = self.detector.read()
        return img if succeed else None

    def send_img_via_shared_memory(self, img):
        # Flatten the image to a 1D array
        flat_img = img.flatten()

        # Create a NumPy array that maps to the shared memory buffer
        shm_array = np.ndarray((1080, 1920, 3), dtype=np.uint8, buffer=self.memory.buf)

        # Copy the image data to the shared memory buffer
        np.copyto(shm_array, img)
