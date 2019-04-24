import struct


def serializeString(string):
    string = string.encode()
    ss = bytes(string)
    return ss

def serializeArrays(bs):
    sa = bytes('',encoding ='utf-8')
    for b in bs:
        b = serializeArray(b)
        sa += b
    return struct.pack(">H", len(bs)) + sa

def serializeArray(b):
    return struct.pack(">H", len(b)) + b
