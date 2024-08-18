import logging, json, os, sys

from enum import Enum
from datetime import datetime

from API.Logging.sql import Log, LogType
from API.Logging.datahandler import LOGSDataHandler

logging.basicConfig(level=logging.INFO)

stored_logs = []

def user_input(message):
    log = Log({"type": LogType.USER_INPUT, "message": message})
    add_log(log)

def info(message):
    log = Log({"type": LogType.INFO, "message": message})
    add_log(log)

def warning(message):
    log = Log({"type": LogType.WARNING, "message": message})
    add_log(log)

def error(message):
    log = Log({"type": LogType.ERROR, "message": message})
    add_log(log)

def exception(message):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # Custom exception message
    message = "[{0} - {1} (Line: {2})] => {3}".format(exc_type, fname, exc_tb.tb_lineno, message)

    log = Log({"type": LogType.ERROR, "message": message})
    add_log(log)

def add_log(log : Log):
    # Adding to db
    LOGSDataHandler().add_log(log)
    date_time = datetime.fromtimestamp(log.date).strftime("%d/%m/%Y %H:%M:%S")
    match log.type:
        case LogType.INFO | LogType.USER_INPUT:
            logging.info("<{0}> {1}".format(date_time, log.message))
        case LogType.WARNING:
            logging.warning("<{0}> {1}".format(date_time, log.message))
        case LogType.ERROR:
            print("---------------------------ERROR----------------------------")
            logging.error("<{0}> {1}".format(date_time, log.message))
            print("------------------------------------------------------------")

def clear_all():
    LOGSDataHandler().clear_logs()

def get_logs():
    temp_logs = []
    temp_logs.extend(stored_logs)
    stored_logs.clear()
    return json.dumps(temp_logs)
