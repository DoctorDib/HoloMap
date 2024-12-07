from datetime import date, datetime

from Common.Classes.processes import ProcessController

import logger

class Instance():

    def __init__(self):
        self.process_controller : ProcessController = ProcessController()
        self.init_time : datetime = datetime.now()
        
        self.is_active : bool = False

    def initialise(self):
        self.init_time = date.today()
        self.start_instance()
        self.is_active = True

    def shutdown(self):
        self.is_active = False

    def start_instance(self):
        self.is_active = True

    # Instance Process Controller
    def start_process(self, key, action = None, process = None, args = None):
        if action is not None:
            self.process_controller.new_process(key, action, args)
        if (process is not None):
            self.process_controller.add_process(key, process)
            return
    def stop_process(self, key):
        self.process_controller.stop(key)
    def stop_processes(self):
        self.process_controller.stop_all()

    def close_instance(self):
        # Closing and removing all processes
        self.process_controller.stop_all()
        self.process_controller.remove_all()

        # Stopping while loop for status checks
        # self.settings_controller.stop()