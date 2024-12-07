import React, { useEffect, useState } from 'react';

import './modules_controller_style.scss';
import { Module, Modules, StateTypes } from '../../Interfaces/StateInterface';
import { useSelector } from 'react-redux';
import axios from 'axios';
import CameraComponent from '../CameraManager/camera';
import SliderComponent from '../Inputs/Slider';
import Heartbeat from '../HeartBeat';
import { ShowModuleInfo } from '../../DataHandler/Root/Actions';
import classNames from 'classnames';
import LogItemComponent from '../LogsViewer/log-item';
import { getTimeAgoFromTimeStamp } from '../../Common/Helpers';

const MoudleInfoViewerComponent = ({ }) : React.ReactElement => {
    const modules: Modules = useSelector((state: StateTypes): Modules => state.root.cached_modules);
    const selectedModule: string = useSelector((state: StateTypes): string => state.root.viewModule);

    const [cameraName, setCameraName] = useState<string | null>(null);
    const [refreshRate, setRefreshRate] = useState<number>(150);
    
    const [module, setModule] = useState<Module>(null);

    const fetchCameraKeys = async (name: string) => {
        try {
            let found = false;
            const response = await axios.get(`http://${window.location.hostname}:5000/get/camera_keys`);

            const data = response.data;
            for (const cameraIndex in data) {
                const cameraName = data[cameraIndex];

                // Is has a camera to view
                if (cameraName.includes(name.toLowerCase())) {
                    found = true;
                    setCameraName(cameraName);
                }
            }

            if (!found) {
                setCameraName(null);
            }

        } catch (error) {
            console.error('Error fetching webcam keys:', error);
        }
    };

    useEffect(() => {
        if (selectedModule === null || selectedModule === undefined) {
            return;
        }

        const currentModule = modules[selectedModule]

        setModule(currentModule);
        fetchCameraKeys(currentModule?.Name);
    }, [selectedModule, modules]);

    return <div className={'module-info-container'}> 

        { selectedModule === null || selectedModule === undefined ? (<div className={'select-message'}> Please select a module... </div>) : null }

        { selectedModule === null || selectedModule === undefined ? null : (
            <div className={classNames(['left', 'info-container'])}> 
                <div className={'info-header'}>
                    <div className={classNames(['state', module?.State])}>{module?.State}</div>
                    <div className={'name'}>{module?.Name}</div>
                </div>
                <div className={'path'}>{module?.Path}</div>
                <div className={'last-updated'}>{getTimeAgoFromTimeStamp(module?.LastUpdated)}</div>
                

                <div className={'info'}>
                    <div className={'title'}> Parent: </div>
                    <div className={'link-value'} onClick={() => {
                        if (module?.ModuleParentName !== null && module?.ModuleParentName !== "") {
                            ShowModuleInfo(module?.ModuleParentName);
                        }
                    }}>
                        { module?.ModuleParentName !== "" ? module?.ModuleParentName : "N/A" }
                    </div>
                </div>

                <div className={'info'}> 
                    <div className={'title'}> Children: </div>
                    {
                        module?.Children == null || module?.Children === undefined || module?.Children.length === 0 ? "N/A" : module?.Children?.map((child: Module) => (
                            <div key={child.Name} className={'link-value'} onClick={() => ShowModuleInfo(child.Name)}> {child.Name} </div>
                        ))
                    }
                </div>

                <div className={'logs'}>
                    <LogItemComponent Logs={module?.Logs} />
                </div>

                <div className={'heartbeat'}>
                    <Heartbeat LastUpdated={module?.LastUpdated}/>
                </div>
            </div>
        )}
        
        { selectedModule === null || selectedModule === undefined ? null : (
            <div className={'right'}>  
                <div className={'top-right'} style={{ display: cameraName === null ? 'none' : 'flex'}}>
                    <CameraComponent CameraName={cameraName} Rate={refreshRate} Disabled={false} DisplayNameTag={false} />

                    <div className={'refresh-rate-container'}>
                        <SliderComponent Min={50} Max={550} Value={refreshRate} Step={100} OnChange={(newVal) => setRefreshRate(newVal)} Text={"Refresh Rate"}/>
                    </div>
                </div>
            </div>
        )}
    </div>
};

export default MoudleInfoViewerComponent;