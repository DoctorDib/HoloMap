import { NotificationTypeInterface } from '../Interfaces/StateInterface';

export const LogType = {
    Default: 'DEFAULT',
    Error: 'ERROR',
    Warning: 'WARNING',
    UserInput: 'USER_INPUT',
};

export const PageEnum = {
    Dashboard: 0,
};

export const DataActionEnum = {
    // Misc
    LOAD: '11',
    LOAD_SUCCESS: '12',
    SET: '13',
    SET_SUCCESS: '14',
    UPDATE: '15',

    // Websocket
    Socket_Initialise: '20',
    Socket_SendData: '21',
    Socket_GetData: '22',
    Socket_Set: '23',

    // MISC
    Write_State: '30',
    Read_State: '31',
    Update_HeartBeat:'32',
    Update_Cached_Modules: '33',

    // System
    Update_Page: '40',
    View_Module: '41',
};


export const NotificationActionEnums = {
    NewNotification: '0',
};

export const NotificationTypes: NotificationTypeInterface = {
    Info: 0,
    Success: 1,
    Warning: 2,
    Error: 3,
};

export enum PagesEnum {
    Logs = 0,
    SelectedModule = 1,
    Camera = 2,
}

export enum ModuleStateEnum {
    SET_INIT = "SET_INIT_EVENT",
    INITIALISING = "INITIALISING",
    
    RUNNING = "RUNNING",
    
    RESUMING = "RESUMING",
    
    SET_PAUSE = "SET_PAUSE_EVENT",
    PAUSING = "PAUSING",
    PAUSED = "PAUSED",
    
    SET_STOP = "SET_STOP_EVENT",
    STOPPING = "STOPPING",
    STOPPED = "STOPPED",
    
    SET_RELOAD = "SET_RELOAD",
    RELOADING = "RELOADING",
    RELOADED = "RELOADED",

    ERRORED = "ERRORED",
    DISABLED = "DISABLED",
    MISSING = "MISSING",
    
    NULL = "NULL",
}