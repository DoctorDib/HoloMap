import React from 'react';

import '../App.scss';

import DisplayComponent from '../Components/Display';
import Spotlight from '../Components/QR/Spotlight';

const SandboxPage = (): React.ReactElement => {
    return (<>
        <div style={{ background: 'black', width:'1920', height:'100vh' }} >
            
            <DisplayComponent content={
                <Spotlight/>
            }/>
        </div>
    </>);
};

export default SandboxPage;