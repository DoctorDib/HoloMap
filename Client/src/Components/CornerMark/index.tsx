import React, { useEffect, useState } from 'react';

import './corner_mark_style.scss';
import { StateTypes } from '../../Interfaces/StateInterface';
import { useSelector } from 'react-redux';
import ButtonComponent from '../Inputs/Button';
import { projectorSetEdit, webcamSetEdit } from '../../DataHandler/Calibration/Actions';

const CornerMarkComponent = (): React.ReactElement => {
    // Constant values
    const incrementValue = 15; // Value to increment markRedness by
    const interval = 500; // Time interval in milliseconds (1000ms = 1 second)

    const webcamEdit: boolean = useSelector((state: StateTypes): boolean => state.calibrations.webcam.edit);
    const projectorEdit: boolean = useSelector((state: StateTypes): boolean => state.calibrations.projector.edit);
    const cornerPoint: number = useSelector((state: StateTypes): number => state.calibrations.cornerPoint);

    const [transitionRedMarker, setTransitionRedMarker] = useState<boolean>(false);
    const [markRedness, setMarkRedness] = useState<number>(0); // markRedness ranges from 0 to 255
    const [justifyContent, setJustifyContent] = useState<string>('left');
    const [alignItems, setAlignItems] = useState<string>('flex-start');

    const ApplyNewPosition = async () => {
        // Finished aligning projector boundary
        await projectorSetEdit(false);
        // Moving to next phase to align webcam with new projector boundary
        await webcamSetEdit(true);
    };

    const CancelCalibration = async () => {
        // Finished aligning projector boundary
        await projectorSetEdit(false);
        // Moving to next phase to align webcam with new projector boundary
        await webcamSetEdit(false);
    };

    useEffect(() => {
        // Resetting markRedness to zero
        setMarkRedness(0);

        // Setting position of marker
        // Top left: 0
        // Top right: 1
        // Bottom right: 2
        // Bottom left: 3
        setJustifyContent((cornerPoint === 0 || cornerPoint === 3) ? 'left' : 'right');
        setAlignItems((cornerPoint === 0 || cornerPoint === 1) ? 'flex-start' : 'flex-end');
    }, [cornerPoint]);

    // Ensuring it'll keep attempting redness
    useEffect(() => {
        if (markRedness >= 255)
            setMarkRedness(0);
    }, [markRedness]);

    // Controlling 
    useEffect(() => {
        setMarkRedness(0);
        setTransitionRedMarker(webcamEdit);
    }, [webcamEdit]);

    // Effect to increase markRedness over time
    useEffect(() => {
        if (!transitionRedMarker) 
            return;

        const intervalId = setInterval(() => {
            console.log(markRedness);
            setMarkRedness((prev) => Math.min(prev + incrementValue, 255)); // Increment markRedness, max is 255
        }, interval);

        return () => clearInterval(intervalId);
    }, [transitionRedMarker]);

    return <div className={'corner-mark'} style={{ justifyContent: justifyContent, alignItems: alignItems, background: webcamEdit ? '#383838' : 'transparent' }}>
        <div className={'centered-item'}>
            {/* Apply button when python boundary active */}
            {
                webcamEdit ? ( <>
                    <div className={'animated-border'}/>

                    <div className={'title'}>
                        <div> Corner Alignment </div>
                        <div> Active </div>
                        <ButtonComponent Text={'Cancel'} OnClick={CancelCalibration} />
                    </div>    
                </>) : null
            }

            {/* Apply button when client boundary active */}
            {
                projectorEdit ? <div className={'button-parent'}>
                    <ButtonComponent Text={'Apply'} OnClick={ApplyNewPosition} />
                    <ButtonComponent Text={'Cancel'} OnClick={CancelCalibration} />
                </div> : null
            }
        </div>

        {/* Mark visible when aligning webcam border with new projector border */}
        {
            webcamEdit ? (<>
                <div className={'mark'} style={{ backgroundColor: `rgb(${markRedness}, 0, 0)` }}/>
            </>) : null
        }
    </div>;
};

export default CornerMarkComponent;