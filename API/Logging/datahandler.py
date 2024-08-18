from API.base_datahandler import BaseDataHandler
from API.Logging.sql import Log
from API.base_sql import SQLList

class LOGSDataHandler(BaseDataHandler):
    def __init__(self, _validate : bool = False):
        super().__init__(Log(), _validate)

    def add_log(self, log : Log):
        prepped_data = log.to_sql()
        super().insert_data(Log(), prepped_data[0], prepped_data[1])

    def get_logs(self) -> SQLList:
        return_data = super().get(Log(), "*", 500, None, True)

        # Formatting to List of Log
        logs : SQLList = SQLList()
        for data in return_data:
            log : Log = Log()
            log.from_sql(data)
            logs.append(log)

        # Returning list of Log classes
        return logs

    def clear_logs(self):
        super().clear_table(self, Log)