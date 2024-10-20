import { DataActionEnum } from '../../Common/enumerations';
import { RootTypes } from '../../Interfaces/StateInterface';
import createSocket from './SocketHandler';

const initialResultState : RootTypes = {
    socket: undefined,
    heartbeat: undefined,
    logs: undefined,
    debug_mode: false,
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
                debug_mode: action.debug_mode,
                heartbeat: action.heartbeat,
                settings: action.settings,
            };

        case DataActionEnum.Write_State:
            return {
                ...state,
                [action.data.key]: action.data.value,
            };

        case DataActionEnum.Update_HeartBeat:
            console.log(action.data.logs)
            return {
                ...state,
                heartbeat: action.data,
                logs: action.data.logs,
            }

        case DataActionEnum.Socket_Initialise:
            return {
                ...state,
                socket: createSocket(),
            };
        case DataActionEnum.Socket_Set:
            return {
                ...state,
                socket: action.socket,
            };

        case DataActionEnum.Socket_SendData:
            if (!state.socket)
                return state;

            state.socket.emit('set_data', action.data);
            return state;
     
        default:
            return { ...state };
    }
};

export default reducer;