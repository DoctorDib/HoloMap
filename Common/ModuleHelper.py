from abc import abstractmethod
from multiprocessing import Event, Process, Queue, shared_memory

from flask import Flask

from Common.ModulesHandler import Modules_MultiProcess
import logger

class ModuleHelper(Process):
    def __init__(self, name: str, has_modules: bool = False, module_directory: str = None, module_str: str = None, parent_memory_name: str = None, app: Flask = None, output: Queue = None):
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

        self.output = output

        # Setting up modules
        if (has_modules):            
            # Memory that it will send to their own processes list
            self.memory = shared_memory.SharedMemory(create=True, size=1920*1080*3)
            # Setting up the multi process modules helper
            self.modules = Modules_MultiProcess(module_directory, module_str)
            # Initialises all of the modules
            self.modules.initialise(self.memory.name, app=app, output=output)

        # The data input
        if (parent_memory_name is not None):
            self.parent_memory = shared_memory.SharedMemory(name=parent_memory_name, size=1920*1080*3)

    @abstractmethod
    def prep(self):
        """
        Prepares the module process with any custom stuff
        """
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

    def __del__(self):
        if (self.memory is not None):
            self.memory.close()
            self.memory.unlink()

        if (self.parent_memory is not None):
            self.parent_memory.close()
            self.parent_memory.unlink()