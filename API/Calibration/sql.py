from enum import Enum

from API.base_sql import BaseSQLInterface

class CalibrationType(str, Enum):
    PROJECTION = "PROJECTION"
    WEBCAM = "WEBCAM"

class Calibration(BaseSQLInterface):
    _table = "calibration"
    _columns = {
        "edit": "INTEGER",
        "readonly_boundary_obj": "TEXT",
        "cached_boundary_obj": "TEXT",
        "type": "TEXT UNIQUE",
    }

    edit: bool = False
    readonly_boundary_obj: dict = {}
    cached_boundary_obj: dict = {}
    type: CalibrationType = CalibrationType.PROJECTION

    def __init__(self, item=None):
        super().__init__(item)