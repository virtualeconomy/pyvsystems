from .contract_build import *
from .error import *
from .deser import *
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
