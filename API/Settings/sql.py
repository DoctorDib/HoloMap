from time import sleep
from Common.helper import deserialise
from API.base_sql import BaseSQLInterface
from config import Config
from enum import IntEnum

class Types(IntEnum):
    STRING=0
    INT=1
    BOOL=2
    ARRAY=3
    DICT=4

class SettingsField(BaseSQLInterface):
    owner_id_aesn : str = ""
    key : str = ''
    value_base64 : str = ''
    type : Types = Types.STRING # default to string

class Settings(BaseSQLInterface):
    _table = "settings"
    _columns = {
        "owner_id_aesn": "TEXT",
        "key": "TEXT",
        "value_base64": "TEXT",
        "type": "INTEGER",
        "UNIQUE_CONSTRAINT": "UNIQUE(owner_id_aesn, key)",
    }

    fields : list[SettingsField] = []

    def format(self, value, val_type):
        match Types(val_type):
            case Types.STRING:
                return str(value)
            case Types.INT:
                return int(value)
            case Types.BOOL:
                return bool(value)
            case Types.ARRAY | Types.DICT:
                return deserialise(value)

    def __init__(self, fields : dict = None):
        if (fields is None):
            return

        settings_fields : list[SettingsField] = []
        type_identifier = SettingsKeyValueTypes()
        
        for key in fields:
            new_field = SettingsField()
            new_field.key = key
            new_field.value_base64 = fields[key]
            new_field.type = type_identifier[key]
            settings_fields.append(new_field)

        setattr(self, "fields", settings_fields)

    def to_json(self):
        new_fields : dict = {}

        for field in self.fields:
            json_field = field.to_json()
            new_fields[json_field['key']] = self.format(json_field['value_base64'], json_field['type'])

        return new_fields

class SettingsController:
    settings : Settings
    settings_server_active : bool = False

    def refresh(self, settings_list):
        settingFields : list[SettingsField] = []
        for settings_key in settings_list:
            settingsField = SettingsField(settings_list[settings_key])
            settingFields.append(settingsField)
        self.settings.fields = settingFields

    def start_status_check(self, running):
        while running.is_set():
            try:
                for _ in range(Config.ComponentStatusInterval):
                    sleep(1) # 1 second
                    # checking if exit
                    if (not running.is_set()):
                        break

                if (not self.settings_server_active):
                    break
            except (KeyboardInterrupt):
                running.clear()
                break

    def initialise(self):
        self.settings_server_active = True

    def stop(self):
        self.settings_server_active = False

class SettingsKeyValueTypes():
    def __getitem__(self, name):
        return getattr(self, name)

    # Settings form values
    time_interval_logger : Types = Types.INT
    time_interval_ping : Types = Types.INT
    def_pos_x : Types = Types.INT
    def_pos_y : Types = Types.INT
    def_size_width : Types = Types.INT
    def_size_height : Types = Types.INT
    drag_steps : Types = Types.INT
    resize_steps : Types = Types.INT

    # Hidden values
    tab_order : Types = Types.ARRAY