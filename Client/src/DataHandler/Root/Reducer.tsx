import { DataActionEnum } from '../../Common/enumerations';
import { RootTypes } from '../../Interfaces/StateInterface';
import createSocket from './SocketHandler';

const initialResultState : RootTypes = {
    logs: [],
    settings: {},
    socket: undefined,
    qr: undefined,
    cursor: undefined,
};

const reducer = (state = initialResultState, action: any = { }) => { // TODO - Better action types?
    const newState = { ...state };
    
    switch (action.type) {
        case DataActionEnum.LOAD:
            return {
                ...newState,
            };
        case DataActionEnum.LOAD_SUCCESS:
            return {
                ...newState,
                logs: action.logs,
                settings: action.settings,
            };

        case DataActionEnum.UPDATE_LOGS:
            return {
                ...newState,
                logs: [...state.logs, ...action.logs],
            };

        case DataActionEnum.Socket_Initialise:
            return {
                ...state,
                socket: createSocket(),
            };

        case DataActionEnum.Socket_SendData:
            if (!state.socket)
                return state;

            state.socket.emit('set_data', action.data);
            return state;
        default:
            return { ...newState };

        // QR
        case DataActionEnum.QR_SetDetectionList:
            return {
                ...state,
                qr: {
                    ... state.qr,
                    detected_qrs: action.data.data,
                },
            };
        case DataActionEnum.QR_EmptyDetectionList:
            return {
                ...state,
                qr: {
                    ... state.qr,
                    detected_qrs: [],
                },
            };

        // Cursor
        case DataActionEnum.Cursor_Set:
            if (action.data.data[0] === null)
                return;

            return {
                ...state,
                cursor: {
                    ... state.cursor,
                    x: action.data.data[0][0], // x
                    y: action.data.data[0][1], // y
                },
            };
        case DataActionEnum.Cursor_Reset:
            return {
                ...state,
                cursor: {
                    ... state.cursor,
                    x: null, 
                    y: null,
                },
            };
    }
};

export default reducer;