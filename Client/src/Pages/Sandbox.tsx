import React from 'react';

import '../App.scss';

import DisplayComponent from '../Components/Display';
// import Spotlight from '../Components/QR/Spotlight';
import CornerMarkComponent from '../Components/CornerMark';
import CommandButtonsComponent from '../Components/CommandButtons';

const SandboxPage = (): React.ReactElement => {
    return (<>
        <div className={'sandbox'}  >
            
            <DisplayComponent content={
                (<>
                    <div className={'project-stamp'}>
                        <img src="http://localhost:8080/favicon-transparent.png" className={'logo'} />
                        <div className={'text'}> Project HOLOMAP: Sandbox </div>
                    </div>

                    <CornerMarkComponent/>
                    
                    <CommandButtonsComponent/>
                </>)
            }/>
        </div>
    </>);
};

export default SandboxPage;