import React, { useEffect, useState } from 'react';
import { Layer, Projection } from 'react-projection-mapping';

import './display_style.scss';
import { useDispatch, useSelector } from 'react-redux';
import { StateTypes } from '../../Interfaces/StateInterface';
import { requestWithLogs } from '../../DataHandler/Actions/rootActions';
import { TaskEnum } from '../../Common/enumerations';

interface DisplayComponentInterface {
    content: React.ReactElement,
}

const DisplayComponent = ({ content }: DisplayComponentInterface): React.ReactElement => {
    
    const dispatch = useDispatch();

    const [items, setItems] = useState();
    
    const settings: any = useSelector((state: StateTypes): any => state.root.settings);

    const update = (layerObj: any) => {
        if (layerObj.isEnd === true && 'layers' in settings) {
            const further: any = {
                'key': 'layers',
                'value_obj': layerObj.layers,
            };

            dispatch(requestWithLogs(TaskEnum.SetSettingsField, further));
        }
    };

    useEffect(() => {
        if ('layers' in settings){
            setItems(settings.layers);
        }
    }, [settings]);

    return <Projection data={items} onChange={ update } edit={ true } enabled={ true }>
        <Layer id='main-content'>
            <div className={'projection-content'}>
                
                { content }

            </div>
        </Layer>;

    </Projection>;
};

export default DisplayComponent;