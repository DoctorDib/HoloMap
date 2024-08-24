from datetime import date, datetime

from API.Settings.sql import SettingsController
from Common.Classes.processes import ProcessController
from Common.Classes.threads import ThreadController

import logger

class Instance():
    process_controller : ProcessController = ProcessController()
    settings_controller : SettingsController = SettingsController()

    thread_controller : ThreadController = ThreadController()
    init_time : datetime = datetime.now()
    is_active : bool = False

    def __getitem__(self, *args, **kwargs):
        with self.is_active:
            super().__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        with self.is_active:
            super().__setitem__(*args, **kwargs)
    
    def refresh_instance(self, settings_list):
        self.settings_controller.refresh(settings_list)

    def initialise(self):
        logger.info("Initialising instance")
        self.init_time = date.today()
        self.start_instance()
        self.is_active = True

    def shutdown(self):
        self.is_active = False

    def start_instance(self):
        self.settings_controller.initialise()
        self.is_active = True

    # Instance Thread  Controller
    def start_thread(self, key, action):
        self.thread_controller.new_thread(key, action)
    def stop_thread(self, key):
        self.thread_controller.stop(key)
    def stop_threads(self):
        self.thread_controller.stop_all()

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
        print("Closing all instances in instance.py")
        # Closing and removing all processes
        self.process_controller.stop_all()
        self.process_controller.remove_all()

        # Closing and removing threads
        self.thread_controller.stop_all()
        self.thread_controller.remove_all()

        # Stopping while loop for status checks
        self.settings_controller.stop()