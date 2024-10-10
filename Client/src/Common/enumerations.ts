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

const TaskEnum = {
    InitialRequest: 11,

    // Logs
    UpdateLogs: 21,

    // Settings
    SetSettings: 31,
    SetSettingsField: 32,
    SetNewAccountSettings: 33,
};

const DataActionEnum = {
    // Misc
    LOAD: '11',
    LOAD_SUCCESS: '12',
    SET: '13',
    SET_SUCCESS: '14',
    UPDATE: '15',

    // Logs
    UPDATE_LOGS: '21',

    // Websocket
    Socket_Initialise: '30',
    Socket_SendData: '31',
    Socket_GetData: '32',
    Socket_Set: '33',

    // QR
    QR_SetDetectionList: '40',
    QR_EmptyDetectionList: '41',

    // Calbration
    Webcam_SetEdit: '51',
    Webcam_SetBoundary: '52',
    Webcam_GetCalibration: '53',
    
    Projector_SetEdit: '54',
    Projector_SetBoundary: '55',
    Projector_GetCalibration: '56',

    GetCalibrations: '58',
    NextCalibrationPoint: '59',
    CompleteCalibration: '510',

    // Cursor
    Cursor_Set: '61',
    Cursor_Reset: '62',

    // ArUco
    ArUco_SetDetectionList: '70',
    ArUco_EmptyDetectionList: '71',
};

const NotificationActionEnums = {
    NewNotification: '0',
};

const DialogActionEnums = {
    NewDialog: '0',
    ResetDialog: '1',
};

const ContextActionEnums = {
    SetXY: '0',
    SetVis: '1',
    SetOptions: '2',
};

const FormFieldTypeEnums = {
    TextInput: 11,
    Checkbox : 12,
    Extra: 13,
    NumberInput: 14,
    Splitter: 15,
    DropDown: 16,
    Header: 17,
    PasswordInput: 18,
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
    TaskEnum,
    DataActionEnum,
    FormFieldTypeEnums,
    NotificationTypes,
    NotificationActionEnums,
    DialogActionEnums,
    ContextActionEnums,
};