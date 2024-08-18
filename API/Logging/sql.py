import calendar
import time

from enum import Enum
from API.base_sql import BaseSQLInterface

class LogType(str, Enum):
    USER_INPUT = "USER_INPUT"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Log(BaseSQLInterface):
    _table = "logs"
    _columns = {
        "date": "INTEGER",
        "message": "TEXT",
        "type": "TEXT",
    }

    date : int = 0
    type : LogType = LogType.INFO
    message : str = ''

    def __init__(self, item=None):
        super().__init__(item)
        self.date = calendar.timegm(time.gmtime())