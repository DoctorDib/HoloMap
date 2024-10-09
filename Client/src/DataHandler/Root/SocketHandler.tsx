import { io, Socket } from 'socket.io-client';
import { DataActionEnum } from '../../Common/enumerations';
import { getStore } from '../../Stores/store';
import { getCalibrations, projectorSetEdit, saveCalibration, webcamSetBoundary, webcamSetEdit } from '../Calibration/Actions';

interface SocketInterface {
    name: string, 
    tag: string,
    data: any
}

const createSocket = (): Socket => {
    // const utestrl = window.location.origin;
    // TODO - Store this socket in the redux store?
    const socket: Socket = io('localhost:5001');
    
    socket.on('connect', (): void => {
        console.log('Connected to the server!');
    });
    
    socket.on('set_data', (data: any): void => {
        const parsedData: SocketInterface = JSON.parse(data);

        QrSocketActions(parsedData);
        ArUcoSocketActions(parsedData);
        CalibrationSocketActions(parsedData);
        CursorSocketActions(parsedData);
    });

    return socket;
};

const QrSocketActions = (parsedData: SocketInterface): void => {
    switch (parsedData.tag) {
        case 'QR_DETECTION':
            return getStore().dispatch({
                type: DataActionEnum.QR_SetDetectionList,
                data: parsedData,
            });
        case 'CLEAR_QR':
            return getStore().dispatch({
                type: DataActionEnum.QR_EmptyDetectionList,
            });
    }
};

const ArUcoSocketActions = (parsedData: SocketInterface): void => {
    switch (parsedData.tag) {
        case 'ARUCO_DETECTION':
            return getStore().dispatch({
                type: DataActionEnum.ArUco_SetDetectionList,
                data: parsedData,
            });
        case 'CLEAR_ARUCO':
            return getStore().dispatch({
                type: DataActionEnum.ArUco_EmptyDetectionList,
            });
    }
};

const CursorSocketActions = (parsedData: SocketInterface): void => {
    switch (parsedData.tag) {
        case 'CURSOR_POINT':
            return getStore().dispatch({
                type: DataActionEnum.Cursor_Set,
                data: parsedData,
            });
        case 'CLEAR_CURSOR':
            return getStore().dispatch({
                type: DataActionEnum.Cursor_Reset,
            });
    }
};

const CalibrationSocketActions = (parsedData: SocketInterface): void => {
    switch (parsedData.tag) {
        case 'CALIBRATION_MOVE_MARKER':
            console.log('going to ', parsedData.data);
            return getStore().dispatch({
                type: DataActionEnum.NextCalibrationPoint,
                data: parsedData.data,
            });

        case 'CALIBRATION_COMPLETE':
            console.log(parsedData);

            webcamSetBoundary(parsedData.data);

            webcamSetEdit(false);
            projectorSetEdit(false); // ensuring all edits are done

            // Saving all caches calibrations over to the official read onlys
            saveCalibration();
            // Getting all calibrations
            getCalibrations();
    }
};

export default createSocket;