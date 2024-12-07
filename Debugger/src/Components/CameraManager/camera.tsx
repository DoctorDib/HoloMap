import React, { useEffect, useState } from 'react';

import './camera_manager_style.scss';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateTypes } from '../../Interfaces/StateInterface';
import ToggleButtonComponent from '../Inputs/ToggleButton';
import Icons from '../../Common/Icons';

interface CameraComponentInterface {
    CameraName: string,
    Rate: number,
    Disabled: boolean,
    DisplayNameTag: boolean,
}

const CameraComponent = ({ CameraName, Rate = 150, Disabled, DisplayNameTag = true }: CameraComponentInterface): React.ReactElement => {
    const debugMode: boolean = useSelector((state: StateTypes): boolean => state.root.debug_mode);

    const [image, setImage] = useState<string | null>(null);
    const [localDisable, setLocalDisable] = useState<boolean>(false);

    const fetchCameraImage = async () => {
        try {
            const response = await axios.get(`http://${window.location.hostname}:5000/get/` + CameraName);

            const data: Array<string> = Object.values(response.data);
            if (data.length > 0) {
                // Camera found
                setImage(data[0]);
            } else {
                // Camera not found
                setImage(null);
            }
        } catch (error) {
            console.error('Error fetching webcam images:', error);
        }
    };

    useEffect(() => {
        // Update cameras
        let intervalId: any; // Declare intervalId outside the condition
    
        if (debugMode && !Disabled && CameraName !== null && !localDisable) {
            intervalId = setInterval(() => {
                fetchCameraImage();
            }, Rate);
        }
    
        // Clean up function to clear the interval
        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [CameraName, Rate, Disabled, debugMode, localDisable]);

    const formatName = (name: string): string => (name ?? '')
        .split('_') // Split the string by underscores
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
        .join(' ') // Join the words back together with a space
        .replace('Camera Base64', '');

    return <>
        { Disabled ? null :
            <div className={'image-container'}>
                <img src={`data:image/jpeg;base64,${image}`} alt={formatName(CameraName) + "       camera"} />

                { DisplayNameTag ? (
                    <div className={'image-title'}>
                    {formatName(CameraName)}
                </div>
                ) : null }

                
                <ToggleButtonComponent ClassName={'disable-button'} Icon={localDisable ? Icons.Play : Icons.Pause} 
                                    IsActive={!localDisable} OnClick={() => setLocalDisable(!localDisable)}/>
            </div>
        }
        
    </>;
};

export default CameraComponent;