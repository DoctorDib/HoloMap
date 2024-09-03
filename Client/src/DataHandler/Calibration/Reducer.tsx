import { PROJECTOR_CALIBRATION_BLANK, WEBCAM_CALIBRATION_BLANK } from '../../Common/blanks';
import { DataActionEnum } from '../../Common/enumerations';
import { Calibrations } from '../../Interfaces/StateInterface';

const initialResultState : Calibrations = {
    webcam: WEBCAM_CALIBRATION_BLANK,
    projector: PROJECTOR_CALIBRATION_BLANK,
    cornerPoint: 0,
};

const reducer = (state = initialResultState, action: any = {}) => {
    const newState = { ...state };

    switch (action.type) {
        case DataActionEnum.Projector_SetEdit:
            return {
                ...newState,
                projector: {
                    ...newState.projector,
                    edit: action.edit,
                },
            };
        case DataActionEnum.Webcam_SetBoundary:
            return {
                ...newState,
                webcam: {
                    ...newState.webcam,
                    cachedBoundary: action.cached_boundary,
                },
            };
        case DataActionEnum.Webcam_GetCalibration:
            return {
                ...newState,
                webcam: action.webcam,
            };

        case DataActionEnum.Webcam_SetEdit:
            return {
                ...newState,
                webcam: {
                    ...newState.webcam,
                    edit: action.edit,
                },
            };
        case DataActionEnum.Projector_SetBoundary:
            return {
                ...newState,
                projector: {
                    ...newState.projector,
                    cachedBoundary: action.cached_boundary,
                },
            };
        case DataActionEnum.Projector_GetCalibration:
            return {
                ...newState,
                projector: action.projector,
            };

        case DataActionEnum.GetCalibrations:
            return {
                ...newState,
                projector: {
                    edit: action.calibrations.projector.edit,
                    readonly_boundary: action.calibrations.projector.readonly_boundary_obj,
                    cached_boundary: action.calibrations.projector.cached_boundary_obj,
                },
                webcam: {
                    edit: action.calibrations.webcam.edit,
                    readonly_boundary: action.calibrations.webcam.readonly_boundary_obj,
                    cached_boundary: action.calibrations.webcam.cached_boundary_obj,
                },
            };

        case DataActionEnum.NextCalibrationPoint:
            return {
                ...newState,
                cornerPoint: action.data,
            };

        default:
            return { ...newState };
    }
};

export default reducer;