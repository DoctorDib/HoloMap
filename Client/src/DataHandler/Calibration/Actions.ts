import * as utils from '../handler';

import { DataActionEnum } from '../../Common/enumerations';
import { getStore } from '../../Stores/store';

export const webcamSetEdit = async (state: boolean) => {
    // Updating database
    await utils.sendData('/calibration/edit/set', { 
        calibration: {
            edit: state,
            type: 'WEBCAM',
        },
    });
    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.Webcam_SetEdit,
        edit: state,
    });
};

export const webcamSetBoundary = async (state: object) => {
    // Updating database
    await utils.sendData('/calibration/boundary/set', { 
        calibration: {
            cached_boundary: state,
            type: 'WEBCAM',
        },
    });
    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.Webcam_SetBoundary,
        cached_boundary: state,
    });
};

export const projectorSetEdit = async (state: boolean) => {
    // Updating database
    await utils.sendData('/calibration/edit/set', { 
        calibration: {
            edit: state,
            type: 'PROJECTION',
        },
    });
    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.Projector_SetEdit,
        edit: state,
    });
};

export const projectorSetBoundary = async (state: object) => {
    // Updating database
    await utils.sendData('/calibration/boundary/set', { 
        calibration: {
            cached_boundary: state,
            type: 'PROJECTION',
        },
    });
    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.Projector_SetBoundary,
        cached_boundary: state,
    });
};

export const webcamGetCalibration = async () => {
    // Updating database
    const response = await utils.sendData('/calibration/get', { 
        calibration: {
            type: 'WEBCAM',
        },
    });
    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.Webcam_GetCalibration,
        webcam: response,
    });
};

export const projectorGetCalibration = async () => {
    // Updating database
    const response = await utils.sendData('/calibration/get', { 
        calibration: {
            type: 'PROJECTION',
        },
    });
    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.Projector_GetCalibration,
        projector: response,
    });
};

export const getCalibrations = async () => {
    // Updating database
    const response = await utils.sendData('/calibration/get/all');

    console.log('getting all calibrations', response);

    // Updating local data
    return getStore().dispatch({
        type: DataActionEnum.GetCalibrations,
        calibrations: response,
    });
};

export const saveCalibration = async () => {
    // Updating database
    await utils.sendData('/calibration/set/all');
    // Getting the newely saved calibrations
    getCalibrations();
};