import { readFileSync } from 'fs';
import { join } from 'path';

export const getTimeAgo = (dateString: string) => {
    const date: any = new Date(dateString);
    const now: any = new Date();
    const secondsAgo: number = Math.floor((now - date) / 1000);
    return getTimeAgoFromSeconds(secondsAgo);
};

export const getTimeAgoFromTimeStamp = (timestamp: number) => {
    const date = new Date(timestamp * 1000); // Convert Unix 
    const now = new Date();
    const secondsAgo = Math.floor((now.getTime() - date.getTime()) / 1000);
    return getTimeAgoFromSeconds(secondsAgo);
};

export const getTimeAgoFromSeconds = (secondsAgo: number): string => {
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

export const formatStringTimestamp = (timestamp: string): string => {
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

export const formatTimestamp = (timestamp: number): string => {
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

export const convertDateNowToClock = () => {
    const now = new Date(Date.now());
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    return `${hours}:${minutes}:${seconds}`;
};
