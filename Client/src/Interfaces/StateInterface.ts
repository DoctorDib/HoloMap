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
    calibrations: Calibrations,
}

interface RootTypes {
    logs: Array<LogTypes>,
    settings: object, // TODO - Look more into interfaces for this?
    socket?: Socket,
    qr: QR,
    aruco: ArUco,
    cursor: Cursor,
}

// Calibration - Projector and Webcam
interface Calibrations {
    projector: Projector_Calibration,
    webcam: Webcam_Calibration,
    cornerPoint: number,
}

interface Projector_Calibration {
    edit: boolean,
    readonly_boundary: object,
    cached_boundary: object,
}

interface Webcam_Calibration {
    edit: boolean,
    readonly_boundary: object,
    cached_boundary: object,
}


// QR
interface QR {
    detected_qrs: Array<Array<Array<number>>>,
}

// ArUco
interface ArUco {
    detected_arucos: Array<Array<Array<number>>>,
}

// Cursor
interface Cursor {
    isMouseDown: boolean,
    position: {
        x: number,
        y: number,
    },
}

// Notifications
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

// Dialog
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

    // Data Vision Handling
    QR,
    ArUco,

    // Cursor Handling 
    Cursor,

    // Vision Aligment
    Calibrations,
    Projector_Calibration,
    Webcam_Calibration,
};