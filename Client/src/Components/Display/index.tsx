import React, { useEffect, useState } from 'react';
import { Layer, Projection } from 'react-projection-mapping';

import './display_style.scss';
import { useSelector } from 'react-redux';
import { StateTypes } from '../../Interfaces/StateInterface';
import { getCalibrations, projectorSetBoundary } from '../../DataHandler/Calibration/Actions';

interface DisplayComponentInterface {
    content: React.ReactElement,
}

const DisplayComponent = ({ content }: DisplayComponentInterface): React.ReactElement => {
    const projectorEdit: boolean = useSelector((state: StateTypes): boolean => state.calibrations.projector.edit);
    const readonlyBoundary: object = useSelector((state: StateTypes): object => state.calibrations.projector.readonly_boundary);

    const [localBoundary, setLocalBoundary] = useState<object>();

    const update = (layerObj: any) => {
        if (layerObj.isEnd === true && projectorEdit) {

            // Setting in react store and database
            projectorSetBoundary(layerObj.layers);
        }
    };

    useEffect(() => {
        console.log(readonlyBoundary);
        // Initial setting
        if (Object.keys(readonlyBoundary).length !== 0 && readonlyBoundary !== undefined) {
            
            // Only set if readonly_boundary is populated
            setLocalBoundary(readonlyBoundary);
        }
    }, [readonlyBoundary]);

    useEffect(() => { getCalibrations(); }, []);

    return <Projection data={localBoundary} onChange={ update } edit={ projectorEdit } enabled={ true }>
        <Layer id='main-content'>
            <div className={'projection-content'}>
                { content }
            </div>
        </Layer>;

    </Projection>;
};

export default DisplayComponent;