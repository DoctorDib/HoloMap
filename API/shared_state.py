import base64
import cv2
from Modules.Vision.Modules.Hands.hands_control import HandsControl
import multiprocessing, numpy

from Modules.Vision.BoundaryBox import BoundaryBox

import logger

class SharedStateValue:
    def __init__(self, key: str, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):

        self.shared_state = shared_state
        self.read_only = read_only

        self.key = key
        self.value = None

    def __enter__(self):
        self.value = self.shared_state.get(self.key)
        return self

    def __exit__(self, exc_type, exc_val: BaseException, exc_tb) -> bool:
        if exc_type:
            logger.error(f"Shared State Manager for {self.key}: {exc_type}, {exc_val}")
            return False

        if (not self.read_only):
            self.shared_state[self.key] = self.value

        return True
    
class DynamicFactory(SharedStateValue):
    def __init__(self, key: str, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__(key, shared_state, read_only)
        self.value: any
    
class HandsFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__('hands', shared_state, read_only)
        self.value: HandsControl

class BoundaryBoxFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__('boundary_box', shared_state, read_only)
        self.value: BoundaryBox

class ProjectorBoundaryBoxFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__('projector_boundary_box', shared_state, read_only)
        self.value: BoundaryBox

class CalibrationFlagFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__('calibration_flag', shared_state, read_only)
        self.value: bool

class BoundaryBoxResetFlagFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__('boundary_box_reset', shared_state, read_only)
        self.value: bool

class DebugModeFlagFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__('debug_mode', shared_state, read_only)
        self.value: bool

class CameraFactory(SharedStateValue):
    def __init__(self, camera_name, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__(camera_name, shared_state, read_only)
        self.shared_state = shared_state
        self.camera_name = camera_name
        self.value: numpy.ndarray
        
    def update(self, img):
        self.value = img
        
        with CameraBase64Factory(self.camera_name, self.shared_state, read_only=False) as camera_state:
            camera_state.update(img) # update base64 string

class CameraBase64Factory(SharedStateValue):
    def __init__(self, camera_name, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__(camera_name + "_base64", shared_state, read_only)
        self.value: any
        
    def update(self, img):
        _, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        self.value = base64.b64encode(buffer).decode('utf-8')

class PcStatsFactory(SharedStateValue):
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__("PcStats", shared_state, read_only)
        self.value: object

class HeartBeatClockFactory(SharedStateValue):
    def __init__(self, module_or_plugin_name, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__(module_or_plugin_name + "_module_heartbeat", shared_state, read_only)
        self.value: float
class ModulePluginActiveFactory(SharedStateValue):
    def __init__(self, module_or_plugin_name, shared_state: multiprocessing.managers.SyncManager.dict, read_only: bool = False):
        super().__init__(module_or_plugin_name + "_is_active", shared_state, read_only)
        self.value: bool

class SharedState:
    def __init__(self, manager):
        self.shared_state = manager.dict()

        # Presets - not really needed but keeping just in case
        with DebugModeFlagFactory(self.shared_state) as state:
            state.value = False
        with BoundaryBoxFactory(self.shared_state) as state:
            state.value = BoundaryBox()
        with ProjectorBoundaryBoxFactory(self.shared_state) as state:
            state.value = BoundaryBox()
        with HandsFactory(self.shared_state) as state:
            state.value = HandsControl()
        with PcStatsFactory(self.shared_state) as state:
            state.value = {}

        # Calibration specifics
        with CalibrationFlagFactory(self.shared_state) as state:
            state.value = False
        with BoundaryBoxResetFlagFactory(self.shared_state) as state:
            state.value = False

    def get_shared_state(self):
        """
        Recieve the shared state dictionary
        """
        return self.shared_state
    
    def set_state(self, key, value):
        """
        Setting a value with a key in a shared state dictionary
        """
        self.shared_state[key] = value

    def get_state(self, key):
        """
        Getting a value with a key in a shared state dictionary
        """
        print(key)
        print(self.shared_state)
        return self.shared_state[key]