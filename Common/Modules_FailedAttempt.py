import os
import importlib
import multiprocessing
import multiprocessing.managers
import multiprocessing.shared_memory

from flask import Flask
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Common.Classes.instance import Instance

class Modules_MultiProcess:
    main_files = []

    instance: Instance

    def __init__(self, base_folder_path: str, class_path_pattern: str):
        self.instance = Instance()
        self.base_folder_path = base_folder_path
        self.class_path_pattern = class_path_pattern
        self.observer = Observer()

    def load_initial_modules(self):
        """Load modules that already exist in the base folder."""
        self.main_files.clear()  # Clear any existing main files
        for item in os.listdir(self.base_folder_path):
            item_path = os.path.join(self.base_folder_path, item)
            if os.path.isdir(item_path):  # Check if the item is a directory
                main_file_path = os.path.join(item_path, 'main.py')
                disabled = os.path.join(item_path, 'disabled')
                if os.path.isfile(main_file_path) and not os.path.isfile(disabled):  # Check if main.py exists in the directory
                    self.main_files.append((item, main_file_path))  # Store the folder name and path
                    self.start_module(item)  # Start the module immediately

    def start_module(self, item):
        """Start a module based on its main.py file."""
        class_path = self.class_path_pattern.format(item)
        new_process_class = self.load_from_file(class_path)
        new_process = new_process_class(self.memory_name, self.memory_size, self.app, self.output, self.shared_state)
        self.instance.start_process(item, process=new_process)
        new_process.start()

    def load_from_file(self, class_str):
        module_path, _, class_name = class_str.rpartition('.')
        mod = importlib.import_module(module_path)
        class_obj = getattr(mod, class_name)
        return class_obj

    def initialise(self, memory_name: str, memory_size: int, app: Flask = None, 
                   output: multiprocessing.Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):
        
        self.memory_name = memory_name
        self.memory_size = memory_size
        self.app = app
        self.output = output
        self.shared_state = shared_state

        self.load_initial_modules()  # Load existing modules initially

        # Set up watchdog for the base folder
        event_handler = ModuleEventHandler(self)
        self.observer.schedule(event_handler, self.base_folder_path, recursive=True)
        self.observer.start()
        print("Monitoring modules...")

    def shutdown(self):
        self.observer.stop()  # Stop the observer
        self.observer.join()   # Wait for the observer thread to finish
        self.instance.close_instance()
        self.instance.shutdown()


class ModuleEventHandler(FileSystemEventHandler):
    def __init__(self, loader: Modules_MultiProcess):
        self.loader = loader

    def on_created(self, event):
        """Handle module creation."""
        if event.is_directory and 'main.py' in os.listdir(event.src_path):
            print(f"Detected new module: {event.src_path}")
            self.loader.load_initial_modules()  # Reload modules to include the new one

    def on_deleted(self, event):
        """Handle module deletion."""
        if event.is_directory:
            module_name = os.path.basename(event.src_path)
            print(f"Detected removal of module: {module_name}")
            # Remove the module from main_files and stop the process if needed
            self.loader.main_files = [mf for mf in self.loader.main_files if mf[0] != module_name]

    def on_modified(self, event):
        """Handle changes to existing modules."""
        if event.src_path.endswith('main.py'):
            module_name = os.path.basename(os.path.dirname(event.src_path))
            print(f"Detected modification in module: {module_name}")
            # Restart the process or handle as needed
            self.loader.load_initial_modules()
