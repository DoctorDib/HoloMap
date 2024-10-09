from enum import Enum

import pickle, codecs

def serialise(obj : any):
    return codecs.decode(codecs.encode(pickle.dumps(obj), "base64"), 'UTF-8').replace('\n', '')

def deserialise(obj : str):
    if (isinstance(obj, dict)):
        return obj

    return pickle.loads(codecs.decode(codecs.encode(obj, 'UTF-8'), 'base64'))

def format_type(input : any):
    val_type = type(input)

    if (val_type == str):
        return "\"{0}\"".format(str(input))
    if (issubclass(val_type, Enum)):
        return format_type(input.value)
    else:
        return str(input)

def sql_val(key : str, val : any, add_speechmarks : bool = False):
    return "{0} = {1}".format(key, "\"{0}\"".format(val) if add_speechmarks else val)

def prep_custom_keys(keys : list[str]) -> str:
    return ", ".join(keys)

def tuple_num_to_tuple_int(tuple_num : tuple[int, int]) -> tuple[int, int]:
    return (int(tuple_num[0]), int(tuple_num[1]))

def convert_tuple_coords(tuple_num):
    return (tuple_num_to_tuple_int(tuple_num[0]), tuple_num_to_tuple_int(tuple_num[1]), tuple_num_to_tuple_int(tuple_num[2]), tuple_num_to_tuple_int(tuple_num[3]))

