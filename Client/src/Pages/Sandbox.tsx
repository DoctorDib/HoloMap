import React from 'react';

import '../App.scss';

import DisplayComponent from '../Components/Display';
import Spotlight from '../Components/Spotlight';
import CornerMarkComponent from '../Components/CornerMark';
import CommandButtonsComponent from '../Components/CommandButtons';
import CursorComponent from '../Components/Cursor';
import NotificationComponent from '../Components/Toast';

const SandboxPage = (): React.ReactElement => {
    return (<>
        <div className={'sandbox'}>
            
            <DisplayComponent content={
                (<>
                    <div className={'project-stamp'}>
                        <img src="http://localhost:8080/favicon-transparent.png" className={'logo'} />
                        <div className={'text'}> Project HOLOMAP: Sandbox </div>
                    </div>

                    <CommandButtonsComponent/>
                    <CursorComponent/>
                    <Spotlight/>

                    <CornerMarkComponent/>
                    <NotificationComponent/>                    
                </>)
            }/>
        </div>
    </>);
};

export default SandboxPage;