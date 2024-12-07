import React, { forwardRef, useEffect, useState } from 'react';

import '../App.scss';

import ToggleButtonComponent from '../Components/Inputs/ToggleButton';
import { useSelector } from 'react-redux';
import { HeartBeat, StateTypes, SystemStats } from '../Interfaces/StateInterface';
import { ChangePage, WriteState } from '../DataHandler/Root/Actions';
import Icons from '../Common/Icons';
import RamUsageDoughnutComponent from '../Components/PcStats/Stats/RamUsageDoughnut';
import CpuUsageDoughnutComponent from '../Components/PcStats/Stats/CpuUsageDoughnut';
import CameraManagerComponent from '../Components/CameraManager';
import DiskUsageComponent from '../Components/PcStats/Stats/DiskUsage';
import GpuUsageComponent from '../Components/PcStats/Stats/GpuUsage';
import LogsComponent from '../Components/LogsViewer';
import ModulesControllerComponent from '../Components/Modules';
import MoudleInfoViewerComponent from '../Components/Modules/moduleInfo';
import { convertDateNowToClock, formatStringTimestamp, formatTimestamp, getTimeAgo, getTimeAgoFromTimeStamp } from '../Common/Helpers';
import { PagesEnum } from '../Common/enumerations';
import Heartbeat from '../Components/HeartBeat';
import Config from '../Common/Config';

const LandingPage = forwardRef((): React.ReactElement => {
    const debugMode: boolean = useSelector((state: StateTypes): boolean => state.root.debug_mode);    
    const initialTime: number = useSelector((state: StateTypes): number => state.root.initialTime);    
    const heartbeat: HeartBeat = useSelector((state: StateTypes): HeartBeat => state.root.heartbeat);
    const timeStamp: number = useSelector((state: StateTypes): number => state.root.heartbeat?.PcStats?.TimeStamp);
    const systemStats: SystemStats = useSelector((state: StateTypes): SystemStats => state.root.heartbeat?.PcStats?.SystemInfo);
    const currentPage: PagesEnum = useSelector((state: StateTypes): PagesEnum => state.root.currentPage);

    const [timeAgo, setTimeAgo] = useState<string>();
    const [time, setTime] = useState<string>("Loading time...");
    const [mainProcessBootTime, setMainProcessBootTime] = useState<string>("Loading boot time...");

    useEffect(() => {
        setMainProcessBootTime(getTimeAgoFromTimeStamp(initialTime));
        setTimeAgo(getTimeAgoFromTimeStamp(timeStamp));
    }, [heartbeat, time]);

    useEffect(() => {
        const intervalId = setInterval(() => setTime(convertDateNowToClock()), 1000);
    
        return () => clearInterval(intervalId); // Cleanup on unmount
    }, []); // Add dependencies if needed

    return (<div className={'parent'}>
        <ToggleButtonComponent ClassName={'power-button'} Icon={Icons.Power} IsActive={debugMode} OnClick={(isActive: boolean) => WriteState("debug_mode", !isActive)}/>

        {/*  */}
        <div className={'debugger-status'} style={{ display: debugMode ? 'none' : 'flex' }}>
            <div className={'title'}> Debugger Offline </div>
            <div className={'timestamp'}> {formatTimestamp(heartbeat?.PcStats?.TimeStamp) || 'N/A'} </div>
            <div className={'time-ago'}> {timeAgo || 'N/A'} </div>
        </div>

        <div className={'header'} style={{ display: debugMode ? 'flex' : 'none' }}>
            <div className={'title'}> {/* BLANK */} </div>
            <div className={'time'}> { time } </div>
            <div className={'title'}> { Config.version } </div>
        </div>

        <div className={'main-container'} style={{ display: debugMode ? 'flex' : 'none' }}>
            {/* Modules Controller */}
            <div className={'section-parent'} style={{ flexDirection: 'column',  }}>
                <div className={'section'} style={{ flexGrow: 1 }}>
                    <ModulesControllerComponent/>
                </div>
            </div>

            <div className={'section-parent'} style={{ flexDirection: 'column', flexGrow: 1 }}>

                {/* Main Window View */}
                <div className={'section'} style={{ flexGrow: 1 }}>
                    { currentPage === PagesEnum.Logs && <LogsComponent/> }
                    { currentPage === PagesEnum.SelectedModule && <MoudleInfoViewerComponent/> }
                    { currentPage === PagesEnum.Camera && <CameraManagerComponent isFullScreen={false}/> }

                    <div className={'main-window-view-button-hotbar'}>
                        <ToggleButtonComponent Icon={Icons.FileLines} OnClick={() => ChangePage(PagesEnum.Logs)} IsActive={currentPage === PagesEnum.Logs}/>
                        <ToggleButtonComponent Icon={Icons.Camera} OnClick={() => ChangePage(PagesEnum.Camera)} IsActive={currentPage === PagesEnum.Camera}/>
                        <ToggleButtonComponent Icon={Icons.Info} OnClick={() => ChangePage(PagesEnum.SelectedModule)} IsActive={currentPage === PagesEnum.SelectedModule}/>
                    </div>
                </div>
                <div className={'section-child'}>
                    <div className={'section'} style={{ flexGrow: 1, marginLeft: 0 }}>
                        <RamUsageDoughnutComponent/>
                    </div>
                    <div className={'section'} style={{ flexGrow: 1, boxSizing: 'border-box', height: '334px' }}>
                        <div className={'main-process-info'}>
                            <h3 className="system-info-title">Main Process Information</h3>
                            <div style={{ display: 'flex' }}>
                                <div style={{ margin: '5px'}}> Uptime </div>
                                <div style={{ margin: '5px'}}> {mainProcessBootTime} </div>
                            </div>
                            <Heartbeat LastUpdated={heartbeat?.PcStats?.TimeStamp} />
                        </div>
                    </div>
                    <div className={'section'} style={{ flexGrow: 1, marginRight: 0 }}>
                        <CpuUsageDoughnutComponent/>
                    </div>
                </div>
            </div>

            <div className={'section-parent'} style={{ flexDirection: 'column', flexGrow: 0 }}>
                <div className={'section'} style={{ flexGrow: 1, background:'#2c254d'}}>
                    <img src={`http://${window.location.hostname}:5002/favicon-transparent.png`} style={{ width:'200px', height:'auto', margin: '20px 10px', justifyContent: 'center', alignItems: 'center' }} />
                </div>

                {/* System Information */}
                <div className={'section'} style={{ flexGrow: 1 }}>
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
                            <li className="system-info-item"><strong>Boot Time:</strong> {formatStringTimestamp(systemStats?.BootTime) || 'N/A'}</li>
                        </ul>
                    </div>
                </div>
            
                <div className={'section'} style={{ flexGrow: 0 }}>
                    <GpuUsageComponent/>
                </div>
                <div className={'section'} style={{ flexGrow: 0 }}>
                    <DiskUsageComponent/>
                </div>
            </div>
        </div>
    </div>);
});

LandingPage.displayName = 'LandingPage';
export default LandingPage;