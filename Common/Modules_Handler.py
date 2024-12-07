import os
import importlib
import multiprocessing
import multiprocessing.managers
import multiprocessing.shared_memory

from flask import Flask

from Common.Classes.instance import Instance

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Only importing for type checking
    from Common.ModuleHelper import ModuleHelper
    
class Modules_MultiProcess:
    # List of string names of modules
    modules = []

    instance: Instance

    def __init__(self, base_folder_path: str, class_path_pattern: str, memory_name: str, memory_size: int, app: Flask = None, 
                   output: multiprocessing.Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None, 
                   parent_module_name: str = ""):
        self.instance = Instance()
        self.base_folder_path = base_folder_path
        self.class_path_pattern = class_path_pattern
        self.module_instances: list[ModuleHelper] = []
        
        self.memory_name = memory_name
        self.memory_size = memory_size
        self.app = app
        self.output = output
        self.shared_state = shared_state
        self.parent_module_name = parent_module_name

    def initialise(self):
        
        self.load_initial_modules()
        
        return self.modules
        
    def load_from_file(self, class_str):
        module_path, _, class_name = class_str.rpartition('.')
        mod = importlib.import_module(module_path)
        class_obj = getattr(mod, class_name)
        return class_obj


    def shutdown(self):
        for module in self.module_instances:
            module.graceful_shutdown()
        
        self.instance.close_instance()
        self.instance.shutdown()

    def detect_modules(self):
        detected_moudles: list[object] = []
        
        for item in os.listdir(self.base_folder_path):
            if ("__pycache__" in item):
                continue
            
            item_path = os.path.join(self.base_folder_path, item)
            if os.path.isdir(item_path):  # Check if the item is a directory
                main_file_path = os.path.join(item_path, 'main.py')
                disabled = os.path.join(item_path, 'disabled')
                
                if os.path.isfile(main_file_path) and not os.path.isfile(disabled):    # Check if main.py exists in the directory
                    
                    detected_moudles.append({
                        'item': item,
                        'item_path': item_path,
                    })
        
        return detected_moudles

    def load_initial_modules(self):
        """Load modules that already exist in the base folder."""
        
        # self.main_files.clear()  # Clear any existing main files
        self.modules.clear()
        
        detected_modules = self.detect_modules()
        
        for module in detected_modules:
            item_path = module['item_path']
            item = module['item']
            
            main_file_path = os.path.join(item_path, 'main.py')
            disabled = os.path.join(item_path, 'disabled')
            
            if os.path.isfile(main_file_path) and not os.path.isfile(disabled):    # Check if main.py exists in the directory
                self.modules.append(item)
                self.start_module(item)
    
    def check_for_new_modules(self, modules_list: list[str]):
        detected_modules = self.detect_modules()
        
        # Convert modules_list to a set for O(1) membership checks
        module_set = set(modules_list)
        
        differences = {
            'added': [],
            'removed': [],
            'unchanged': [],
        }
        
        # Check detected modules for 'added' or 'unchanged' status
        for detected_module in detected_modules:
            if detected_module['item'] in module_set:
                differences['unchanged'].append(detected_module)
            else:
                differences['added'].append(detected_module)
        
        # Check for modules in modules_list that are not in detected_modules
        detected_items = { detected['item'] for detected in detected_modules }
        differences['removed'] = [module for module in module_set if module not in detected_items]
        
        return differences
    
    def reload_all_modules(self, modules_list: list[str]):
        modules = self.check_for_new_modules(modules_list)
        
        # Creating new process for new modules detected
        for module in modules['added']:
            # self.start_module(module['item'])
            modules_list.append(module['item'])
            
        # Removing old modules from state
        for module in modules['removed']:
            # del self.instance.processes[module]
            modules_list.remove(module)
            
        # Starting modules back up
        for module in modules_list:
            self.start_module(module)
        
  
    def start_module(self, item):
        """Start a module based on its main.py file."""
        
        # Starting the process
        class_path = self.class_path_pattern.format(item)
        
        new_process_class = self.load_from_file(class_path)
        new_process = new_process_class(self.memory_name, self.parent_module_name, self.memory_size, self.app, self.output, self.shared_state, item)
        self.instance.start_process(item, process = new_process)
        new_process.start()
