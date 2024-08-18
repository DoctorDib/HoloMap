from flask import Blueprint, request

from API.Settings.datahandler import SettingsDataHandler

import logger

settings_routes_app = Blueprint('settings_routes_app', __name__)

@settings_routes_app.route("/settings/set", methods=['POST'])
def settings_set():
    try:
        # Not using OwnerID because when creating a new account 
        # there is a chance OwnerID does not yet exist
        settings = request.get_json()['settings'] # object of keys and values
        # settings_class = Settings(settings)
        # SettingsDataHandler().set_settings(settings_class)
    except Exception as e:
        logger.exception(e)
    return {}

@settings_routes_app.route("/settings/get", methods=['GET'])
def settings_get():
    try:
        return SettingsDataHandler().get_settings().to_json()
    except Exception as e:
        logger.exception(e)

@settings_routes_app.route("/settings/field/set", methods=['POST'])
def settings_field_set():
    try:
        owner_id = request.get_json()['ownerID']
        field = request.get_json()['field'] # object of keys and values
        # setting_types = SettingsKeyValueTypes()
        key = field['key']
        # field = SettingsField(key, field['value'], setting_types[key])
        SettingsDataHandler(owner_id).set_field(field)
    except Exception as e:
        logger.exception(e)
    return {}

@settings_routes_app.route("/settings/field/get", methods=['GET'])
def settings_field_get():
    try:
        key = request.get_json()['field_key'] # object of keys and values
        return SettingsDataHandler().get_field(key).to_json()
    except Exception as e:
        logger.exception(e)