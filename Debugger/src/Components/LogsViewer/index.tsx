import React, { useEffect, useRef, useState } from 'react';
import './logs_style.scss';
import { useSelector } from 'react-redux';
import { Log, Logs, StateTypes } from '../../Interfaces/StateInterface';
import Icons from '../../Common/Icons';
import ButtonComponent from '../Inputs/Button';

const LogsComponent = (): React.ReactElement => {
    const logs: Logs = useSelector((state: StateTypes): StateTypes => state).root.logs;
    const [autoScroll, setAutoScroll] = useState(true); // State to manage auto-scroll
    const [showScrollButton, setShowScrollButton] = useState(false); // State to manage scroll-to-bottom button visibility
    const logsContainerRef = useRef<HTMLDivElement>(null); // Ref for the logs container

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

    // Scroll to the bottom whenever new logs are added, if auto-scroll is enabled
    useEffect(() => {
        const container = logsContainerRef.current;
        if (container && autoScroll) {
            container.scrollTop = container.scrollHeight;
        }
    }, [logs, autoScroll]);

    // Check if the user manually scrolls, disable auto-scroll if they scroll up, and show the button
    const handleScroll = () => {
        const container = logsContainerRef.current;
        if (container) {
            const isAtBottom = container.scrollHeight - container.scrollTop === container.clientHeight;
            setAutoScroll(isAtBottom); // Auto-scroll only if at the bottom
            setShowScrollButton(!isAtBottom); // Show the button when not at the bottom
        }
    };

    const scrollToBottom = () => {
        const container = logsContainerRef.current;
        if (container) {
            container.scrollTo({
                top: container.scrollHeight,
                behavior: 'smooth' // Add smooth scroll behavior
            });
            setAutoScroll(true); // Re-enable auto-scroll
        }
    };

    return (
        <div className={'logs-container-wrapper'}>
            <div
                className={"logs-container"}
                ref={logsContainerRef}
                onScroll={handleScroll} // Add onScroll handler
            >
                {logs?.Logs?.map((log: Log, index) => (
                    <div className={"log"} key={index}>
                        <div className={"type"} style={{ color: getSymbolColour(log.type) }}>
                            {getSymbol(log.type)}
                        </div>
                        <div className={"content"}>
                            <div className={"message"}>{log.message}</div>
                            <div className={"date"}>{formatTimestamp(log.date)}</div>
                        </div>
                    </div>
                ))}
            </div>
            
            {/* Scroll to bottom button */}
            {showScrollButton && (
                <ButtonComponent Icon={Icons.ArrowDown} ClassName={'scroll-to-bottom'} OnClick={scrollToBottom} />
            )}
        </div>
    );
};

export default LogsComponent;
