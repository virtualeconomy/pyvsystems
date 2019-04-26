import struct


def serialize_string(string):
    string = string.encode()
    ss = bytes(string)
    return ss

def serialize_arrays(bs):
    sa = bytes('',encoding ='utf-8')
    for b in bs:
        b = serialize_array(b)
        sa += b
    return struct.pack(">H", len(bs)) + sa

def serialize_array(b):
    if(type(b) is list):
        b_bytes = bytes('', encoding='utf-8')
        for b_element in b:
            b_bytes += b_element
        return struct.pack(">H", len(b)) + b_bytes
    else:
        return struct.pack(">H", len(b)) + b
