import base64
from enum import Enum
from Crypto.Cipher import AES

import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

import pickle, codecs

def serialise(obj : any):
    return codecs.decode(codecs.encode(pickle.dumps(obj), "base64"), 'UTF-8').replace('\n', '')

def deserialise(obj : str):
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
