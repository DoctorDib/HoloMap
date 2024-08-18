import React from "react";
import { Socket } from 'socket.io-client';

interface LogTypes {
    date: number,
    type: string,
    message: string,
}

interface StateTypes {
    root: RootTypes,
    notification: NotificationQueueInterface,
    dialog: DialogStateInterface,
}

interface RootTypes {
    logs: Array<LogTypes>,
    settings: object, // TODO - Look more into interfaces for this?
    socket?: Socket,
    qr: QR,
}

interface QR {
    detected_qrs: Array<Array<Array<number>>>,
}

interface NotificationTypeInterface {
    Info: number,
    Success: number,
    Warning: number,
    Error: number,
}

interface NotificationInterface {
    message: string,
    type: number
}

interface NotificationQueueInterface {
    queue: Array<NotificationInterface>
}

interface DialogInterface {
    header: string,
    message: string,
    options: Array<DialogOptionsInterface>,
}

interface DialogStateInterface {
    dialog: DialogInterface | null,
}

interface ContextOptionInterface {
    title: string,
    element: React.ReactElement,
}

interface ContextStateInterface {
    x: number,
    y: number,
    isVis: boolean,
    options: Array<React.ReactElement>,
}

interface DialogOptionsInterface {
    label: string,
    onClick: () => void | null,
}

export {
    // Default
    StateTypes,
    RootTypes,

    // Logging
    LogTypes,

    // Notification pop ups
    NotificationTypeInterface,
    NotificationInterface,
    NotificationQueueInterface,
    
    // Dialog window
    DialogStateInterface,
    DialogInterface,
    DialogOptionsInterface,
    ContextStateInterface,
    ContextOptionInterface,

    // QR Handling
    QR,
};