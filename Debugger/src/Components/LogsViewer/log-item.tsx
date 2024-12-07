import React from 'react';
import './logs_style.scss';
import { Log } from '../../Interfaces/StateInterface';
import Icons from '../../Common/Icons';

interface LogItemInterface {
    Logs: Log[];
}

const LogItemComponent = ({ Logs }: LogItemInterface): React.ReactElement => {
    const getSymbol = (type: string) => {
        switch (type) {
            case 'INFO':
                return Icons.Info;
            case 'WARNING':
                return Icons.Warning;
            case 'ERROR':
                return Icons.Error;
        }
    };

    const getSymbolColour = (type: string) => {
        switch (type) {
            case 'INFO':
                return 'green';
            case 'WARNING':
                return 'orange';
            default:
                return 'red';
        }
    };

    const formatTimestamp = (timestamp: number): string => {
        const date = new Date(timestamp * 1000);

        return date.toLocaleString('en-UK', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        });
    };

    return <>
        {
            Logs?.map((log: Log, index): React.ReactElement => (
                <div className={"log"} key={index}>
                    <div className={"type"} style={{ color: getSymbolColour(log.type) }}>
                        {getSymbol(log.type)}
                    </div>
                    <div className={"content"}>
                        <div className={"message"}>{log.message}</div>
                        <div className={"date"}>{formatTimestamp(log.date)}</div>
                    </div>
                </div>
            ))
        }
    </>
};

export default LogItemComponent;
