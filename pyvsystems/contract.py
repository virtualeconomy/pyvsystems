from .crypto import *
from .deser import Deser
from .setting import ContractMeta
from .errors import *
import struct
import base58

class Contract(object):
    def __init__(self, base58_string=None):
        self.language_code = None
        self.language_version = None
        self.trigger = None
        self.descriptor = None
        self.state_variable = None
        self.state_map = None
        self.textual = None
        if base58_string:
            self.from_base58_string(base58_string)


    @property
    def json(self):
        return {"language_code": Deser.deserialize_string(self.language_code),
                "language_version": int.from_bytes(self.language_version, byteorder='big'),
                "triggers": [bytes2str(base58.b58encode(x)) for x in self.trigger],
                "descriptors": [bytes2str(base58.b58encode(x)) for x in self.descriptor],
                "state_variables": [bytes2str(base58.b58encode(x)) for x in self.state_variable],
                "state_map": [bytes2str(base58.b58encode(x)) for x in self.state_map],
                "textual": {"triggers": bytes2str(base58.b58encode(self.textual[0])),
                            "descriptors": bytes2str(base58.b58encode(self.textual[1])),
                            "state_variables": bytes2str(base58.b58encode(self.textual[2])),
                            "state_maps": bytes2str(base58.b58encode(self.textual[3])) if len(
                                self.textual) >= 4 else ''
                            }}


    @property
    def bytes(self):
        if self.language_version == struct.pack(">I", 1):
            return self.language_code + self.language_version \
                   + Deser.serialize_array(Deser.serialize_arrays(self.trigger)) \
                   + Deser.serialize_array(Deser.serialize_arrays(self.descriptor)) \
                   + Deser.serialize_array(Deser.serialize_arrays(self.state_variable)) \
                   + Deser.serialize_arrays(self.textual)
        else:
            return self.language_code + self.language_version \
                   + Deser.serialize_array(Deser.serialize_arrays(self.trigger)) \
                   + Deser.serialize_array(Deser.serialize_arrays(self.descriptor)) \
                   + Deser.serialize_array(Deser.serialize_arrays(self.state_variable)) \
                   + Deser.serialize_array(Deser.serialize_arrays(self.state_map)) \
                   + Deser.serialize_arrays(self.textual)


    @property
    def base58_string(self):
        return bytes2str(base58.b58encode(self.bytes))


    def from_base58_string(self, contract_bytes_string):
        contract_bytes = base58.b58decode(contract_bytes_string)
        self.from_bytes(contract_bytes)


    def from_bytes(self, contract_bytes):
        try:
            self.language_code = contract_bytes[0:ContractMeta.language_code_byte_length]
            self.language_version = contract_bytes[
                                    ContractMeta.language_code_byte_length:ContractMeta.language_code_byte_length + ContractMeta.language_version_byte_length]
            trigger_bytes, trigger_end = Deser.parse_array_size(contract_bytes,
                                                                ContractMeta.language_code_byte_length + ContractMeta.language_version_byte_length)
            self.trigger = Deser.parse_arrays(trigger_bytes)
            descriptor_bytes, descriptor_end = Deser.parse_array_size(contract_bytes, trigger_end)
            self.descriptor = Deser.parse_arrays(descriptor_bytes)
            state_variable_bytes, state_variable_end = Deser.parse_array_size(contract_bytes, descriptor_end)
            self.state_variable = Deser.parse_arrays(state_variable_bytes)
            state_map_bytes, state_map_end = (
            state_variable_bytes, state_variable_end) if self.language_version == struct.pack(">I",
                                                                                              1) else Deser.parse_array_size(
                contract_bytes, state_variable_end)
            self.state_map = Deser.parse_arrays(struct.pack(">H", 0)) if self.language_version == struct.pack(">I",
                                                                                                              1) else Deser.parse_arrays(
                state_map_bytes)
            self.textual = Deser.parse_arrays(contract_bytes[state_map_end:len(contract_bytes)])
        except ValueError or TypeError:
            raise InvalidContractException("Contract is not initialized")


def language_code_builder(code):
    if len(code) == ContractMeta.language_code_byte_length:
        language_code = Deser.serialize_string(code)
        return language_code
    else:
        logging.error("Wrong language code length")
        raise Exception("Wrong language code length")


def language_version_builder(version):
    if len(struct.pack(">I", version)) == ContractMeta.language_version_byte_length:
        return struct.pack(">I", version)
    else:
        logging.error("Wrong language version length")
        raise Exception("Wrong language code length")


def bytes_builder_from_list(input_list):
    if type(input_list) is list:
        return Deser.serialize_array(Deser.serialize_arrays(input_list))
    else:
        logging.error("The input should be a list")

def chain_system_contract_id(chain):
    unhashedAddress = chr(6) + str(chain.chain_id) + hashChain(base58.b58encode(''))[0:20]
    addressHash = hashChain(str2bytes(unhashedAddress))[0:4]
    contract_id = bytes2str(base58.b58encode(str2bytes(unhashedAddress + addressHash)))
    return contract_id

def token_id_from_contract_id(contract_id, idx):
    address_bytes = base58.b58decode(contract_id)
    contract_id_no_check_sum = address_bytes[1:(len(address_bytes) - ContractMeta.check_sum_length)]
    without_check_sum = struct.pack("b", ContractMeta.token_address_version) + contract_id_no_check_sum + struct.pack(
        ">I",
        idx)
    return bytes2str(
        base58.b58encode(without_check_sum + str2bytes(hashChain(without_check_sum)[0:ContractMeta.check_sum_length])))


def serialize_data(data_entry_list):
    custom_data_stack = []
    if not type(data_entry_list) is list:
        data_entry_list = [data_entry_list]
    for data in data_entry_list:
        custom_data_stack.append(data.bytes)
    return Deser.serialize_array(custom_data_stack)


def data_entry_from_base58_str(str_object):
    base58_str = base58.b58decode(str_object)
    return data_entries_from_bytes(base58_str)


def data_entries_from_bytes(bytes_object):
    length = struct.unpack(">H", bytes_object[0:2])[0]
    all_data = []
    pos_drift = 2
    for pos in range(length):
        [array_info, pos_drift] = parse_data_entry_array_size(bytes_object, pos_drift)
        all_data.append(array_info)
    return all_data


def parse_data_entry_array_size(bytes_object, start_position):
    if bytes_object[start_position: start_position + 1] == Type.public_key:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.key_length + 1]),
                start_position + Type.key_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.address:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.address_length + 1]),
                start_position + Type.address_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.amount:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.amount_length + 1]),
                start_position + Type.amount_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.int32:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.int32_length + 1]),
                start_position + Type.int32_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.short_text:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + struct.unpack(">H", bytes_object[
                                                                                                       start_position + 1:start_position + 3])[
            0] + 3]),
                start_position + struct.unpack(">H", bytes_object[start_position + 1: start_position + 3])[0] + 3)
    elif bytes_object[start_position: start_position + 1] == Type.contract_account:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.address_length + 1]),
                start_position + Type.address_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.token_id:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.token_address_length + 1]),
                start_position + Type.token_address_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.timestamp:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.amount_length + 1]),
                start_position + Type.amount_length + 1)
    elif bytes_object[start_position: start_position + 1] == Type.short_bytes:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + struct.unpack(">H", bytes_object[
                                                                                                       start_position + 1:start_position + 3])[
            0] + 3]),
                start_position + struct.unpack(">H", bytes_object[start_position + 1: start_position + 3])[0] + 3)


def data_entry_from_bytes(bytes_object):
    if len(bytes_object) == 0:
        raise ValueError("Invalid DataEntry %s" % str(bytes_object))
    elif bytes_object[0:1] == Type.public_key:
        return DataEntry(bytes2str(base58.b58encode(bytes_object[1:])), bytes_object[0:1])
    elif bytes_object[0:1] == Type.address:
        return DataEntry(bytes2str(base58.b58encode(bytes_object[1:])), bytes_object[0:1])
    elif bytes_object[0:1] == Type.amount:
        return DataEntry(struct.unpack(">Q", bytes_object[1:])[0], bytes_object[0:1])
    elif bytes_object[0:1] == Type.int32:
        return DataEntry(struct.unpack(">I", bytes_object[1:])[0], bytes_object[0:1])
    elif bytes_object[0:1] == Type.short_text:
        return DataEntry(bytes2str(bytes_object[3:]), bytes_object[0:1])
    elif bytes_object[0:1] == Type.contract_account:
        return DataEntry(bytes2str(base58.b58encode(bytes_object[1:])), bytes_object[0:1])
    elif bytes_object[0:1] == Type.token_id:
        return DataEntry(bytes2str(base58.b58encode(bytes_object[1:])), bytes_object[0:1])
    elif bytes_object[0:1] == Type.timestamp:
        return DataEntry(struct.unpack(">Q", bytes_object[1:])[0], bytes_object[0:1])
    elif bytes_object[0:1] == Type.short_bytes:
        return DataEntry(bytes2str(bytes_object[3:]), bytes_object[0:1])


def check_data_type(data, data_type):
    if data_type == Type.public_key:
        data_bytes = base58.b58decode(data)
        return len(data_bytes) == Type.key_length
    elif data_type == Type.address:
        data_bytes = base58.b58decode(data)
        return len(data_bytes) == Type.address_length
    elif data_type == Type.amount:
        data_bytes = struct.pack(">Q", data)
        return len(data_bytes) == Type.amount_length and struct.unpack(">Q", data_bytes)[0] > 0
    elif data_type == Type.int32:
        data_bytes = struct.pack(">I", data)
        return len(data_bytes) == Type.int32_length and struct.unpack(">I", data_bytes)[0] > 0
    elif data_type == Type.short_text:
        data_bytes = Deser.serialize_array(str2bytes(data))
        return struct.unpack(">H", data_bytes[0:2])[0] + 2 == len(data_bytes) and len(
            data_bytes) <= Type.max_short_text_size + 2
    elif data_type == Type.short_bytes:
        data_bytes = Deser.serialize_array(str2bytes(data))
        return struct.unpack(">H", data_bytes[0:2])[0] + 2 == len(data_bytes) and len(
            data_bytes) <= Type.max_short_bytes_size + 2
    else:
        return True


class DataEntry:
    def __init__(self, data, data_type):
        if not check_data_type(data, data_type):
            raise ValueError("Invalid DataEntry data: %s, type: %s" % (str(data), str(data_type)))
        if data_type == Type.public_key:
            self.data_bytes = base58.b58decode(data)
            self.data_type = 'public_key'
        elif data_type == Type.address:
            self.data_bytes = base58.b58decode(data)
            self.data_type = 'address'
        elif data_type == Type.amount:
            self.data_bytes = struct.pack(">Q", data)
            self.data_type = 'amount'
        elif data_type == Type.int32:
            self.data_bytes = struct.pack(">I", data)
            self.data_type = 'int32'
        elif data_type == Type.short_text:
            self.data_bytes = Deser.serialize_array(str2bytes(data))
            self.data_type = 'short_text'
        elif data_type == Type.contract_account:
            self.data_bytes = base58.b58decode(data)
            self.data_type = 'contract_account'
        elif data_type == Type.token_id:
            self.data_bytes = base58.b58decode(data)
            self.data_type = 'token_id'
        elif data_type == Type.timestamp:
            self.data_bytes = struct.pack(">Q", data)
            self.data_type = 'timestamp'
        elif data_type == Type.short_bytes:
            self.data_bytes = Deser.serialize_array(str2bytes(data))
            self.data_type = 'short_bytes'
        self.data = data
        self.bytes = data_type + self.data_bytes


class Type:
    public_key = struct.pack(">B", 1)
    key_length = 32
    address = struct.pack(">B", 2)
    address_length = 26
    amount = struct.pack(">B", 3)
    amount_length = 8
    int32 = struct.pack(">B", 4)
    int32_length = 4
    short_text = struct.pack(">B", 5)
    max_short_text_size = 140
    contract_account = struct.pack(">B", 6)
    contract_account_length = 26
    account = struct.pack(">B", 7)
    token_id = struct.pack(">B", 8)
    token_address_length = 30
    timestamp = struct.pack(">B", 9)
    boolean = struct.pack(">B", 10)
    short_bytes = struct.pack(">B", 11)
    max_short_bytes_size = 255
    balance = struct.pack(">B", 12)


