import React from 'react';

import './modules_controller_style.scss';
import ToggleButtonComponent from '../Inputs/ToggleButton';
import { WriteState } from '../../DataHandler/Root/Actions';
import { HeartBeat, StateTypes } from '../../Interfaces/StateInterface';
import { useSelector } from 'react-redux';

const ModulesControllerComponent = (): React.ReactElement => {

    const heartbeat: HeartBeat = useSelector((state: StateTypes): HeartBeat => state.root.heartbeat);
    
    const CheckColour = (key: string) => {
        const moduleName = key.split('_')[0]

        const heartbeatKey = moduleName + '_module_heartbeat';
        const lastHeartbeatTick = heartbeat[heartbeatKey];
        const timeDifference = (Date.now() / 1000) - lastHeartbeatTick;
        return timeDifference > (18 + 1) ? '#FF3333' : timeDifference > (8 + 1) ? '#ff8533' : '#28A745';
    }
    
    return <>
        <div className={'module-control'}> 

            <div className={'module-title'}>Module Control</div>

            <div className={'module-list'}>
            {
                Object.keys(heartbeat ?? {}).map((key: string) => {
                    if (key.includes('is_active')) {
                        return (
                            <div key={key} className={'module'}>
                                <ToggleButtonComponent key={key} Text={key.split('_')[0]} IsActive={heartbeat[key]} OnClick={(isActive: boolean) => WriteState(key, !isActive)} />
                                <div className={'status'} style={{ backgroundColor: CheckColour(key) }}/>
                            </div>
                        );
                    }
                })
            }
            </div>
        </div>
    </>;
};

export default ModulesControllerComponent;