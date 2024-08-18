import { io, Socket } from 'socket.io-client';
import { DataActionEnum } from '../../Common/enumerations';
import { RootTypes } from '../../Interfaces/StateInterface';
import { getStore } from '../../Stores/store';

const initialResultState : RootTypes = {
    logs: [],
    settings: {},
    socket: undefined,
    qr: undefined,
};

const reducer = (state = initialResultState, action: any = { }) => { // TODO - Better action types?
    const newState = { ...state };
    let socket : Socket;

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
            // const utestrl = window.location.origin;
            // TODO - Store this socket in the redux store?
            socket = io('localhost:5001');
            
            socket.on('connect', () => {
                console.log('Connected to the server!');
            });
            
            socket.on('set_data', (data) => {
                const parsedData = JSON.parse(data);

                if (parsedData.tag === 'QR_DETECTION') {
                    
                    getStore().dispatch({
                        type: DataActionEnum.QR_SetDetectionList,
                        data: parsedData,
                    });
                }
            });
            
            return {
                ...state,
                socket: socket,
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