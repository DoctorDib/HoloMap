from dotenv import load_dotenv

import logging
import os, inspect

MAIN_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

global x

class DirectoryInfo:
    def __init__(self, _folder, _file_name):
        self.directory = "{0}/{1}".format(MAIN_PATH, _folder)
        self.file_name = _file_name

    directory : str = ''
    file_name : str = ''
    format : str = ''

    def full_path(self):
        return "{0}/{1}".format(self.directory, self.file_name)

class Config():

    def __init__(self):
        self.cached_data = {}
        load_dotenv()

    # Logs
    MaxLogs = 500
    LogLocation = DirectoryInfo('Data', 'logs.json')
    
    APIStatusInterval = 60
    ComponentStatusInterval = 60

    #SQLite
    DBName="HANA_storage.db"
    DEVDBName="HANA_storage_DEV.db"

    MainDir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

    def get_double(self, key):
        try:
            if key in self.cached_data:
                return self.cached_data[key]
            else:
                new_data = float(os.getenv(key))  # Use float to handle double precision
                self.cached_data.update({key: new_data})
                return new_data
        except Exception as e:
            logging.exception(e)

    def get_int(self, key):
        try:
            if (key in self.cached_data):
                return self.cached_data[key]
            else:
                new_data = int(os.getenv(key))
                self.cached_data.update({key: new_data})
                return new_data
        except Exception as e:
            logging.exception(e)
    
    def get_str(self, key):
        try:
            if (key in self.cached_data):
                return self.cached_data[key]
            else:
                new_data = str(os.getenv(key))
                self.cached_data.update({key: new_data})
                return new_data
        except Exception as e:
            logging.exception(e)