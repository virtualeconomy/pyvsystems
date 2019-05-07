from .contract_build import *
from .error import *
from .deser import *
from .setting import *
import pyvsystems


def init_data_stack_gen(max, unity, desc):
    max = DataEntry(max, Type.amount)
    unit = DataEntry(unity, Type.amount)
    short_txt = DataEntry(desc, Type.short_text)
    init_data_stack = [max.bytes, unit.bytes, short_txt.bytes]
    return serialize_array(init_data_stack)


def supersede_data_stack_gen(new_iss):
    iss = DataEntry(new_iss, Type.address)
    supersede_data_stack = [iss.bytes]
    return serialize_array(supersede_data_stack)


def split_data_stack_gen(new_unity):
    unit = DataEntry(new_unity, Type.amount)
    split_data_stack = [unit.bytes]
    return serialize_array(split_data_stack)


def destroy_data_stack_gen(amount):
    am = DataEntry(amount, Type.amount)
    destroy_data_stack = [am.bytes]
    return serialize_array(destroy_data_stack)


def issue_data_stack_gen(amount):
    max = DataEntry(amount, Type.amount)
    issue_data_stack = [max.bytes]
    return serialize_array(issue_data_stack)


def send_data_stack_gen(recipient, amount):
    reci = DataEntry(recipient, Type.address)
    am = DataEntry(amount, Type.amount)
    send_data_stack = [reci.bytes, am.bytes]
    return serialize_array(send_data_stack)


def transfer_data_stack_gen(sender, recipient, amount):
    se = DataEntry(sender, Type.address)
    reci = DataEntry(recipient, Type.address)
    am = DataEntry(amount, Type.amount)
    transfer_data_stack = [se.bytes, reci.bytes, am.bytes]
    return serialize_array(transfer_data_stack)


def deposit_data_stack_gen(sender, smart_contract, amount):
    se = DataEntry(sender, Type.address)
    sc = DataEntry(smart_contract, Type.contract_account)
    am = DataEntry(amount, Type.amount)
    deposit_data_stack = [se.bytes, sc.bytes, am.bytes]
    return serialize_array(deposit_data_stack)


def withdraw_data_stack_gen(smart_contract, recipient, amount):
    sc = DataEntry(smart_contract, Type.contract_account)
    reci = DataEntry(recipient, Type.address)
    am = DataEntry(amount, Type.amount)
    withdraw_data_stack = [sc.bytes, reci.bytes, am.bytes]
    return serialize_array(withdraw_data_stack)


def total_supply_data_stack_gen():
    total_supply_data_stack = []
    return serialize_array(total_supply_data_stack)


def max_supply_data_stack_gen():
    max_supply_data_stack = []
    return serialize_array(max_supply_data_stack)


def balance_of_data_stack_gen(account):
    acc = DataEntry(account, Type.address)
    balance_of_data_stack = [acc.bytes]
    return serialize_array(balance_of_data_stack)


def get_issuer_data_stack_gen():
    get_issuer_data_stack = []
    return serialize_array(get_issuer_data_stack)


def custom_data_stack_gen(data_entry_list):
    custom_data_stack = []
    for data in data_entry_list:
        custom_data_stack.append(data.bytes)
    return serialize_array(custom_data_stack)


def data_entry_from_base58_str(str_object):
    if not type(str_object) is str:
        msg = 'Input must be string'
        pyvsystems.throw_error(msg, InvalidParameterException)
    else:
        base58_str = base58.b58decode(str_object)
        return parse_data_entry_arrays(base58_str)


def parse_data_entry_arrays(bytes_object):
    length = struct.unpack(">H", bytes_object[0:2])[0]
    all_data = []
    pos_drift = 2
    for pos in range(length):
        [array_info, pos_drift] = parse_data_entry_array_size(bytes_object, pos_drift)
        all_data.append(array_info)
    return all_data


def data_entry_from_bytes(bytes_object):
    if len(bytes_object) == 0:
        msg = 'Invalid Data Entry'
        pyvsystems.throw_error(msg, InvalidParameterException)
    elif not type(bytes_object) is bytes:
        msg = 'Input must be bytes'
        pyvsystems.throw_error(msg, InvalidParameterException)
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


class DataEntry:
    def __init__(self, data, data_type):
        if not type(data_type) is bytes:
            msg = 'Data Type must be bytes'
            pyvsystems.throw_error(msg, InvalidParameterException)
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
            if len(str2bytes(data)) > MAX_ATTACHMENT_SIZE:
                msg = 'description length must be <= %d' % MAX_ATTACHMENT_SIZE
                pyvsystems.throw_error(msg, InvalidParameterException)
            else:
                self.data_bytes = serialize_array(str2bytes(data))
                self.data_type = 'short_text'
        elif data_type == Type.contract_account:
            self.data_bytes = base58.b58decode(data)
            self.data_type = 'contract_account'
        else:
            msg = 'Invalid Data Entry'
            pyvsystems.throw_error(msg, InvalidParameterException)
        self.data = data
        self.bytes = data_type + self.data_bytes


class Type:
    public_key = bytes([1])
    key_length = 32
    address = bytes([2])
    address_length = 26
    amount = bytes([3])
    amount_length = 8
    int32 = bytes([4])
    int32_length = 4
    short_text = bytes([5])
    contract_account = bytes([6])
    contract_account_length = 26
    account = bytes([7])
