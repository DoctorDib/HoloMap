from abc import abstractmethod
from multiprocessing import Event, Process, Queue, shared_memory
import multiprocessing
import numpy as np

from flask import Flask

from Common.Modules import Modules
from config import Config
import logger

class ModuleHelper(Process):
    def __init__(self, name: str, has_modules: bool = False, module_directory: str = None, module_str: str = None, parent_memory_name: str = None, 
                 app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        super().__init__()

        logger.info(f"Starting up {name} Process")

        # The name of the process
        self._name = name
        # Modules that will run on their own process
        self.modules = None
        # The detector if the module has one
        self.detector = None
        # Event that will trigger the shutdown
        self.shutdown_event = Event()

        self.memory = None
        self.parent_memory = None
        self.app = app

        self.config = Config()

        self.output = output
        self.shared_state = shared_state

        memory_size = self.config.get_int('RESOLUTION_WIDTH')*self.config.get_int('RESOLUTION_HEIGHT')*self.config.get_int('RESOLUTION_CHANELS')
        
        # Setting up modules
        if (has_modules):
            # Memory that it will send to their own processes list
            self.memory = shared_memory.SharedMemory(create=True, size=memory_size)
            # Setting up the multi process modules helper
            self.modules = Modules(module_directory, module_str)
            # Initialises all of the modules
            self.modules.initialise(self.memory.name, memory_size=memory_size, app=app, output=output, shared_state=shared_state)

        # The data input
        if (parent_memory_name is not None):
            self.parent_memory = shared_memory.SharedMemory(name=parent_memory_name, size=memory_size)

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
        
    def start(self):
        logger.info(f"Starting {self._name} Process")
        super().start()
        
    def shutdown_process(self):
        self.join()
        self.terminate()

    def stop(self):
        logger.info(f"Stopping {self._name} Process")
        self.graceful_shutdown()
        
    def graceful_shutdown(self):
        if (self.shutdown_event.is_set()):
            # Shutdown process has already started
            return
        
        logger.info(f"Gracefully shutting down {self._name}")
        self.shutdown_event.set()

    def set_up_frame(self):
        """
        Sets up the frame by linking it to the shared memory buffer.

        Returns:
            np.ndarray: The frame as a NumPy array.
        """
        # Ensure the buffer is large enough for the image
        buffer_size = np.prod(self.image_shape)
        
        if len(self.parent_memory.buf) < buffer_size:
            raise ValueError("Buffer size is too small for the image. Ensure the shared memory size is correct.")

        height = self.config.get_int('RESOLUTION_HEIGHT')
        width = self.config.get_int('RESOLUTION_WIDTH')
        channels = self.config.get_int('RESOLUTION_CHANELS')
        
        self.frame = np.ndarray((height, width, channels), dtype=np.uint8, buffer=self.parent_memory.buf)
        
        logger.info(f"Attempting to set up Camera")

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