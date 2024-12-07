from datetime import datetime 
import multiprocessing
import time
import uuid
import re
import socket
import platform
import psutil
import GPUtil

import multiprocessing

from API.shared_state import PcStatsFactory

class PCStats_DebugOnly:
    
    def __init__(self, shared_state: multiprocessing.managers.SyncManager.dict, output: multiprocessing.Queue = None):
        self.shared_state = shared_state
        self.output = output
        
        # Getting PC info
        self.run_once()

    def get_system_info(self):
        return {
            "Os": platform.system(),
            "OsVersion": platform.version(),
            "Architecture": platform.architecture(),
            "Hostname": socket.gethostname(),
            "IpAddress": socket.gethostbyname(socket.gethostname()),
            "MacAddress": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            "PythonVersion": platform.python_version(),
            "BootTime": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        }
        
    def get_cpu_info(self):
        return {
            "PhysicalCores": psutil.cpu_count(logical=False),
            "TotalCores": psutil.cpu_count(logical=True),
            "CpuUsage": psutil.cpu_percent(interval=1),
            "CpuUsagePerCore": [f"{core}%" for core in psutil.cpu_percent(percpu=True, interval=1)],
        }
        
    def get_ram_info(self):
        virtual_mem = psutil.virtual_memory()
        
        return {
            "Total": virtual_mem.total,
            "Available": virtual_mem.available,
            "Used": virtual_mem.used,
            "Free": virtual_mem.free,
            "PercentUsed": virtual_mem.percent,
        }

    def get_disk_info(self):
        disk_info = psutil.disk_partitions()
        
        disks = []
        for disk in disk_info:
            try:
                usage = psutil.disk_usage(disk.mountpoint)._asdict()
                
                disks.append({
                    "Device": disk.device,
                    "MountPoint": disk.mountpoint,
                    "Fstype": disk.fstype,
                    "Usage": {
                        "Free": usage["free"],
                        "Total": usage["total"],
                        "Used": usage["used"],
                        "PercentUsed": usage["percent"],
                    }
                })
            except:
                # Bit locked device can cause an error
                pass
            
        return disks
    
    def get_network_info(self):
        net_io = psutil.net_io_counters()
        
        return {
            "BytesSent": net_io.bytes_sent,
            "BytesReceived": net_io.bytes_recv,
            "PacketsSent": net_io.packets_sent,
            "PacketsReceived": net_io.packets_recv,
            "ErrorsIn": net_io.errin,
            "ErrorsOut": net_io.errout,
        }
        
    def get_gpu_info(self):
        try:
            gpus_info = GPUtil.getGPUs()
            
            gpus = []
            for gpu in gpus_info:
                gpus.append(
                    {
                        "Id": gpu.id,
                        "Name": gpu.name,
                        "Load": gpu.load * 100,
                        "MemoryTotal": gpu.memoryTotal,
                        "MemoryUsed": gpu.memoryUsed,
                        "MemoryFree": gpu.memoryFree,
                        "Temperature": gpu.temperature,
                        "Uuid": gpu.uuid,
                    }
                )
        except Exception:
            return {
                "Gpus": "No GPU found or GPUtil not installed"
            }

        return gpus
    
    def get_static_info(self):
        return {
            "SystemInfo": self.get_system_info(),
            "TimeStamp": time.time()
        }
    
    def get_all_info(self):
        return {
            "CpuInfo": self.get_cpu_info(),
            "RamInfo": self.get_ram_info(),
            "DiskInfo": self.get_disk_info(),
            "NetworkInfo": self.get_network_info(),
            "GpuInfo": self.get_gpu_info(),
            "TimeStamp": time.time(),
        }

    def run_once(self):
        stats = self.get_static_info()
        with PcStatsFactory(self.shared_state, read_only=False) as pcStats:
            pcStats.value = stats
        
    def run(self):
        with PcStatsFactory(self.shared_state, read_only=False) as pcStats:
            new_stats = self.get_all_info()
            old_stats = pcStats.value
            old_stats.update(new_stats)    
            pcStats.value = old_stats
        