import React from 'react';

import './command_buttons_style.scss';
import ButtonComponent from '../Inputs/Button';
import { projectorSetEdit, webcamSetEdit } from '../../DataHandler/Calibration/Actions';

const CommandButtonsComponent = (): React.ReactElement => {
    // List of commands
    const TriggerCalibration = async () => {
        await projectorSetEdit(true);
        await webcamSetEdit(false);
    };
    
    const TriggerCalibrationWebcam = async () => {
        await projectorSetEdit(false);
        await webcamSetEdit(true);
    };
    
    return <div className={'command_buttons'}>
        <div className={'button-list'}>
            <ButtonComponent Text={'Calibrate'} OnClick={TriggerCalibration} />
            <ButtonComponent Text={'Calibrate Webcam'} OnClick={TriggerCalibrationWebcam} />
        </div>
    </div>;
};

export default CommandButtonsComponent;