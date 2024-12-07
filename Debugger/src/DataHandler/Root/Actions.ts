import * as utils from '../handler';
import { DataActionEnum, PagesEnum } from '../../Common/enumerations';
import { getStore } from '../../Stores/store';
import { Modules } from '../../Interfaces/StateInterface';

export const initialiseDataRequest = async (loadSocket = true): Promise<any> => { 
    getStore().dispatch({ type: DataActionEnum.LOAD });

    // Grabbing the initial data from the database
    const data: any = await utils.sendData('/initialise-debugger');
    if (data == undefined) {
        return;
    }

    const newData: any = {
        type: DataActionEnum.LOAD_SUCCESS,

        initialTime: data.start_time,
        debug_mode: data.debug_mode,
        heartbeat: data.heartbeat,
        modules: data.modules,
        
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
        const response = await fetch(`http://${window.location.hostname}:5000/read_state/${key}`);
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
        const response = await fetch(`http://${window.location.hostname}:5000/write_state/${key}`, {
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

export const WriteModuleSharedState = async (key: string, command: string): Promise<any> => {
    try {
        const response = await fetch(`http://${window.location.hostname}:5000/set/module/${key}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ value: command }),
        });

        if (!response.ok) {
            // Handle error response from server
            const errorData = await response.json();
            console.error('Error writing to the shared state:', errorData);
            return;
        }
        
        const data = await response.json(); // Get response data if needed

        initialiseDataRequest(false);
        
        return data;
    } catch (error) {
        console.error('Error writing to the shared state:', error);
        return null;
    }
};

export const ChangePage = async (pageEnum: PagesEnum) => {
    getStore().dispatch({ type: DataActionEnum.Update_Page, data: pageEnum });
};

export const ShowModuleInfo = async (module: string) => {
    getStore().dispatch({ type: DataActionEnum.View_Module, data: module });
};

export const UpdateCachedModules = async (modules: Modules) => {
    getStore().dispatch({ type: DataActionEnum.Update_Cached_Modules, data: modules });
};