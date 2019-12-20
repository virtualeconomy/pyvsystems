import struct
import logging
from .crypto import list2bytes, to_hex


def convert_bytes_to_hex(bytes_object):
    return [to_hex(bytes([byte])) for byte in bytes_object]


def shorts_from_byte_array(byte_array):
    if len(byte_array) != 2:
        logging.exception("Error: Input is not shorts!")
    return int(''.join(byte_array), 16)


def serialize_string(string):
    string = string.encode()
    ss = bytes(string)
    return ss


def serialize_arrays(bs):
    sa = bytes()
    for b in bs:
        b = serialize_array(b)
        sa += b
    return struct.pack(">H", len(bs)) + bytes(sa)


def serialize_array(b):
    if type(b) is list:
        b_bytes = list2bytes(b)
        return struct.pack(">H", len(b)) + b_bytes
    else:
        return struct.pack(">H", len(b)) + b


def parse_array_size(bytes_object, start_position):
    length_byte_array = convert_bytes_to_hex(bytes_object[start_position:(start_position + 2)])
    length = shorts_from_byte_array(length_byte_array)

    return [bytes_object[(start_position + 2):(start_position + 2 + length)], start_position + 2 + length]


def parse_arrays(bytes_object):
    length_byte_array = convert_bytes_to_hex(bytes_object[0:2])
    length = shorts_from_byte_array(length_byte_array)
    all_info = []
    pos_drift = 2
    for pos in range(length):
        [array_info, pos_drift] = parse_array_size(bytes_object, pos_drift)
        all_info.append(array_info)
    return [all_info, pos_drift - 2 - 2 * length]
