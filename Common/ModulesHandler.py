import importlib.util
import multiprocessing
import multiprocessing.managers
import multiprocessing.shared_memory
import os

from flask import Flask

from Common.Classes.instance import Instance

class Modules_MultiProcess():
    main_files = []

    instance: Instance

    def __init__(self, base_folder_path: str, class_path_pattern: str):
        self.instance = Instance()
        self.base_folder_path = base_folder_path
        self.class_path_pattern = class_path_pattern

    def initialise(self, memory_name: str, memory_size: int = 1920 * 1080 * 3, app: Flask = None, 
                   output: multiprocessing.Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        # Get all modules that have main.py
        self.main_files = []

        # Loop through all items in the base folder
        for item in os.listdir(self.base_folder_path):
            item_path = os.path.join(self.base_folder_path, item)
            if os.path.isdir(item_path):  # Check if the item is a directory
                main_file_path = os.path.join(item_path, 'main.py')
                if os.path.isfile(main_file_path):  # Check if main.py exists in the directory
                    self.main_files.append((item, main_file_path))  # Store the folder name and path

        for main_file in self.main_files:
            # Check if the class is indeed a class and not an instance
            class_path = self.class_path_pattern.format(main_file[0])
            new_process_class = self.load_from_file(class_path)

            new_process = new_process_class(memory_name, memory_size, app, output, shared_state)

            self.instance.start_process(main_file[0], process = new_process)

            new_process.start()

    def load_from_file(self, class_str):
        module_path, _, class_name = class_str.rpartition('.')
        mod = importlib.import_module(module_path)
        class_obj = getattr(mod, class_name)
        return class_obj

    def shutdown(self):
        self.instance.close_instance()
        self.instance.shutdown()

class Modules_SingleProcess():
    main_files = []

    instance: Instance

    def __init__(self, base_folder_path: str, class_path_pattern: str):
        self.base_folder_path = base_folder_path
        self.class_path_pattern = class_path_pattern

    def initialise(self, memory_name: str, memory_size: int = 1920 * 1080 * 3):
        # Get all modules that have main.py
        self.main_files = []
        self.instances = []

        # Loop through all items in the base folder
        for item in os.listdir(self.base_folder_path):
            item_path = os.path.join(self.base_folder_path, item)
            if os.path.isdir(item_path):  # Check if the item is a directory
                main_file_path = os.path.join(item_path, 'main.py')
                if os.path.isfile(main_file_path):  # Check if main.py exists in the directory
                    self.main_files.append((item, main_file_path))  # Store the folder name and path

        for main_file in self.main_files:
            # Check if the class is indeed a class and not an instance
            class_path = self.class_path_pattern.format(main_file[0])
            new_process_class = self.load_from_file(class_path)

            self.instances.append(new_process_class(memory_name, memory_size))

    def process_data(self, data):
        for instance in self.instances:
            
            instance.queue.put(data)
            # instance.run(data)

    def load_from_file(self, class_str):
        module_path, _, class_name = class_str.rpartition('.')
        mod = importlib.import_module(module_path)
        class_obj = getattr(mod, class_name)
        return class_obj

    def shutdown(self):
        print("NOW DOING A GRACEFUL SHUTDOWN")
        
        self.instance.close_instance()
        self.instance.shutdown()