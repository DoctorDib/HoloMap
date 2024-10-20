import { io, Socket } from 'socket.io-client';
import { notifyError, notifySuccess } from '../Notifications/Actions';
import { getStore } from '../../Stores/store';
import { DataActionEnum } from '../../Common/enumerations';

interface SocketInterface {
    name: string, 
    tag: string,
    data: any
}

const createSocket = (): Socket => {
    // const utestrl = window.location.origin;
    // TODO - Store this socket in the redux store?
    const socket: Socket = io(`${window.location.hostname}:5001`);
    
    socket.on('connect', (): void => {
        console.log('Connected to the server!');
        notifySuccess('Connected to server!');
    });

    // Listen for disconnect event
    socket.on('disconnect', (reason: string): void => {
        console.log('Disconnected from the server:', reason);
        notifyError('Disconnected from server. Reason: ' + reason);
    });
    
    socket.on('set_data', (data: any): void => {
        const parsedData: SocketInterface = JSON.parse(data);

        RootSocketActions(parsedData);
    });

    return socket;
};

const RootSocketActions = (parsedData: SocketInterface): void => {
    switch (parsedData.tag) {
        case 'STATE_VALUE':
            return getStore().dispatch({
                type: DataActionEnum.Write_State,
                data: parsedData,
            });
        case 'HEARTBEAT':
            return getStore().dispatch({
                type: DataActionEnum.Update_HeartBeat,
                data: parsedData.data,
            });
    }
};

const PCStatsSocketActions = (parsedData: SocketInterface): void => {
    switch (parsedData.tag) {
        case 'STATE_VALUE':
            return getStore().dispatch({
                type: DataActionEnum.Write_State,
                data: parsedData,
            });
    }
};



export default createSocket;