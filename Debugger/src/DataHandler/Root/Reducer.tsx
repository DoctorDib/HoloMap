import { DataActionEnum, PagesEnum } from '../../Common/enumerations';
import { RootTypes } from '../../Interfaces/StateInterface';
import createSocket from './SocketHandler';

const initialResultState : RootTypes = {
    initialTime: undefined,
    socket: undefined,
    heartbeat: undefined,
    modules: undefined,
    logs: undefined,
    debug_mode: false,
    currentPage: undefined,
    viewModule: undefined,
    cached_modules: undefined,
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
                initialTime: action.initialTime,
                heartbeat: action.heartbeat,
                modules: action.modules,
                settings: action.settings,
                currentPage: PagesEnum.Logs,
            };

        case DataActionEnum.Write_State:
            return {
                ...state,
                [action.data.key]: action.data.value,
            };

        case DataActionEnum.Update_HeartBeat:
            let logs = action.data.data.logs.Logs;
            logs.reverse();

            return {
                ...state,
                heartbeat: action.data.data.heartbeat,
                modules: action.data.data.modules,
                logs: {
                    ...action.data.data.logs,
                    Logs: logs
                },
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

        case DataActionEnum.Update_Page:
            return {
                ...state,
                currentPage: action.data,
            };

        case DataActionEnum.View_Module:
            return {
                ...state,
                currentPage: PagesEnum.SelectedModule,
                viewModule: action.data,
            }

        case DataActionEnum.Update_Cached_Modules:
            return {
                ...state,
                cached_modules: action.data,
            }
     
        default:
            return { ...state };
    }
};

export default reducer;