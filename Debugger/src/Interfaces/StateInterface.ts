import { Socket } from 'socket.io-client';

interface StateTypes {
    root: RootTypes,
    notification: NotificationQueueInterface,
}

interface RootTypes {
    socket?: Socket,
    debug_mode: boolean,
    heartbeat: HeartBeat
    logs: Logs
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
    TimeStamp: string
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