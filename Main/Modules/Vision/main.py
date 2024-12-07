from multiprocessing import Queue
import multiprocessing
import os
from API.shared_state import BoundaryBoxFactory, CameraFactory, DebugModeFlagFactory, ModuleSharedStateFactory, ProjectorBoundaryBoxFactory
import cv2
from flask import Flask
import numpy as np

from Common.ModuleHelper import ModuleHelper

class Vision_Module(ModuleHelper):
    def __init__(self, memory_name: str = None, parent_module_name: str = None, memory_size: int = None,
                app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None, module_path: str = ""):

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\Modules"
        
        super().__init__("Vision", parent_module_name, True, self.base_folder_path, "Main.Modules.Vision.Modules.{0}.main.{0}_Module", app=app, output=output, shared_state=shared_state, module_path=module_path)

        # Shared memory setup
        self.memory_name = memory_name
        self.memory_size = memory_size

    def prep(self):
        if (self.config == None):
            return

        self.detector = cv2.VideoCapture(self.config.get_int("CAMERA_SOURCE"), cv2.CAP_DSHOW)  # this is the magic!

        self.detector.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get_int("RESOLUTION_WIDTH"))
        self.detector.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get_int("RESOLUTION_HEIGHT"))
        # self.detector.set(cv2.CAP_PROP_FPS, self.config.get_int("FPS"))
        # self.detector.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # Screen friendly (Mainly or colour recognition)
        # NOTE: Might not be needed anymore
        # self.detector.set(cv2.CAP_PROP_AUTO_WB, 0)  # Disable auto white balance
        # self.detector.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.4)  # Disable auto exposure (0.25 is manual mode, 0.75 is auto)

        # Disable auto-exposure
        # self.detector.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # This might vary depending on your webcam model
        # Manually set exposure (experiment with values)
        # self.detector.set(cv2.CAP_PROP_EXPOSURE, -5)  # Lower values mean shorter exposure

        # Manually set exposure and white balance if needed
        # self.detector.set(cv2.CAP_PROP_EXPOSURE, -5)  # Adjust this value as needed
        # self.detector.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)  # Adjust this value as needed
        self.detector.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
        self.detector.set(cv2.CAP_PROP_FOCUS , 5) # turn the autofocus off
        
        super().prep()

    def run(self):
        if self.detector is None:
            self.prep()

        try:
            while not self.shutdown_event.is_set():
                
                should_run = self.common_run()
                if (not should_run):
                    continue
                
                img = self.camera_stuff()

                if img is not None:
                    try:
                        # Send image over shared memory
                        self.send_img_via_shared_memory(img)
                    except Exception as e:
                        with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
                            state.value.log_error("send_img_via_shared_memory: ", str(e))
                        pass

                with DebugModeFlagFactory(self.shared_state, read_only=True) as flag_state:
                    if img is not None and flag_state.value:
                        with BoundaryBoxFactory(self.shared_state, read_only=True) as boundary_state:
                            img = boundary_state.value.draw_boundary(img)
                            
                            with ProjectorBoundaryBoxFactory(self.shared_state, read_only=True) as projector_state:
                                img = projector_state.value.draw_boundary(img, (0, 255, 0))
                                
                                with CameraFactory("vision_camera", self.shared_state) as camera_state:
                                    camera_state.update(img)
                cv2.waitKey(1)

        except Exception as e:
            with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
                state.value.log_error(e)
            
        finally:
            with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
                state.value.log_info("Shutting down CV2 capture")
                
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
        # flat_img = img.flatten()

        # Create a NumPy array that maps to the shared memory buffer
        shm_array = np.ndarray((self.config.get_int('RESOLUTION_HEIGHT'), self.config.get_int('RESOLUTION_WIDTH'), self.config.get_int('RESOLUTION_CHANELS')), dtype=np.uint8, buffer=self.memory.buf)

        # Copy the image data to the shared memory buffer
        np.copyto(shm_array, img)
