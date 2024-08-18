# from API.base_datahandler import BaseDataHandler
# from API.base_sql import SQLList
# from Common.helper import sql_val

# class SettingsDataHandler(BaseDataHandler):

#     def __init__(self, _validate : bool = False):
#         super().__init__(Settings(), _validate)

#     def get_settings(self) -> SQLList:
#         returned_data = super().get(Settings(), "*", 500)
#         fields : SQLList = SQLList(SettingsField)
#         for data in returned_data:
#             new_field = SettingsField()
#             new_field.from_sql(data, Settings().columns())
#             fields.append(new_field)

#         boop = fields.to_json()

#         settings : Settings = Settings()
#         settings.fields = fields
#         return settings

#     def set_settings(self, settings : Settings):
#         for field in settings.fields:
#             self.set_field(field)

#     def set_field(self, field : SettingsField):
#         prepped_field = field.to_sql(Settings().columns())
#         super().insert_update(Settings(), prepped_field[0], prepped_field[1])
            
#     def get_field(self, key : str) -> SettingsField:
#         returned_data = super().get(Settings(), '*', 1)
#         settings_field = SettingsField()
#         settings_field.from_sql(returned_data, Settings().columns())
#         return settings_field