from multiprocessing import Queue
import multiprocessing
import os
from API.shared_state import ModuleSharedStateFactory
from flask import Flask

from Common.ModuleHelper import ModuleHelper

class Main_Module(ModuleHelper):
    def __init__(self, memory_name: str = None, parent_module_name: str = None, memory_size: int = None,
                app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None, module_path: str = ""):

        self.base_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\Modules"
        
        super().__init__("Main", parent_module_name, True, self.base_folder_path, "Main.Modules.{0}.main.{0}_Module", app=app, output=output, shared_state=shared_state, module_path=module_path)
        
        # Shared memory setup
        self.memory_name = memory_name
        self.memory_size = memory_size

    def prep(self):
        if (self.config == None):
            return

        super().prep()

    def run(self):
        self.prep()

        try:
            while not self.shutdown_event.is_set():
                should_run = self.common_run()
                if (not should_run):
                    continue

        except Exception as e:
            with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
                state.value.log_error(e)
            
        finally:
            with ModuleSharedStateFactory(self.name, self.shared_state, read_only=True) as state:
                state.value.log_info("Shutting down CV2 capture") # TODO change this