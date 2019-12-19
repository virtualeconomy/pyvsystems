from .error import *
from .deser import *
from .crypto import *
import base58


def init_data_stack_gen(max, unity, desc):
    maximum = DataEntry(max, Type.amount)
    unit = DataEntry(unity, Type.amount)
    short_txt = DataEntry(desc, Type.short_text)
    init_data_stack = [maximum, unit, short_txt]
    return init_data_stack

def supersede_data_stack_gen(new_iss):
    iss = DataEntry(new_iss, Type.address)
    supersede_data_stack = [iss]
    return supersede_data_stack


def split_data_stack_gen(new_unity):
    unit = DataEntry(new_unity, Type.amount)
    split_data_stack = [unit]
    return split_data_stack


def destroy_data_stack_gen(amount):
    am = DataEntry(amount, Type.amount)
    destroy_data_stack = [am]
    return destroy_data_stack


def issue_data_stack_gen(amount):
    max = DataEntry(amount, Type.amount)
    issue_data_stack = [max]
    return issue_data_stack


def send_data_stack_gen(recipient, amount):
    reci = DataEntry(recipient, Type.address)
    am = DataEntry(amount, Type.amount)
    send_data_stack = [reci, am]
    return send_data_stack


def transfer_data_stack_gen(sender, recipient, amount):
    se = DataEntry(sender, Type.address)
    reci = DataEntry(recipient, Type.address)
    am = DataEntry(amount, Type.amount)
    transfer_data_stack = [se, reci, am]
    return transfer_data_stack


def deposit_data_stack_gen(sender, smart_contract, amount):
    se = DataEntry(sender, Type.address)
    sc = DataEntry(smart_contract, Type.contract_account)
    am = DataEntry(amount, Type.amount)
    deposit_data_stack = [se, sc, am]
    return deposit_data_stack


def withdraw_data_stack_gen(smart_contract, recipient, amount):
    sc = DataEntry(smart_contract, Type.contract_account)
    reci = DataEntry(recipient, Type.address)
    am = DataEntry(amount, Type.amount)
    withdraw_data_stack = [sc, reci, am]
    return withdraw_data_stack


def total_supply_data_stack_gen():
    total_supply_data_stack = []
    return total_supply_data_stack


def max_supply_data_stack_gen():
    max_supply_data_stack = []
    return max_supply_data_stack


def balance_of_data_stack_gen(account):
    acc = DataEntry(account, Type.address)
    balance_of_data_stack = [acc]
    return balance_of_data_stack


def get_issuer_data_stack_gen():
    get_issuer_data_stack = []
    return get_issuer_data_stack


def serialize_data(data_entry_list):
    custom_data_stack = []
    if not type(data_entry_list) is list:
        data_entry_list = [data_entry_list]
    for data in data_entry_list:
        custom_data_stack.append(data.bytes)
    return serialize_array(custom_data_stack)


def create_data(list_data_tuple):
    custom_data = []
    if not type(list_data_tuple) is list:
        list_data_tuple = [list_data_tuple]
    for data in list_data_tuple:
        if type(data) == tuple:
            if data[1] == 'public_key' and type(data[0]) == str:
                custom_data.append(DataEntry(data[0], bytes([1])))
            if data[1] == 'address' and type(data[0]) == str:
                custom_data.append(DataEntry(data[0], bytes([2])))
            if data[1] == 'amount' and type(data[0]) == int:
                custom_data.append(DataEntry(data[0], bytes([3])))
            if data[1] == 'int32' and type(data[0]) == int:
                custom_data.append(DataEntry(data[0], bytes([4])))
            if data[1] == 'short_text' and type(data[0]) == str:
                custom_data.append(DataEntry(data[0], bytes([5])))
            if data[1] == 'contract_account' and type(data[0]) == str:
                custom_data.append(DataEntry(data[0], bytes([6])))
        else:
            msg = 'Invalid Data Entry'
            throw_error(msg, InvalidParameterException)
    return custom_data


def data_entry_from_base58_str(str_object):
    if not type(str_object) is str:
        msg = 'Input must be string'
        throw_error(msg, InvalidParameterException)
    else:
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
        return (data_entry_from_bytes(bytes_object[start_position:start_position +
                struct.unpack(">H", bytes_object[start_position + 1: start_position + 3])[0] + 3]),
                start_position + struct.unpack(">H", bytes_object[start_position + 1: start_position + 3])[0] + 3)
    elif bytes_object[start_position: start_position + 1] == Type.contract_account:
        return (data_entry_from_bytes(bytes_object[start_position:start_position + Type.address_length + 1]),
                start_position + Type.address_length + 1)


def data_entry_from_bytes(bytes_object):
    if len(bytes_object) == 0:
        msg = 'Invalid Data Entry'
        throw_error(msg, InvalidParameterException)
    elif not type(bytes_object) is bytes:
        msg = 'Input must be bytes'
        throw_error(msg, InvalidParameterException)
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
        return len(data_bytes) == Type.amount_length and struct.unpack(">I", data_bytes)[0] > 0
    elif data_type == Type.short_text:
        data_bytes = serialize_array(str2bytes(data))
        return struct.unpack(">H", data_bytes[0:2])[0] + 2 == len(data_bytes) and len(data_bytes) <= Type.max_short_text_size + 2
    else:
        return True


class DataEntry:
    def __init__(self, data, data_type):
        if not type(data_type) is bytes:
            msg = 'Data Type must be bytes'
            throw_error(msg, InvalidParameterException)
        if not check_data_type(data, data_type):
            msg = 'Invalid DataEntry'
            throw_error(msg, InvalidParameterException)
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
            self.data_bytes = serialize_array(str2bytes(data))
            self.data_type = 'short_text'
        elif data_type == Type.contract_account:
            self.data_bytes = base58.b58decode(data)
            self.data_type = 'contract_account'
        else:
            msg = 'Invalid Data Entry'
            throw_error(msg, InvalidParameterException)
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
