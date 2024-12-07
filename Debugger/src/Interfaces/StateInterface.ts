import { Socket } from 'socket.io-client';
import { PagesEnum } from '../Common/enumerations';

interface StateTypes {
    root: RootTypes,
    notification: NotificationQueueInterface,
}

interface RootTypes {
    initialTime: number,
    socket?: Socket,
    debug_mode: boolean,
    heartbeat: HeartBeat
    modules: Modules
    logs: Logs,
    currentPage: PagesEnum,
    viewModule: string,
    cached_modules: Modules,
}

interface Modules {
    [key: string]: Module
}

interface Module {
    Name: string,
    Path: string,
    LastUpdated: number,
    ModuleParentName: string,

    State: string,

    Paused: boolean,

    ScheduledInitModules: ScheduleEvents
    ScheduledShutdownModules: ScheduleEvents
    ScheduledPauseModules: ScheduleEvents
    ScheduledReloadModules: ScheduleEvents
    ScheduledResumeModules: ScheduleEvents
    
    // TODO - Support module logs to be the same as the interface logs
    // e.g. Array<Logs>
    Logs: Array<Log>,

    // Only used on the TypeScript side
    Children?: Module[]
}

interface ScheduleEvents {
    Name: string,
    IsScheduled: boolean,
    Time: number,
    Count: number,
}

interface HeartBeat {
    PcStats: PCStats
    [key: string]: any
}

interface Logs {
    Logs: Array<Log>,
    LogCount: number,
}

interface Log {
    date: number,
    type: string,
    message: string,
}

interface PCStats {
    SystemInfo: SystemStats
    CpuInfo: CpuStats
    RamInfo: RamStats
    DiskInfo: Array<DiskStats>
    NetworkInfo: NetworkStats
    GpuInfo: Array<GPUStat>
    TimeStamp: number
}

interface SystemStats {
    Os: string,
    OsVersion: string,
    Architecture: Array<string>,
    Hostname: string,
    IpAddress: string,
    MacAddress: string,
    PythonVersion: string,
    BootTime: string,
}

interface CpuStats {
    PhysicalCores: number,
    TotalCores: number,
    CpuUsage: number,
    CpuUsagePerCore: Array<string>,
}

interface RamStats {
    Total: number,
    Available: number,
    Used: number,
    Free: number,
    PercentUsed: number,
}

interface DiskStats {
    Device: string,
    MountPoint: string,
    Fstype: string,
    Usage: DiskUsageStats,
}

interface DiskUsageStats {
    Free: number,
    Total: number,
    Used: number,
    PercentUsed: number,
}

interface NetworkStats {
    BytesSent: number,
    BytesReceived: number,
    PacketsSent: number,
    PacketsReceived: number,
    ErrorsIn: number,
    ErrorsOut: number,
}

interface GPUStat {
    "Id": number,
    "Name": string,
    "Load": number,
    "MemoryTotal": number,
    "MemoryUsed": number,
    "MemoryFree": number,
    "Temperature": number,
    "Uuid": string,

}

interface NotificationInterface {
    message: string,
    type: number
}


// Notifications
interface NotificationTypeInterface {
    Info: number,
    Success: number,
    Warning: number,
    Error: number,
}

interface NotificationInterface {
    message: string,
    type: number
}

interface NotificationQueueInterface {
    queue: Array<NotificationInterface>
}

export {
    // Default
    StateTypes,
    RootTypes,

    // Logging
    Logs,
    Log,

    // Modules
    Modules,
    Module,

    // Notification pop ups
    NotificationTypeInterface,
    NotificationInterface,
    NotificationQueueInterface,

    // Health
    HeartBeat,
    PCStats,
    SystemStats,
    CpuStats,
    RamStats,
    DiskStats,
    NetworkStats,
    GPUStat,
    DiskUsageStats,
};