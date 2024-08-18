from threading import Thread, Event
from datetime import datetime

import logger

class ThreadInstance:
    thread : Thread
    key : str = ''
    is_running = Event()
    start_time : datetime = datetime.now()

    def __init__(self, _key, _action):
        self.initialise(_key, _action)

    def stop(self):
        logger.info("{0} thread: Shutting down thread".format(self.key))
        self.is_running.clear()
        self.thread.join()

    def start(self):
        # Ensuring it is not running more than once
        if (self.is_running.is_set()):
            return
        logger.info("{0} thread: Initialising thread".format(self.key))
        self.start_time = datetime.now()
        self.is_running.set()
        try:
            self.thread.start()
        except Exception as e:
            logger.exception(e)

    def initialise(self, _key, _action):
        try:
            # Ensuring it is not running more than once
            if (self.is_running.is_set()):
                logger.info("{0} thread: Thread is already running".format(_key))
                return

            self.key = _key
            self.thread = Thread(target=_action, args=([self.is_running]), daemon=True)
            self.start()
        except Exception as e:
            logger.exception(e)

class ThreadController:
    threads = {}

    def __init__(self):
        self.initialise()

    def initialise(self):
        self.threads = {}

    def new_thread(self, _key, _action):
        if (_key in self.threads):
            if (not self.threads[_key].is_running):
                self.threads[_key].start()
            logger.warning("Multiple key thread attempt detected")
            # thread already active - no need to create new instance
            return

        new_thread = ThreadInstance(_key, _action)
        self.threads.update({_key: new_thread})
    
    def stop(self, _key):
        self.threads[_key].stop()

    def remove_thread(self, _key):
        self.stop(_key)
        del self.threads[_key]

    def remove_all(self):
        self.stop_all()
        self.initialise()

    def stop_all(self):
        for thread_key in self.threads:
            self.threads[thread_key].stop()