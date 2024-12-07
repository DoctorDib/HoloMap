import calendar
from enum import Enum
import time
from API.Logging.sql import Log, LogType
import logger
from datetime import datetime

class ScheduledEvent:
    def __init__(self, name: str):
        self.name: str = name
        self.is_scheduled: bool = False
        self.time: float = 0.0
        self.count: int = 0
        
    def do_check(self, last_update: float) -> bool:
        if (self.time is None):
            return
        
        if (self.is_scheduled and (last_update > self.time)):
            self.is_scheduled = False
            self.count += 1
            return True
        
        return False
    
    def toggle_schedule(self):
        if (self.is_scheduled):
            self.is_scheduled = False
            self.time = None
        else:
            self.is_scheduled = True
            self.time = time.time()
    
    def set_schedule(self, should_schedule):
        self.is_scheduled = should_schedule
        if (should_schedule):
            self.time = time.time()
            
    def to_json(self) -> object:
        return {
            "Name": self.name,
            "IsScheduled": self.is_scheduled,
            "Time": self.time,
            "Count": self.count
        }

class ModuleRunningStateEnum(str, Enum):
    """Is it a string because it is used in JSON
    """
    
    SET_INIT = "SET_INIT_EVENT"
    INITIALISING = "INITIALISING"
    
    RUNNING = "RUNNING"
    
    SET_PAUSE = "SET_PAUSE_EVENT"
    
    RESUMING = "RESUMING"
    
    PAUSING = "PAUSING"
    PAUSED = "PAUSED"
    
    SET_STOP = "SET_STOP_EVENT"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    
    SET_RELOAD = "SET_RELOAD"
    RELOADING = "RELOADING"
    RELOADED = "RELOADED"
    
    ERRORED = "ERRORED"
    DISABLED = "DISABLED"
    MISSING = "MISSING"
    
    NULL = "NULL"
    
    
class ModuleLog(Log):
    def __init__(self, message: str, type: LogType):
        self.message = message
        self.type = type
        self.date = calendar.timegm(time.gmtime())
        
    def to_json(self):
        return super().to_json()
    
class ModuleStates():
    def __init__(self):
        
        # Items will remain in this list until we start them back up
        self.shutdown_list = []
        
        # Items will remain in this list until they start up
        self.to_startup_list = []

class ModuleSharedState():
    def __init__(self, name: str, module_parent_name: str, path: str, should_start_paused: bool = False):
        self.name: str = name
        self.module_parent_name: str = module_parent_name
        self.path: str = path
        self.paused: bool = should_start_paused
        self.state: ModuleRunningStateEnum = ModuleRunningStateEnum.NULL
        
        # LOGS
        self.__logs: list[ModuleLog] = []
        self.__has_errors = False
        self.__has_warnings = False
        
        self.scheduled_init_modules: ScheduledEvent = ScheduledEvent("Initialise")
        self.scheduled_shutdown_modules: ScheduledEvent = ScheduledEvent("Shutdown")
        self.scheduled_pause_modules: ScheduledEvent = ScheduledEvent("Pause")
        self.scheduled_reload_modules: ScheduledEvent = ScheduledEvent("Reload")
        self.scheduled_resume_modules: ScheduledEvent = ScheduledEvent("Resume")
        
        self.last_updated: float = 0.0
        
        # self.config = Config()
        self.heatbeat_buffer = 0.5 # TODO - FIX? self.config.get_double('HEARTBEAT_BUFFER')
        
        self.log_info(f"Initialising {self.name} Module")
        # Setting the initialise event
        self.initialise()
        
    def log_error(self, *args):
        message = " ".join(map(str, args))
        message = f"{self.name}: {message}"
        
        new_log = ModuleLog(message, LogType.ERROR)
        
        self.__has_errors = True
        self.__logs.append(new_log)
        logger.error(message)
        
    def log_warning(self, *args):
        message = " ".join(map(str, args))
        message = f"{self.name}: {message}"
        
        new_log = ModuleLog(message, LogType.WARNING)
        
        self.__has_warnings = True
        self.__logs.append(new_log)
        logger.warning(message)
        
    def log_info(self, *args):
        message = " ".join(map(str, args))
        message = f"{self.name}: {message}"
        
        new_log = ModuleLog(message, LogType.INFO)
        
        self.__logs.append(new_log)
        logger.info(message)
        
    def initialise(self):
        self.state = ModuleRunningStateEnum.INITIALISING
        self.scheduled_init_modules.set_schedule(True)
    def reload(self):
        self.state = ModuleRunningStateEnum.RELOADING
        self.scheduled_reload_modules.set_schedule(True)
    def stop(self):
        self.state = ModuleRunningStateEnum.STOPPING
        self.scheduled_shutdown_modules.set_schedule(True)
    def cancel_stop(self):
        self.state = ModuleRunningStateEnum.RUNNING
        self.scheduled_shutdown_modules.set_schedule(False)
    def pause(self):
        self.state = ModuleRunningStateEnum.PAUSING
        self.scheduled_pause_modules.set_schedule(True)
    def play(self):
        self.state = ModuleRunningStateEnum.RESUMING
        self.scheduled_resume_modules.set_schedule(True)
        
    # TODO - Add an achknowledge system
    # def ackknowledge(self):
    #     self.__detected_error = False
    #     self.__detected_warning = False
    
    def clear_logs(self):
        self.ackknowledge()
        self.__logs = []
        self.__has_warnings = False
        self.__has_errors = False
        
    
    def heartbeat(self):
        # Do load and unload here
        
        # We only care to heart beat if the module is enabled
        if (self.paused):
            return
        
        now = time.time()
        # We only care about heartbeats every x seconds
        if ((now - self.last_updated) > self.heatbeat_buffer):
            # NOTE - Ensure that the return actions are always at the bottom
            
            # OTHER ACTIONS
            self.last_updated = now
            
            # RETURN ACTIONS
            # TODO - Return enums
            # Do checks here
            
    def check_scheduled_actions(self) -> bool:
        if (self.scheduled_init_modules.do_check(self.last_updated) and
            self.state == ModuleRunningStateEnum.INITIALISING):
            return True
        
        if (self.scheduled_shutdown_modules.do_check(self.last_updated) and
            self.state == ModuleRunningStateEnum.STOPPING):
            return True
        
        if (self.scheduled_pause_modules.do_check(self.last_updated) and
            self.state == ModuleRunningStateEnum.PAUSING):
            return True
        
        if (self.scheduled_reload_modules.do_check(self.last_updated) and 
            self.state == ModuleRunningStateEnum.RELOADING):
            return True
        
        if (self.scheduled_resume_modules.do_check(self.last_updated) and 
            self.state == ModuleRunningStateEnum.RESUMING):
            return True
        
        # No actions are required
        return False

    def logs_to_json(self):
        logs = []
        
        for log in self.__logs:
            logs.append(log.to_json())
            
        return logs
    
    def to_json(self) -> object:
        return {
            'Name': self.name,
            'Path': self.path,
            'LastUpdated': self.last_updated,
            'ModuleParentName': self.module_parent_name,
            
            'State': self.state,
            'Paused': self.paused,
            
            'ScheduledInitModules': self.scheduled_init_modules.to_json(),
            'ScheduledShutdownModules': self.scheduled_shutdown_modules.to_json(),
            'ScheduledPauseModules': self.scheduled_pause_modules.to_json(),
            'ScheduledReloadModules': self.scheduled_reload_modules.to_json(),
            'ScheduledResumeModules': self.scheduled_resume_modules.to_json(),
            
            # Logs
            'Logs': self.logs_to_json(),
            "HasWarnings": self.__has_warnings,
            "HasErrors": self.__has_errors,
        }