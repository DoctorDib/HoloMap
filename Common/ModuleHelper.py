from abc import abstractmethod
from multiprocessing import Event, Process, Queue, shared_memory, managers
import time
from API.shared_state import ModuleSharedStateFactory
from Common.Modules_Handler import Modules_MultiProcess
import numpy as np

from flask import Flask

from config import Config
from Common.ModuleSharedState import ModuleRunningStateEnum, ModuleSharedState

class ModuleHelper(Process):
    def __init__(self, name: str, module_parent_name: str = None, has_modules: bool = False, module_directory: str = None, module_str: str = None, parent_memory_name: str = None, app: Flask = None, output: Queue = None, shared_state: managers.SyncManager.dict = None, module_path: str = ""):
        super().__init__()
        
        # The name of the process
        self._name = name
        self.module_parent_name = module_parent_name
        # Modules that will run on their own process
        self.modules = []
        # The detector if the module has one
        self.detector = None
        # Event that will trigger the shutdown
        self.shutdown_event = Event()
        self.pause = False

        self.memory = None
        self.parent_memory = None
        self.app = app
        self.module_path=module_path

        self.config = Config()

        self.output = output
        self.shared_state = shared_state
        
        self.module_str = module_str
        self.module_directory = module_directory
        self.has_modules = has_modules
        
        with ModuleSharedStateFactory(self.name, self.shared_state, read_only=False) as state:
            # Originally sets up
            state.value = ModuleSharedState(self.name, module_parent_name, module_directory, should_start_paused=False)
        
        self.memory_size = self.config.get_int('RESOLUTION_WIDTH')*self.config.get_int('RESOLUTION_HEIGHT')*self.config.get_int('RESOLUTION_CHANELS')
        self.memory = shared_memory.SharedMemory(create=True, size=self.memory_size)
        
        # The data input
        if (parent_memory_name is not None):
            self.parent_memory = shared_memory.SharedMemory(name=parent_memory_name, size=self.memory_size)
        
    def set_up_modules(self, specific_modules_to_setup: list[str] | None = None):
        # Memory that it will send to their own processes list
        # self.memory = shared_memory.SharedMemory(create=True, size=self.memory_size)
        
        # Setting up the multi process modules helper
        temp = Modules_MultiProcess(self.module_directory, self.module_str, self.memory.name, self.memory_size, self.app, self.output, self.shared_state, self.name)
        # Initialises all of the modules
        new_modules = temp.initialise()
        # Concatting new modules to list
        self.modules = self.modules + new_modules # TODO - This will cause problems, will need a solution to maybe remove items when we stop?
                
    def common_run(self, custom_sleep = None):
        time.sleep(self.timeout_buffer if custom_sleep is None else custom_sleep)
        
        # Setting up state module
        with ModuleSharedStateFactory(self.name, self.shared_state, read_only=False) as state:
            
            # Check if module has been scheduled for any events    
            state.value.heartbeat()
            
        # Checking if there are any events scheduled
        self.do_schedule_checks()
        
        with ModuleSharedStateFactory(self.name, self.shared_state, read_only=False) as state:
            if (state.value.state == ModuleRunningStateEnum.RELOADED):
                state.value.state = ModuleRunningStateEnum.RUNNING
        
        return not self.pause
        
    def do_schedule_checks(self) -> ModuleSharedState:
        with ModuleSharedStateFactory(self.name, self.shared_state, read_only=False) as state:
            
            try:
                do_action: bool = state.value.check_scheduled_actions()
            
                if (not do_action):
                    return
                
                match (state.value.state):
                    case ModuleRunningStateEnum.INITIALISING:
                        # Loading the neccessary modules
                        if (self.has_modules):
                            self.set_up_modules(self.modules)
                            
                        self.pause = False
                        
                        state.value.state = ModuleRunningStateEnum.RUNNING
                    
                    case ModuleRunningStateEnum.STOPPING:
                        # Shutting down Instance class that contains all processes of modules
                        state.value = self.set_shutdown(state.value)
                        
                    case ModuleRunningStateEnum.PAUSING:
                        state.value = self.set_pause(state.value)
                        
                    case ModuleRunningStateEnum.RESUMING:
                        print("Oh I am trying")
                        state.value = self.set_resume(state.value)
                        
                    case ModuleRunningStateEnum.RELOADING:
                        state.value = self.set_reload(state.value)
                        
                    case _: 
                        # Default, no actions required
                        pass
            except Exception as e:
                state.value.log_error(e)
                state.value.state = ModuleRunningStateEnum.ERRORED
                

    @abstractmethod
    def prep(self):
        """
        Prepares the module process with any custom stuff
        """
        
        self.timeout_buffer = self.config.get_double('TIMEOUT_BUFFER')
        
        pass

    @abstractmethod
    def run(self):
        """
        Runs the module after Process.start is called
        """
        pass
        
    def set_reload(self, main_state: ModuleSharedState) -> ModuleSharedState: 
        # Reload all child modules
        # for module_name in self.modules:
        #     with ModuleSharedStateFactory(module_name, self.shared_state, read_only=True) as state:
        #         state.value.reload()

        # with ModuleSharedStateFactory(self.name, self.shared_state, read_only=False) as state:
        #     state.value.state = ModuleRunningStateEnum.RUNNING
        #     state.value.log_info(f"{self._name} has reloaded its modules")
        
        # Shutting down all children
        for module_name in self.modules:
            with ModuleSharedStateFactory(module_name, self.shared_state, read_only=False) as state:
                state.value.stop()
                state.value.state = ModuleRunningStateEnum.DISABLED

        # with ModuleSharedStateFactory(self.name, self.shared_state, read_only=False) as state:
        #     state.value.state = ModuleRunningStateEnum.RUNNING
        #     state.value.log_info(f"{self._name} has reloaded its modules")
        
        temp = Modules_MultiProcess(self.module_directory, self.module_str, self.memory.name, self.memory_size, self.app, self.output, self.shared_state, self.name)
        
        # Getting new list
        temp.reload_all_modules(self.modules)
        
        main_state.state = ModuleRunningStateEnum.RELOADED
        
        return main_state
        
    def set_pause(self, main_state: ModuleSharedState) -> ModuleSharedState:
        # Pause children first
        for module_name in self.modules:
            with ModuleSharedStateFactory(module_name, self.shared_state, read_only=False) as state:
                state.value.pause()
        
        # Pausing main one
        main_state.state = ModuleRunningStateEnum.PAUSED
        main_state.log_info(f"{self._name} has been paused")
            
        # Setting the pause flag
        self.pause = True
        
        return main_state
        
    def set_resume(self, main_state: ModuleSharedState) -> ModuleSharedState:
        # Pause children first
        for module_name in self.modules:
            with ModuleSharedStateFactory(module_name, self.shared_state, read_only=False) as state:
                state.value.play()
                
        main_state.state = ModuleRunningStateEnum.RUNNING
        main_state.log_info(f"{self._name} is resuming")
        
        # Setting the pause flag
        self.pause = False
        
        return main_state

    def set_shutdown(self, main_state: ModuleSharedState) -> ModuleSharedState:
        # Gracefully shutting down module
        if (self.shutdown_event.is_set()):
            # Shutdown process has already started
            return
        
        # Shut down children first
        for module_name in self.modules:
            with ModuleSharedStateFactory(module_name, self.shared_state, read_only=False) as state:
                state.value.stop()
        
        main_state.state = ModuleRunningStateEnum.STOPPED
        main_state.log_info(f"Gracefully shutting down {self._name}")
            
        # Setting flag to exit while loop on main loop
        self.shutdown_event.set()
            
        # self.terminate()
        # Waiting for the process to finish
        # self.join()
        
        return main_state
    
    def set_up_frame(self):
        """
        Sets up the frame by linking it to the shared memory buffer.

        Returns:
            np.ndarray: The frame as a NumPy array.
        """
        # Ensure the buffer is large enough for the image
        buffer_size = np.prod(self.image_shape)
        
        if len(self.parent_memory.buf) < buffer_size:
            with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
                state.value.log_error("Buffer size is too small for the image. Ensure the shared memory size is correct.")    
                return None
            
        height = self.config.get_int('RESOLUTION_HEIGHT')
        width = self.config.get_int('RESOLUTION_WIDTH')
        channels = self.config.get_int('RESOLUTION_CHANELS')
        
        self.frame = np.ndarray((height, width, channels), dtype=np.uint8, buffer=self.parent_memory.buf)
        
        with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
            state.value.log_info(f"Attempting to set up Camera")

        return self.frame
    
    def receive_image(self):
        """
        Receives the image from the shared memory buffer.

        Returns:
            np.ndarray or None: The image frame if available; otherwise, None.
        """

        if self.frame is not None and self.frame.size > 0:
            if not np.any(self.frame):
                return None
            
            # Ensuring they can modify their own images without affecting other threads
            img_copy = self.frame.copy()
            return img_copy
        else:
            self.frame = self.set_up_frame()
            return None

    def __del__(self):
        if (self.memory is not None):
            self.memory.close()
            self.memory.unlink()

        if (self.parent_memory is not None):
            self.parent_memory.close()
            self.parent_memory.unlink()