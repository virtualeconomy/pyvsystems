from .crypto import *
from .error import *
from .contract_build import *
import base58
import pyvsystems


class DataEntry:
    def __init__(self, data, dataType):
        if not type(dataType) is bytes:
            msg = 'Data Type must be bytes'
            pyvsystems.throw_error(msg, InvalidParameterException)
        if dataType == Type.public_key:
            self.bytes = dataType + base58.b58decode(data)
        elif dataType == Type.address:
            self.bytes = dataType + base58.b58decode(data)
        elif dataType == Type.amount:
            self.bytes = dataType + struct.pack(">Q", data)
        elif dataType == Type.int32:
            self.bytes = dataType + struct.pack(">I", data)
        elif dataType == Type.short_text:
            self.bytes = dataType + deser.serialize_array(str2bytes(data))
        elif dataType == Type.contract_account:
            self.bytes = dataType + base58.b58decode(data)
        elif dataType == Type.account:
            self.bytes = dataType + base58.b58decode(data)
        else:
            msg = 'Invalid Data Entry'
            pyvsystems.throw_error(msg, InvalidParameterException)

class Type:
    public_key = bytes([1])
    address = bytes([2])
    amount = bytes([3])
    int32 = bytes([4])
    short_text = bytes([5])
    contract_account = bytes([6])
    account = bytes([7])


