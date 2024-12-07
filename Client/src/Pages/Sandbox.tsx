import React from 'react';

import '../App.scss';

import DisplayComponent from '../Components/Display';
import Spotlight from '../Components/Spotlight';
import CornerMarkComponent from '../Components/CornerMark';
import CommandButtonsComponent from '../Components/CommandButtons';
import CursorComponent from '../Components/Cursor';
import NotificationComponent from '../Components/Toast';
import AspectContainerComponent from '../Components/AspectContainer';

const SandboxPage = (): React.ReactElement => {
    return (<>
        <div className={'sandbox'}>
            {/* <DisplayComponent content={
                <>
                    <div className={'project-stamp'}>
                        <img src={"http://" + window.location.host + "/favicon-transparent.png"} className={'logo'} />
                        <div className={'text'}> Project HOLOMAP: Sandbox </div>
                    </div>

                    <CommandButtonsComponent/>
                    <CursorComponent/>
                    <Spotlight/>

                    <CornerMarkComponent/>
                    <NotificationComponent/>                    
                </>
            }/> */}

            <DisplayComponent content={
                <>
                    {/* Header */}
                    {/* <AspectContainerComponent Width={'100%'} Height={'100%'}>
                        <div className={'top-toolbar'}> 
                            asdf
                        </div>
                    </AspectContainerComponent> */}

                    {/* Footer */}
                    <AspectContainerComponent Width={'100%'} Height={'100%'}>
                        <div className={'project-stamp'}>
                            <img src={"http://" + window.location.host + "/favicon-transparent.png"} className={'logo'} />
                            <div className={'text'}> Project HOLOMAP: Sandbox </div>
                        </div>

                        <img src={"http://" + window.location.host + "/favicon.png"} className={'logo'} />

                        <CornerMarkComponent/>

                        <CommandButtonsComponent/>
                    </AspectContainerComponent>
                </>
            }/>
        </div>
    </>);
};

export default SandboxPage;