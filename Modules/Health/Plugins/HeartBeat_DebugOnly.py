import multiprocessing
import time

from config import Config
import logger

class HeartBeat_DebugOnly:
    
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, output: multiprocessing.Queue = None):
        self.shared_state = shared_state
        self.output = output
        
        self.config = Config()
        self.heatbeat_buffer = self.config.get_int('HEARTBEAT_BUFFER')
        self.last_heatbeat = 0
        self.interested_keys = ['PcStats', '_module_heartbeat', '_is_active']
        
        
    def check_time(self):
        now = time.time()
        if (now - self.last_heatbeat > self.heatbeat_buffer):
            self.last_heatbeat = now
            return True
        
        return False
        
    def run(self):
        # Only run every x seconds
        if (not self.check_time()):
            return
        
        self.collate_and_send()
        
    def collate_and_send(self):
        data = {}
        keys = self.shared_state.keys()
        for key in keys:
            if any(interested_key in key for interested_key in self.interested_keys):
                data[key] = self.shared_state[key]
                
        # Send over logs
        logs = logger.get_stored_logs().to_json()
        data['logs'] = {
            "LogCount": len(logs),
            "Logs": logs
        }
          
        self.output.put({
            "name": "Sending master heartbeat", 
            "tag": "HEARTBEAT",
            "data": data,
        })  