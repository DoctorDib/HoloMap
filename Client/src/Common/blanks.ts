import { Calibrations, QR, Webcam_Calibration, Projector_Calibration } from '../Interfaces/StateInterface';

const SETTINGS_BLANK : object = {
    layers: {},
};

const QR_BLANK : QR = {
    detected_qrs: [],
};

const WEBCAM_CALIBRATION_BLANK: Webcam_Calibration = {
    edit: false,
    readonly_boundary: {},
    cached_boundary: {},
};

const PROJECTOR_CALIBRATION_BLANK: Projector_Calibration = {
    edit: false,
    readonly_boundary: {},
    cached_boundary: {},
};

const CALIBRATION_BLANK: Calibrations = {
    webcam: WEBCAM_CALIBRATION_BLANK,
    projector: PROJECTOR_CALIBRATION_BLANK,
    cornerPoint: 0,
};

export { 
    QR_BLANK,  

    SETTINGS_BLANK,

    WEBCAM_CALIBRATION_BLANK,
    PROJECTOR_CALIBRATION_BLANK,
    CALIBRATION_BLANK,
};