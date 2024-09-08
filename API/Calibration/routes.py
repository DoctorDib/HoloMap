from flask import Blueprint, request

from API.Calibration.datahandler import CalibrationDataHandler
from API.Calibration.sql import CalibrationType

import logger

calibration_routes_app = Blueprint('calibration_routes_app', __name__)

def create_calibration_route(shared_state):

    @calibration_routes_app.route("/calibration/edit/set", methods=['POST'])
    def calibration_edit_set(edit_flag: bool = None, type: CalibrationType = None):
        try:
            if (edit_flag is None or type is None):
                calibration_data = request.get_json()['calibration']
                edit_flag = calibration_data['edit']
                type = CalibrationType(calibration_data['type'])

            calibration = CalibrationDataHandler().get_calibration(type)
            calibration.edit = edit_flag

            if (type == CalibrationType.WEBCAM and edit_flag):
                # Starting calibration for webcam
                shared_state['calibration_flag'] = True
            elif (type == CalibrationType.WEBCAM and not edit_flag):
                # Starting calibration for webcam
                shared_state['calibration_flag'] = False
            
            CalibrationDataHandler().set_calibration(calibration)
        except Exception as e:
            logger.exception(e)
        return {}

    @calibration_routes_app.route("/calibration/boundary/set", methods=['POST'])
    def calibration_boundary_set(cached_boundary_obj: dict = None, type: CalibrationType = None):
        try:
            if (cached_boundary_obj is None or type is None):
                calibration_data = request.get_json()['calibration']
                cached_boundary_obj = calibration_data['cached_boundary']
                type = CalibrationType(calibration_data['type'])

            calibration = CalibrationDataHandler().get_calibration(type)
            calibration.cached_boundary_obj = cached_boundary_obj

            CalibrationDataHandler().set_calibration(calibration)

        except Exception as e:
            logger.exception(e)
        return {}

    @calibration_routes_app.route("/calibration/get", methods=['POST'])
    def calibration_get(type: CalibrationType = None):
        try:
            if (type is None):
                calibration_data = request.get_json()['calibration']
                type = CalibrationType(calibration_data['type'])

            return CalibrationDataHandler().get_calibration(type).to_json()
        except Exception as e:
            logger.exception(e)
        return {}


    @calibration_routes_app.route("/calibration/get/all", methods=['POST'])
    def calibration_get_all():
        try:
            projector_calibration = CalibrationDataHandler().get_calibration(CalibrationType.PROJECTION).to_json()
            webcam_calibration = CalibrationDataHandler().get_calibration(CalibrationType.WEBCAM).to_json()

            return {
                "projector": projector_calibration,
                "webcam": webcam_calibration
            }
        except Exception as e:
            logger.exception(e)
        return {}
    
    @calibration_routes_app.route("/calibration/set/all", methods=['POST'])
    def calibration_set_all():
        try:
            projector_calibration = CalibrationDataHandler().get_calibration(CalibrationType.PROJECTION)
            webcam_calibration = CalibrationDataHandler().get_calibration(CalibrationType.WEBCAM)

            # Saving cached boundary as the main boundary
            projector_calibration.readonly_boundary_obj = projector_calibration.cached_boundary_obj
            webcam_calibration.readonly_boundary_obj = webcam_calibration.cached_boundary_obj

            # Saving new data
            CalibrationDataHandler().set_calibration(projector_calibration)
            CalibrationDataHandler().set_calibration(webcam_calibration)
        except Exception as e:
            logger.exception(e)
        return {}
    

    return calibration_routes_app