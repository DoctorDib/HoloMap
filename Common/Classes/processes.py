from multiprocessing import Process, Queue, Event

import logger

class ProcessInstance:
    def __init__(self, _key, _action, args=None):
        self.key = _key
        self._action = _action
        self.queue = Queue()
        self.system_command_queue = Queue()
        self.shutdown_event = Event()  # Event to signal shutdown
        self.process = Process(target=self._action, args=(self.queue, self.system_command_queue, self.shutdown_event))
        self.initialise(_key, _action, args)

    def initialise(self, _key, _action, args_input=None):
        try:
            if args_input is not None:
                self.queue.put(args_input)  # Pass arguments to process if needed

            self.start()
        except Exception as e:
            logger.exception(e)

    def start(self):
        logger.info(f"{self.key} Process: Initialising process")
        self.process.start()

    def graceful_shutdown(self):
        self.shutdown_event.set()  # Signal the process to shut down

    def stop(self):
        logger.info(f"{self.key} Process: Shutting down process")
        self.graceful_shutdown()
        #self.process.join()  # Wait for the process to exit

class ProcessController:
    processes = {}

    def __init__(self):
        self.initialise()

    def initialise(self):
        self.processes = {}

    def new_process(self, _key, _action, args = None):
        print(5)
        if (_key in self.processes):
            print(6)
            if (not self.processes[_key].is_running):
                self.processes[_key].start()
            logger.warning("Multiple key process attempt detected")

            # thread already active - no need to create new instance
            return

        new_multiple_process = ProcessInstance(_key, _action, args)
        self.add_process(_key, new_multiple_process)

    def add_process(self, _key, process):
        self.processes.update({_key: process})
    
    def stop(self, _key):
        print("Stopping: ", _key)
        self.processes[_key].stop()

    def remove_thread(self, _key):
        self.stop(_key)
        del self.processes[_key]

    def remove_all(self):
        self.stop_all()
        self.initialise()

    def stop_all(self):
        for process_key in self.processes:
            self.processes[process_key].stop()