import os, sys, inspect

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

class Config:
    # Logs
    MaxLogs = 500
    LogLocation = DirectoryInfo('Data', 'logs.json')
    
    APIStatusInterval = 60
    ComponentStatusInterval = 60

    #SQLite
    DBName="HANA_storage.db"
    DEVDBName="HANA_storage_DEV.db"

    MainDir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
