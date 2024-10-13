import multiprocessing
import os
import importlib.util
import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Plugin: 
    # def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict):
    #     self.shared_state = shared_state
        
    def prep(self, shared_state: multiprocessing.managers.SyncManager.dict):
        self.shared_state = shared_state

    def run(self):
        pass

class PluginLoader:
    def __init__(self, path, shared_state: multiprocessing.managers.SyncManager.dict, output: multiprocessing.Queue = None):
        self.plugins_folder = os.path.join(path, 'Plugins')
        self.loaded_plugins = {}
        self.shared_state = shared_state
        self.output = output
        
        # Ensure the plugins folder exists
        if not os.path.exists(self.plugins_folder):
            os.makedirs(self.plugins_folder)

        # Load existing plugins
        self.load_existing_plugins()

    def load_existing_plugins(self):
        # Load all existing plugins in the plugins folder
        for file_name in os.listdir(self.plugins_folder):
            if file_name.endswith('.py'):
                self.load_plugin(os.path.join(self.plugins_folder, file_name))

    def run_through_plugins(self, *args):
        for plugin in self.loaded_plugins.values():
            plugin.run(*args)

    def load_plugin(self, file_path):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        if module_name in self.loaded_plugins:
            print(f"{module_name} is already loaded.")
            return

        # Load the plugin module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        
        # Check if the module has a class with the same name as the module
        if hasattr(plugin_module, module_name):
            plugin_class = getattr(plugin_module, module_name)

            # Instantiate the plugin class with shared_state
            if callable(plugin_class):
                plugin_instance = plugin_class(self.shared_state, self.output)  # Pass the shared_state to the constructor
                self.loaded_plugins[module_name] = plugin_instance
            else:
                logger.error(f"{module_name} is not callable.")
                return

            # Check if the instance has a `run` method
            if not hasattr(plugin_instance, 'run'):
                logger.error(f"Plugin {module_name} does not have a 'run' method.")
                raise Exception(f"Plugin {module_name} does not have a 'run' method.")
        else:
            logger.error(f"Plugin {module_name} does not have a class named '{module_name}'.")
            logger.info("(for above error) - Available attributes:", dir(plugin_module))
            

    def unload_plugin(self, module_name):
        if module_name in self.loaded_plugins:
            del self.loaded_plugins[module_name]
            print(f"Unloaded plugin: {module_name}")

    def monitor_plugins(self):
        event_handler = PluginEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, self.plugins_folder, recursive=False)
        observer.start()

        print("Monitoring plugins...")


class PluginEventHandler(FileSystemEventHandler):
    def __init__(self, loader):
        self.loader = loader

    def on_created(self, event):
        if event.is_directory:
            return
        
        print(f"Detected new plugin: {event.src_path}")
        self.loader.load_plugin(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        
        module_name = os.path.splitext(os.path.basename(event.src_path))[0]
        self.loader.unload_plugin(module_name)
