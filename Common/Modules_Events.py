import os

from watchdog.events import FileSystemEventHandler

class ModuleEventHandler(FileSystemEventHandler):
    def __init__(self, loader: any):
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
# |