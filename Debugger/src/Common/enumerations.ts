import { NotificationTypeInterface } from '../Interfaces/StateInterface';

const LogType = {
    Default: 'DEFAULT',
    Error: 'ERROR',
    Warning: 'WARNING',
    UserInput: 'USER_INPUT',
};

const PageEnum = {
    Dashboard: 0,
};

const DataActionEnum = {
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
    Update_HeartBeat:'32'
};


const NotificationActionEnums = {
    NewNotification: '0',
};

const NotificationTypes: NotificationTypeInterface = {
    Info: 0,
    Success: 1,
    Warning: 2,
    Error: 3,
};

export {
    LogType,
    PageEnum,
    DataActionEnum,
    NotificationTypes,
    NotificationActionEnums,
};