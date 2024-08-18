import * as utils from '../handler';
import { TaskEnum, DataActionEnum } from '../../Common/enumerations';
import { Dispatch } from 'redux';
import { getStore } from '../../Stores/store';

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
    }
};

export const initialiseDataRequest = async (): Promise<any> => { 

    console.log('sending');

    getStore().dispatch({ type: DataActionEnum.LOAD });

    console.log('sending');

    // const data: any = await utils.sendData('/initialise');

    // if (data == undefined) {
    //     return;
    // }

    const newData: any = {
        type: DataActionEnum.LOAD_SUCCESS,
        //logs: data.logs,
        //settings: data.settings,
        isError: false,
    };

    // if (newData.account === null)
    //     delete newData.account;

    // console.log(newData);

    // getStore().dispatch(newData);

    console.log('Init socket');
    // Initialising WebSocket events
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