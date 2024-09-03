from API.Calibration.sql import Calibration, CalibrationType
from API.base_datahandler import BaseDataHandler
from API.Logging.sql import Log
from Common.helper import sql_val

class CalibrationDataHandler(BaseDataHandler):
    def __init__(self, _validate : bool = False):
        super().__init__(Calibration(), _validate)

    # Set a single calibration edit flag
    def set_calibration(self, calibration: Calibration):
        prepped_data = calibration.to_sql()
        
        super().insert_update(Calibration(), prepped_data[0], prepped_data[1])

    # Get a single calibration
    def get_calibration(self, type: CalibrationType):
        calibration = Calibration()

        returned_data = super().get(Calibration(), "*", 1, [[sql_val("type", type.value, True)]], False)
        
        if (returned_data is None):
            # Create new input
            new_calibration = Calibration()
            new_calibration.type = type
            self.set_calibration(new_calibration)
            return new_calibration
        
        calibration.from_sql(returned_data)
        return calibration

    # Get all avaiable calibrations
    def get_all_calibrations(self, type: CalibrationType):
        calibration = Calibration()
        returned_data = super().get(Calibration(), "*", 1, [[sql_val("type", type, True)]], True)
        
        if (returned_data is None):
            return None
        
        calibration.from_sql(returned_data)
        return calibration