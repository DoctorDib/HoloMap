from multiprocessing import Queue
import multiprocessing
import os
import time
from API.shared_state import DebugModeFlagFactory
from Common.Plugins import PluginLoader
import cv2
from flask import Flask
import logger

from Common.ModuleHelper import ModuleHelper

class Health_Module(ModuleHelper):
    def __init__(self, memory_name: str = None, memory_size: int = None,
                app: Flask = None, output: Queue = None, shared_state: multiprocessing.managers.SyncManager.dict = None):

        super().__init__("Health", parent_memory_name=memory_name, app=app, output=output, shared_state=shared_state)

    def prep(self):
        root_path = os.path.dirname(__file__)
        self.plugin_manager = PluginLoader(root_path, self.shared_state, self.output)
        self.plugin_manager.monitor_plugins() # Watching for new or removed plugins
        
        super().prep()
        
    def run(self):
        self.prep()

        try:
            while not self.shutdown_event.is_set():
                time.sleep(self.timeout_buffer)
                
                # NOTE - Temporarily disabling for now as I don't really want it 
                #        to send info when in debug mode.
                # Run all plugins that are not for debug only
                # for plugin_key in self.plugin_manager.loaded_plugins.keys():
                #     if ("DebugOnly" not in plugin_key):
                #         self.plugin_manager.loaded_plugins[plugin_key].run()
                        
                # Run all plugins that are for only debug
                with DebugModeFlagFactory(self.shared_state, read_only=True) as debugState:
                    if (debugState.value):
                        for plugin_key in self.plugin_manager.loaded_plugins.keys():
                            if ("DebugOnly" in plugin_key):
                                self.plugin_manager.loaded_plugins[plugin_key].run()
        except Exception as e:
            logger.error(e)
        finally:
            logger.info("Shutting down")
            cv2.destroyAllWindows()