import React, { useEffect, useRef, useState } from 'react';
import { Layer, Projection } from 'react-projection-mapping';

import './display_style.scss';
import { useSelector } from 'react-redux';
import { StateTypes } from '../../Interfaces/StateInterface';
import { getCalibrations, projectorSetBoundary } from '../../DataHandler/Calibration/Actions';
import AspectContainerComponent from '../AspectContainer';

interface DisplayComponentInterface {
    content: React.ReactElement,
}

const DisplayComponent = ({ content }: DisplayComponentInterface): React.ReactElement => {
    const projectorEdit: boolean = useSelector((state: StateTypes): boolean => state.calibrations.projector.edit);
    const readonlyBoundary: object = useSelector((state: StateTypes): object => state.calibrations.projector.readonly_boundary);

    const ref = useRef(null);

    const [localBoundary, setLocalBoundary] = useState<any>({});

    const update = (layerObj: any) => {
        if (layerObj.isEnd === true && projectorEdit) {

            // Setting in react store and database
            projectorSetBoundary(layerObj.layers);
        }
    };

    useEffect(() => {
        // Initial setting
        if (Object.keys(readonlyBoundary).length !== 0 && readonlyBoundary !== undefined) {
            // Only set if readonly_boundary is populated
            setLocalBoundary(readonlyBoundary);
        }
    }, [readonlyBoundary]);

    useEffect(() => { getCalibrations(); }, []);

    // Counntering a stretch
    // 16:9 ratio 
    // 1122 x 777 resolution
    // transform: scaleX(calc(16 / 9 / (1122 / 777))); /* Counteract the stretch */

    return <Projection data={localBoundary} onChange={ update } edit={ projectorEdit } enabled={ true }>
        <Layer id='main-content'>
            <div className={'projection-content'} ref={ref}>
                { content }
            </div>
        </Layer>
    </Projection>
};

export default DisplayComponent;