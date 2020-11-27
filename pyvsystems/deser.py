import struct
from .crypto import list2bytes, to_hex


class Deser(object):
    @staticmethod
    def convert_bytes_to_hex(bytes_object):
        return [to_hex(bytes([byte])) for byte in bytes_object]

    @staticmethod
    def shorts_from_byte_array(byte_array):
        if len(byte_array) != 2:
            # Error: Input is not shorts!
            pass
        return int(''.join(byte_array), 16)

    @staticmethod
    def serialize_string(string):
        string = string.encode()
        ss = bytes(string)
        return ss

    @staticmethod
    def deserialize_string(byte_array):
        byte_array = byte_array.decode()
        ss = str(byte_array)
        return ss

    @staticmethod
    def serialize_arrays(bs):
        sa = bytes()
        for b in bs:
            b = Deser.serialize_array(b)
            sa += b
        return struct.pack(">H", len(bs)) + bytes(sa)

    @staticmethod
    def serialize_array(b):
        if type(b) is list:
            b_bytes = list2bytes(b)
            return struct.pack(">H", len(b)) + b_bytes
        else:
            return struct.pack(">H", len(b)) + b

    @staticmethod
    def parse_array_size(bytes_object, start_position):
        length_byte_array = Deser.convert_bytes_to_hex(bytes_object[start_position:(start_position + 2)])
        length = Deser.shorts_from_byte_array(length_byte_array)
        return bytes_object[(start_position + 2):(start_position + 2 + length)], start_position + 2 + length

    @staticmethod
    def parse_arrays(bytes_object):
        length_byte_array = Deser.convert_bytes_to_hex(bytes_object[0:2])
        length = Deser.shorts_from_byte_array(length_byte_array)
        all_info = []
        pos_drift = 2
        for pos in range(length):
            array_info, pos_drift = Deser.parse_array_size(bytes_object, pos_drift)
            all_info.append(array_info)
        return all_info