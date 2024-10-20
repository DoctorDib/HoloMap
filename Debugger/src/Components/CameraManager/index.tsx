import React, { useEffect, useState } from 'react';

import './camera_manager_style.scss';
import axios from 'axios';
import ToggleButtonComponent from '../Inputs/ToggleButton';
import { useSelector } from 'react-redux';
import { StateTypes } from '../../Interfaces/StateInterface';
import classNames from 'classnames';
import SliderComponent from '../Inputs/Slider';
import ButtonComponent from '../Inputs/Button';
import Icons from '../../Common/Icons';

interface CameraState {
    [key: string]: string;
}

interface CameraManagerInterface {
    isFullScreen: boolean,
}

const CameraManagerComponent = ({ isFullScreen }: CameraManagerInterface): React.ReactElement => {
    const debugMode: boolean = useSelector((state: StateTypes): boolean => state.root.debug_mode);

    const [cameraStates, setCameraStates] = useState<CameraState>({});
    const [cameraLabels, setCameraLabels] = useState<Array<string>>([]);
    const [activeCamera, setActiveCamera] = useState<any>({});
    const [shouldCapture, setShouldCapture] = useState<boolean>(false);
    const [refreshRate, setRefreshRate] = useState<number>(150);

    const fetchCameraImages = async () => {
        try {
            const response = await axios.get(`http://${window.location.hostname}:5000/get/` + Object.keys(activeCamera).join(','));

            const data = response.data;
            setCameraStates(data);
        } catch (error) {
            console.error('Error fetching webcam images:', error);
        }
    };

    const fetchCameraKeys = async () => {
        try {
            const response = await axios.get(`http://${window.location.hostname}:5000/get/camera_keys`);

            const data = response.data;
            if (data.length !== cameraLabels.length) {
                setCameraLabels(data);
            }
        } catch (error) {
            console.error('Error fetching webcam keys:', error);
        }
    };

    useEffect(() => {
        // Update cameras
        let intervalId: any; // Declare intervalId outside the condition
    
        if (debugMode && shouldCapture) {
            intervalId = setInterval(() => {
                fetchCameraImages();
            }, refreshRate);
        }
    
        // Clean up function to clear the interval
        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [cameraLabels, debugMode, shouldCapture, refreshRate]);

    useEffect(() => {
        let intervalId: any; // Declare intervalId outside the condition
    
        if (debugMode) {
            intervalId = setInterval(() => {
                fetchCameraKeys();
            }, 1000);
        }
    
        // Clean up function to clear the interval
        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [debugMode]);

    useEffect(() => {
        // Enable or disable the interval based on the debug mode and if any cameras are selected
        setShouldCapture(Object.keys(activeCamera).length > 0);
    }, [activeCamera]);

    const toggleCamera = (cameraName: string) => {
        if (activeCamera.hasOwnProperty(cameraName)) {
            let newActiveCamera = {...activeCamera};
            delete newActiveCamera[cameraName];
            newActiveCamera = Object.fromEntries(
                Object.entries(newActiveCamera).sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
            );
            setActiveCamera(newActiveCamera);
            return;
        } else {

            let newList = {
                ... activeCamera,
                [cameraName]: true,
            };

            newList = Object.fromEntries(
                Object.entries(newList).sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
            );

            setActiveCamera(newList);
        }
    };

    const formatName = (name: string): string => name
        .split('_') // Split the string by underscores
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
        .join(' ') // Join the words back together with a space
        .replace('Camera Base64', '');

    const toggleAllCameras = () => {
        if (Object.keys(activeCamera).length !== cameraLabels.length) {
            let newActiveCamera:any = {};
            cameraLabels.map((key: string) => {
                newActiveCamera[key] = true;
            });
            setActiveCamera(newActiveCamera);
            return;
        }

        setActiveCamera({});
    };

    return <>
        <div className={'camera-container'}>
            <div className={classNames('camera', isFullScreen ? 'camera-fullscreen' : '')}>
                {
                    Object.keys(activeCamera).map((key: string) => {
                        return (
                            <div className={'image-container'}>
                                <img src={`data:image/jpeg;base64,${cameraStates[key]}`} alt={formatName(key) + "       camera"} />
                                <div className={'image-title'}>
                                    {formatName(key)}
                                </div>
                            </div>
                        );
                    })
                }

                <div className={'refresh-rate-container'}>
                    <SliderComponent Min={50} Max={550} Value={refreshRate} Step={100} OnChange={(newVal) => setRefreshRate(newVal)} Text={"Refresh Rate"}/>
                </div>
            </div>

            <div className={'camera-controller'}>
                <div style={{ margin: '0 10px' }}> 
                    <ButtonComponent ClassName={'toggle-cameras'} Icon={Icons.Power} OnClick={() => toggleAllCameras()} />
                </div>
                {
                    cameraLabels.map((key: string) => {
                        return (
                            <div key={key} className={'module'}>
                                <ToggleButtonComponent ClassName={'camera-button'} Text={formatName(key)} OnClick={() => toggleCamera(key)} IsActive={activeCamera.hasOwnProperty(key)} />
                            </div>
                        );
                    })
                }   
            </div>
        </div>
    </>;
};

export default CameraManagerComponent;