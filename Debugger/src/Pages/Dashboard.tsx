import React, { forwardRef, useEffect, useState } from 'react';

import '../App.scss';

import ButtonComponent from '../Components/Inputs/Button';
import ToggleButtonComponent from '../Components/Inputs/ToggleButton';
import { useSelector } from 'react-redux';
import { HeartBeat, StateTypes, SystemStats } from '../Interfaces/StateInterface';
import { WriteState } from '../DataHandler/Root/Actions';
import Icons from '../Common/Icons';
import RamUsageDoughnutComponent from '../Components/PcStats/Stats/RamUsageDoughnut';
import CpuUsageDoughnutComponent from '../Components/PcStats/Stats/CpuUsageDoughnut';
import classNames from 'classnames';
import CameraManagerComponent from '../Components/CameraManager';
import DiskUsageComponent from '../Components/PcStats/Stats/DiskUsage';
import GpuUsageComponent from '../Components/PcStats/Stats/GpuUsage';
import LogsComponent from '../Components/LogsViewer';
import ModulesControllerComponent from '../Components/Modules';

const LandingPage = forwardRef((): React.ReactElement => {

    const debugMode: boolean = useSelector((state: StateTypes): boolean => state.root.debug_mode);    
    const heartbeat: HeartBeat = useSelector((state: StateTypes): HeartBeat => state.root.heartbeat);
    const timeStamp: string = useSelector((state: StateTypes): string => state.root.heartbeat?.PcStats?.TimeStamp);
    const systemStats: SystemStats = useSelector((state: StateTypes): SystemStats => state.root.heartbeat?.PcStats?.SystemInfo);

    const [timeAgo, setTimeAgo] = useState<string>();
    const [cameraFullScreen, setCameraFullScreen] = useState<boolean>(false);
    const [time, setTime] = useState<string>("Loading time...");

    const getTimeAgo = (dateString: string) => {
        const date: any = new Date(dateString);
        const now: any = new Date();
        const secondsAgo = Math.floor((now - date) / 1000);

        let interval = Math.floor(secondsAgo / 31536000); // seconds in a year
        if (interval > 1) return `${interval} years ago`;
        
        interval = Math.floor(secondsAgo / 2592000); // seconds in a month
        if (interval > 1) return `${interval} months ago`;
        
        interval = Math.floor(secondsAgo / 86400); // seconds in a day
        if (interval > 1) return `${interval} days ago`;
        
        interval = Math.floor(secondsAgo / 3600); // seconds in an hour
        if (interval > 1) return `${interval} hours ago`;
        
        interval = Math.floor(secondsAgo / 60); // seconds in a minute
        if (interval > 1) return `${interval} minutes ago`;

        return `${secondsAgo} seconds ago`;
    };

    const formatTimestamp = (timestamp: string): string => {
        const date = new Date(timestamp);
        
        return date.toLocaleString('en-UK', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        });
    };

    function convertDateNowToClock() {
        const now = new Date(Date.now());
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
    
        return `${hours}:${minutes}:${seconds}`;
    }
    
    useEffect(() => {
        const intervalId = setInterval(() => {
            setTimeAgo(getTimeAgo(timeStamp));
        }, 5000);
    
        return () => clearInterval(intervalId); // Cleanup on unmount
    }, [timeStamp]); // Add dependencies if needed
    
    useEffect(() => {
        const intervalId = setInterval(() => {
            setTime(convertDateNowToClock());
        }, 1000);
    
        return () => clearInterval(intervalId); // Cleanup on unmount
    }, []); // Add dependencies if needed

    return (<div className={'parent'}>
        <ToggleButtonComponent ClassName={'power-button'} Icon={Icons.Power} IsActive={debugMode} OnClick={(isActive: boolean) => WriteState("debug_mode", !isActive)}/>

        <div className={'debugger-status'} style={{ display: debugMode ? 'none' : 'flex' }}>
            <div className={'title'}> Debugger Offline </div>
            <div className={'timestamp'}> {formatTimestamp(heartbeat?.PcStats?.TimeStamp) || 'N/A'} </div>
            <div className={'time-ago'}> {timeAgo || 'N/A'} </div>
        </div>

        <div className={'header'} style={{ display: debugMode ? 'flex' : 'none' }}>
            <div className={'title'}> {/* BLANK */} </div>
            <div className={'time'}> {time} </div>
            <div className={'title'}> Holomap Dashboard </div>
        </div>

        <div className={'main-container'} style={{ display: debugMode ? 'flex' : 'none' }}>
            <div className={'section-parent'} style={{ flexDirection: 'column' }}>
                <div className={'section'} style={{ flexGrow: 1, }}>
                    <div className={'navigation-button-container'}>
                        <ButtonComponent Icon={Icons.PieChart} OnClick={() => {}} />
                        <ButtonComponent Icon={Icons.Camera} OnClick={() => setCameraFullScreen(true)} />
                    </div>
                </div>
                <div className={'section'} style={{ flexGrow: 1 }}>
                    <GpuUsageComponent/>
                </div>
                <div className={'section'} style={{ flexGrow: 1 }}>
                    <DiskUsageComponent/>
                </div>
                <div className={'section'} style={{ flexGrow: 2 }}>
                <div className="system-info-container" style={{ padding: '50px 15px '}}>
                    <h3 className="system-info-title">System Information</h3>
                    <div className="system-info-last-updated">
                        Last Updated: <strong>{timeAgo}</strong>
                    </div>
                        <ul className="system-info-list">
                            <li className="system-info-item"><strong>Hostname:</strong> {systemStats?.Hostname || 'N/A'}</li>
                            <li className="system-info-item"><strong>IP Address:</strong> {systemStats?.IpAddress || 'N/A'}</li>
                            <li className="system-info-item"><strong>MAC Address:</strong> {systemStats?.MacAddress || 'N/A'}</li>
                            <li className="system-info-item"><strong>OS:</strong> {systemStats?.Os || 'N/A'}</li>
                            <li className="system-info-item"><strong>OS Version:</strong> {systemStats?.OsVersion || 'N/A'}</li>
                            <li className="system-info-item"><strong>Architecture:</strong> {systemStats?.Architecture || 'N/A'}</li>
                            <li className="system-info-item"><strong>Python Version:</strong> {systemStats?.PythonVersion || 'N/A'}</li>
                            <li className="system-info-item"><strong>Boot Time:</strong> {formatTimestamp(systemStats?.BootTime) || 'N/A'}</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div className={'section-parent'} style={{ flexDirection: 'column', flexGrow: 0 }}>
                <div className={'section'} style={{ flexGrow: 1 }}>
                    <LogsComponent/>
                </div>
                <div className={'section-child'}>
                    <div className={'section'} style={{ flexGrow: 1, marginLeft: 0 }}>
                        <RamUsageDoughnutComponent/>
                    </div>
                    <div className={'section'} style={{ flexGrow: 1, marginRight: 0 }}>
                        <CpuUsageDoughnutComponent/>
                    </div>
                </div>
            </div>
            <div className={'section-parent'} style={{ flexDirection: 'column', flexGrow: 0 }}>
                <div className={'section'} style={{ flexGrow: 0, background:'#2c254d'}}>
                    <img src="http://localhost:5002/favicon-transparent.png" style={{ width:'200px', height:'auto', margin: '20px 10px', justifyContent: 'center', alignItems: 'center' }} />
                </div>

                <div className={'section'} style={{ flexGrow: 1 }}>
                    <ModulesControllerComponent/>
                </div>
            </div>
            <div className={'section-parent'} style={{ flexDirection: 'column', width: '40vw', flexGrow: 1 }}>
                <div className={classNames('section', cameraFullScreen ? 'section-fullscreen' : '')}  style={{ flexGrow: 1 }}>
                    <ButtonComponent ClassName={'fullscreen'} Icon={Icons.Expand} OnClick={() => setCameraFullScreen(!cameraFullScreen)} />

                    <CameraManagerComponent isFullScreen={cameraFullScreen}/>
                </div>

                <div className={'backdrop'} style={{ display: cameraFullScreen ? 'block' : 'none'}} />
            </div>
        </div>
    </div>);
});

LandingPage.displayName = 'LandingPage';
export default LandingPage;