import { useState } from 'react';

import './full-screen-style.scss';
import ButtonComponent from '../Inputs/Button';
import Icons from '../../Common/Icons';

const FullscreenToggle = () => {
    const [isFullscreen, setIsFullscreen] = useState(false);

    const toggleFullscreen = () => {
        if (!isFullscreen) {
            // Enter fullscreen mode
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            }
        } else {
            // Exit fullscreen mode
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }

        setIsFullscreen(!isFullscreen);
    };

    return (
        <ButtonComponent CustomStyle={{ backgroundColor: isFullscreen ? '#131330' : 'black' }} Icon={Icons.Compress} OnClick={() => toggleFullscreen()} />
    );
};

export default FullscreenToggle;