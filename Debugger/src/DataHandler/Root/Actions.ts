import * as utils from '../handler';
import { DataActionEnum } from '../../Common/enumerations';
import { getStore } from '../../Stores/store';

export const initialiseDataRequest = async (loadSocket = true): Promise<any> => { 
    getStore().dispatch({ type: DataActionEnum.LOAD });

    // Grabbing the initial data from the database
    const data: any = await utils.sendData('/initialise-debugger');
    if (data == undefined) {
        return;
    }

    const newData: any = {
        type: DataActionEnum.LOAD_SUCCESS,

        debug_mode: data.debug_mode,
        heartbeat: data.heartbeat,
        
        isError: false,
    };

    // Saving data
    getStore().dispatch(newData);
    
    if (loadSocket) {
        // Initialising WebSocket events
        console.log('Init socket');
        getStore().dispatch({ ...newData, type: DataActionEnum.Socket_Initialise });
    }
};

export const ReadState = async (key: string): Promise<any> => {
    try {
        const response = await fetch(`http://localhost:5000/read_state/${key}`);
        const data = await response.json();

        // Saving data
        getStore().dispatch({ type: DataActionEnum.Write_State, data: data });

        return data.data;
    } catch (error) {
        console.error('Error fetching the shared state:', error);
        return null;
    }
};

export const WriteState = async (key: string, value: any): Promise<any> => {
    try {
        const response = await fetch(`http://localhost:5000/write_state/${key}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ value: value }),
        });

        if (!response.ok) {
            // Handle error response from server
            const errorData = await response.json();
            console.error('Error writing to the shared state:', errorData);
            return;
        }

        
        const data = await response.json(); // Get response data if needed
        getStore().dispatch({ 
            type: DataActionEnum.Write_State, 
            data: {
                key: key, 
                value: value
            }
        });
        
        return data;
    } catch (error) {
        console.error('Error writing to the shared state:', error);
        return null;
    }
};