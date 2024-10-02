import React from 'react';
import { useSelector } from 'react-redux';

import './command_buttons_style.scss';
import ButtonComponent from '../Inputs/Button';
import { projectorSetBoundary, projectorSetEdit, saveCalibration, webcamSetEdit } from '../../DataHandler/Calibration/Actions';
import { StateTypes } from '../../Interfaces/StateInterface';

const CommandButtonsComponent = (): React.ReactElement => {    
    const webcamEdit: boolean = useSelector((state: StateTypes): boolean => state.calibrations.webcam.edit);
    const projectorEdit: boolean = useSelector((state: StateTypes): boolean => state.calibrations.projector.edit);

    // List of commands
    const Reset = async () => {
        await projectorSetEdit(false);
        await webcamSetEdit(false);

        projectorSetBoundary({
            'main-content': {
                corners: [
                    0, 0,
                    1920, 0,
                    0, 1080,
                    1920, 1080,
                ],
            },
        });

        saveCalibration();
    };

    const TriggerCalibration = async () => {
        await projectorSetEdit(true);
        await webcamSetEdit(false);
    };
    
    const TriggerCalibrationWebcam = async () => {
        await projectorSetEdit(false);
        await webcamSetEdit(true);
    };
    
    return <div className={'command_buttons'} style={{ display: webcamEdit || projectorEdit ? 'none' : 'flex' }}>
        <div className={'button-list'}>
            <ButtonComponent Text={'Reset'} OnClick={Reset} />
            <ButtonComponent Text={'Calibrate'} OnClick={TriggerCalibration} />
            <ButtonComponent Text={'Calibrate Webcam'} OnClick={TriggerCalibrationWebcam} />
        </div>
    </div>;
};

export default CommandButtonsComponent;