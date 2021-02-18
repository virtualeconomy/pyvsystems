from .crypto import *
from .deser import Deser
from .setting import ContractMeta
from .error import *
from typing import NamedTuple
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
        # Wrong language code length
        raise Exception("Wrong language code length")


def language_version_builder(version):
    if len(struct.pack(">I", version)) == ContractMeta.language_version_byte_length:
        return struct.pack(">I", version)
    else:
        # Wrong language version length
        raise Exception("Wrong language code length")


def bytes_builder_from_list(input_list):
    if type(input_list) is list:
        return Deser.serialize_array(Deser.serialize_arrays(input_list))
    else:
        # The input should be a list
        raise Exception("The input should be a list")

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
    index = bytes_object[start_position: start_position + 1]
    data_type = Type().by_index(index)
    return data_type.parse_data_entry_size(bytes_object, start_position)

def data_entry_from_bytes(bytes_object):
    if len(bytes_object) == 0:
        raise ValueError("Invalid DataEntry %s" % str(bytes_object))
    else:
        type_object = Type().by_index(bytes_object[0:1])
        return type_object.data_entry_from_data_bytes(bytes_object[1:])

class DataEntry:
    def __init__(self, data, data_type):
        if not data_type.check_data_type(data):
            raise ValueError("Invalid DataEntry data: %s, type: %s" % (str(data), str(data_type)))
        self.data_bytes = data_type.data_to_bytes(data)
        self.data_name = data_type.name
        self.data = data
        self.bytes = data_type.index + self.data_bytes

class TypeStruct(NamedTuple):
  index: bytes
  length: int
  name: str
  data_category: str

  def check_data_type(self, data):
      data_bytes = self.data_to_bytes(data)
      if self.data_category == 'b58':
          return len(data_bytes) == self.length
      elif self.data_category == 'long':
          return len(data_bytes) == self.length and struct.unpack(">Q", data_bytes)[0] >= 0
      elif self.data_category == 'int':
          return len(data_bytes) == self.length and struct.unpack(">I", data_bytes)[0] >= 0
      elif self.data_category == 'short_type':
          return struct.unpack(">H", data_bytes[0:2])[0] + 2 == len(data_bytes) and len(
              data_bytes) <= Type.short_text.length + 2
      elif self.data_category == 'short_bytes_string':
          return struct.unpack(">H", data_bytes[0:2])[0] + 2 == len(data_bytes) and len(
              data_bytes) <= Type.short_text.length + 2
      else:
          return True

  def data_to_bytes(self, data):
      if self.data_category == 'b58':
          return base58.b58decode(data)
      elif self.data_category == 'long':
          return struct.pack(">Q", data)
      elif self.data_category == 'int':
          return struct.pack(">I", data)
      elif self.data_category == 'short_type':
          return Deser.serialize_array(str2bytes(data))
      elif self.data_category == 'short_bytes_string':
          return Deser.serialize_array(base58.b58decode(data))

  def parse_data_entry_size(self, bytes_object, start_position):
      if (self.data_category == 'short_type'):
          return (data_entry_from_bytes(bytes_object[start_position:start_position + struct.unpack(">H", bytes_object[
                                                                                                         start_position + 1:start_position + 3])[
              0] + 3]),
                  start_position + struct.unpack(">H", bytes_object[start_position + 1: start_position + 3])[0] + 3)
      elif (self.data_category == 'short_bytes_string'):
          return (data_entry_from_bytes(bytes_object[start_position:start_position + struct.unpack(">H", bytes_object[
                                                                                                         start_position + 1:start_position + 3])[
              0] + 3]),
                  start_position + struct.unpack(">H", bytes_object[start_position + 1: start_position + 3])[0] + 3)
      else:
          return (data_entry_from_bytes(bytes_object[start_position:start_position + self.length + 1]),
                  start_position + self.length + 1)

  def data_entry_from_data_bytes(self, data):
      if self.data_category == 'b58':
          return DataEntry(bytes2str(base58.b58encode(data)), self)
      elif self.data_category == 'long':
          return DataEntry(struct.unpack(">Q", data)[0], self)
      elif self.data_category == 'int':
          return DataEntry(struct.unpack(">I", data)[0], self)
      elif self.data_category == 'short_type':
          return DataEntry(bytes2str(data[2:]), self)
      elif self.data_category == 'short_bytes_string':
          return DataEntry(base58.b58encode(data[2:]), self)



class Type:
    public_key = TypeStruct(struct.pack(">B", 1), 32, 'public_key', 'b58')
    address = TypeStruct(struct.pack(">B", 2), 26, 'address', 'b58')
    amount = TypeStruct(struct.pack(">B", 3), 8, 'amount', 'long')
    int32 = TypeStruct(struct.pack(">B", 4), 4, 'int32', 'int')
    short_text = TypeStruct(struct.pack(">B", 5), 140, 'short_text', 'short_type')
    contract_account = TypeStruct(struct.pack(">B", 6), 26, 'contract_account', 'b58')
    account = TypeStruct(struct.pack(">B", 7), 26, 'account', 'b58')
    token_id = TypeStruct(struct.pack(">B", 8), 30, 'token_id', 'b58')
    timestamp = TypeStruct(struct.pack(">B", 9), 8, 'timestamp', 'long')
    boolean = TypeStruct(struct.pack(">B", 10), 1, 'boolean', 'bool')
    short_bytes = TypeStruct(struct.pack(">B", 11), 255, 'short_bytes', 'short_type')
    short_bytes_string = TypeStruct(struct.pack(">B", 11), 255, 'short_bytes_string', 'short_bytes_string')
    balance = TypeStruct(struct.pack(">B", 12), 8, 'balance', 'long')

    def by_index(self, index):
        if index == 1 or index == struct.pack(">B", 1):
            return Type.public_key
        elif index == 2 or index == struct.pack(">B", 2):
            return Type.address
        elif index == 3 or index == struct.pack(">B", 3):
            return Type.amount
        elif index == 4 or index == struct.pack(">B", 4):
            return Type.int32
        elif index == 5 or index == struct.pack(">B", 5):
            return Type.short_text
        elif index == 6 or index == struct.pack(">B", 6):
            return Type.contract_account
        elif index == 7 or index == struct.pack(">B", 7):
            return Type.account
        elif index == 8 or index == struct.pack(">B", 8):
            return Type.token_id
        elif index == 9 or index == struct.pack(">B", 9):
            return Type.timestamp
        elif index == 10 or index == struct.pack(">B", 10):
            return Type.boolean
        elif index == 11 or index == struct.pack(">B", 11):
            return Type.short_bytes_string
        elif index == 12 or index == struct.pack(">B", 12):
            return Type.balance
