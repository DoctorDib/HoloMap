from enum import Enum
from abc import ABC
from typing import get_type_hints
from collections.abc import MutableSequence, MutableMapping

from Common.helper import format_type, serialise, deserialise

import logger

class BaseSQLInterface(ABC):
    __sql_class_type__ = True

    def __init__(self, obj=None):
        if (obj is None):
            return
        self.prep(obj)

    def get_keys(self):
        return list(self.to_json().keys())

    def to_json(self, obj : dict | list = None):
        is_list = False

        prepped_dict = {}

        if (obj is None):
            dict_obj = self.__dict__
        else:
            is_list = True if type(obj) == list else False
            dict_obj = obj

        seq_iter = dict_obj if isinstance(dict_obj, dict) else range(len(dict_obj))

        for key in seq_iter:
            val = dict_obj[key]
            dict_val_type = type(val)

            if (dict_val_type == list or dict_val_type == dict):
                # recursive
                prepped_dict[key] = self.to_json(val)
            elif (hasattr(val, '__sql_class_type__')):
                prepped_dict[key] = self.to_json(val.__dict__)
            elif (issubclass(dict_val_type, Enum)):
                prepped_dict[key] = val.value
            else:
                prepped_dict[key] = val

        if (is_list):
            # Converting back to list
            new_list = []
            for key in prepped_dict:
                new_list.append(prepped_dict[key])
            return new_list

        return prepped_dict

    def from_sql(self, values, keys = None):
        if (keys is None):
            keys = self._columns

        # Type example get_type_hints(Test)['id'](2)
        #
        # Add a tag to the name e.g. storage_aes64.
        # Anything with base64 will convert else use get_type_hints

        try:
            for index, key in enumerate(keys):
                if (key == 'UNIQUE_CONSTRAINT'):
                    continue

                value = values[index]
                if ("_base64" in key):
                    value = deserialise(value)
                else:
                    value = get_type_hints(self)[key](value)
                    
                setattr(self, key, value)
        except Exception as e:
            print("error")
            logger.exception(e)
    
    def get_active_data_keys(self):
        keys = []
        for key in self.__dict__:
            keys.append(key)
        return keys
            
    def to_sql(self, keys=None):
        if keys is None:
            keys = self.columns()

        key_list = []
        value_list = []
        
        if (keys == "*"):
            keys = self.get_keys()

        for key in keys:
            key_list.append(key)
            if ("_base64" in key):
                value = format_type(serialise(getattr(self, key)))
            else:
                value = format_type(getattr(self, key))
            value_list.append(value)
        
        final_key = "({0})".format(", ".join(key_list)) 
        final_value = "({0})".format(", ".join(value_list)) 
        
        return [ final_key, final_value ]

    def prep(self, obj : dict):
        for key in obj:
            setattr(self, key, obj[key])

    def table(self):
        return self._table
    def columns(self):
        keys : list[str] = []
        for key in self._columns:
            if (key == 'UNIQUE_CONSTRAINT'):
                continue
            keys.append(key)
        return keys
    def columns_with_type(self):
        columns : list[str] = []
        for key in self._columns:
            if (key == 'UNIQUE_CONSTRAINT'):
                column_type : str = "{0}".format(self._columns[key])
            else:
                column_type : str = "{0} {1}".format(key, self._columns[key])
            columns.append(column_type)
        return columns

class SQLList(MutableSequence):
    def __init__(self, _type=None):
        self._inner_list = list()

    def __len__(self):
        return len(self._inner_list)

    def __delitem__(self, index):
        self._inner_list.__delitem__(index)

    def insert(self, index, value):
        self._inner_list.insert(index, value)

    def __setitem__(self, index, value):
        self._inner_list.__setitem__(index, value)

    def __getitem__(self, index):
        return self._inner_list.__getitem__(index)

    def append(self, value):
        self.insert(len(self) + 1, value)

    def to_json(self, single_key:str=None):
        list_obj : list[BaseSQLInterface] = []
        for item in self._inner_list:
            if (single_key == None):
                list_obj.append(item.to_json())
            else:
                list_obj.append(item.to_json()[single_key])
        return list_obj

class SQLDict(MutableMapping):
    '''
    Mapping that works like both a dict and a mutable object, i.e.
    d = D(foo='bar')
    and 
    d.foo returns 'bar'
    '''
    # ``__init__`` method required to create instance from class.
    def __init__(self, *args, **kwargs):
        '''Use the object dict'''
        self.__dict__.update(*args, **kwargs)
    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def __getitem__(self, key):
        return self.__dict__[key]
    def __delitem__(self, key):
        del self.__dict__[key]
    def __iter__(self):
        return iter(self.__dict__)
    def __len__(self):
        return len(self.__dict__)
    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        '''returns simple dict representation of the mapping'''
        return str(self.__dict__)
    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        return '{}, D({})'.format(super(SQLDict, self).__repr__(), 
                                  self.__dict__)

    def to_json(self):
        if (self.__dict__ == {}):
            return {}
            
        dict_obj : dict[BaseSQLInterface] = {}
        for key in self.__dict__:
            
            dict_obj[key] = self.__dict__[key].to_json()
        return dict_obj