import { DataActionEnum } from '../../Common/enumerations';
import { RootTypes } from '../../Interfaces/StateInterface';
import createSocket from './SocketHandler';

const initialResultState : RootTypes = {
    logs: [],
    settings: {},
    socket: undefined,
    qr: undefined,
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


        case DataActionEnum.QR_SetDetectionList:
            // console.log(state);
            return {
                ...state,
                qr: {
                    ... state.qr,
                    detected_qrs: action.data.data,
                },
            };
    }
};

export default reducer;