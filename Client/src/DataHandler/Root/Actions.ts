import * as utils from '../handler';
import { TaskEnum, DataActionEnum } from '../../Common/enumerations';
import { Dispatch } from 'redux';
import { getStore } from '../../Stores/store';
import { SETTINGS_BLANK } from '../../Common/blanks';

export const requestWithLogs = (requestEnum: number, data:any = null): any => async (dispatch: Dispatch) => {
    dispatch({ type: DataActionEnum.LOAD });

    if (data != null) {
        console.log(data);
    }

    switch (requestEnum) {
        // LOGS
        case TaskEnum.UpdateLogs:
            await utils.sendData('/cmd/update');
            return;

        // SETTINGS
        case TaskEnum.SetNewAccountSettings:
            await utils.sendData('/settings/set', { id_aesn: data, settings: SETTINGS_BLANK });
            return;
        case TaskEnum.SetSettings:
            await utils.sendData('/settings/set', { settings: data });
            return;
        case TaskEnum.SetSettingsField:
            await utils.sendData('/settings/field/set', { field: data });
            return;
    }
};

export const initialiseDataRequest = async (): Promise<any> => { 
    getStore().dispatch({ type: DataActionEnum.LOAD });

    // Grabbing the initial data from the database
    const data: any = await utils.sendData('/initialise');
    if (data == undefined) {
        return;
    }

    const newData: any = {
        type: DataActionEnum.LOAD_SUCCESS,

        logs: data.logs,
        settings: data.settings,
        calibrations: data.calibrations,
        
        isError: false,
    };

    // Saving data
    getStore().dispatch(newData);

    // Initialising WebSocket events
    console.log('Init socket');
    getStore().dispatch({ ...newData, type: DataActionEnum.Socket_Initialise });
};

// async (dispatch: Dispatch): Promise<void> => {
//     console.log('sending');

//     dispatch({ type: DataActionEnum.LOAD });

//     console.log('sending');

//     const data: any = await utils.sendData('/initialise');

//     const newData: any = {
//         type: DataActionEnum.LOAD_SUCCESS,
//         logs: data.logs,
//         settings: data.settings,
//         isError: false,
//     };

//     if (newData.account === null)
//         delete newData.account;

//     console.log(newData);

//     dispatch(newData);

//     console.log('Init socket');
//     // Initialising WebSocket events
//     getStore().dispatch({ ...newData, type: DataActionEnum.Socket_Initialise });
// };