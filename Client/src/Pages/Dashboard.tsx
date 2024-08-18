import React, { forwardRef } from 'react';

import '../App.scss';

import Config from '../Common/Config';
import { Layer, Projection, useProjection } from 'react-projection-mapping';

const LandingPage = forwardRef((): React.ReactElement => {
    const MainDashboard: React.ReactElement = (
        <div className={'dashboard-container'}>
            <div className={'dashboard-content'}>
                <div className={'watermark-container'}>
                    <img src={'http://' + window.location.host + '/favicon-transparent.png'} className={'header-icon'} />
                    <div className={'header'}>
                        <div className={'watermark-title'}> Dashboard </div>
                        <div className={'watermark-version'}> C.A.S.I v{ Config.version } </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const update = ({ values, action }: any) => {
        if (action === 'onEnd') {
            localStorage.setItem('projection', JSON.stringify(values));
        }
    };

    const {
        data,
    } = useProjection();

    return (<div className={'main-container'}>

        { MainDashboard }


        <div className={'dashboard-content-parent'}>
            <Projection data={ data } onChange={ update } edit={ true } enabled={ true }>
                <Layer id='total'>
                    <div style={{ background: 'white', width:'100%', height:'100%', display: 'flex', justifyContent: 'center', alignItems: 'center', border: '15px solid #0096FF' }}>
                        <img src="http://localhost:8080/favicon.png" style={{ width:'500px', height:'500px', marginLeft: 'auto', marginRight: 'auto', justifyContent: 'center', alignItems: 'center' }} />
                    </div>
                </Layer>;
            
            </Projection>
        </div>
    </div>);
});

LandingPage.displayName = 'LandingPage';
export default LandingPage;