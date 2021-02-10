from .contract import Contract, DataEntry, Type
from .setting import Contract_Token_With_Split, Contract_Token_Without_Split, Contract_Payment_Channel,\
    Contract_Lock, Contract_Non_Fungible_Token
from .crypto import bytes2str, sign
import struct
import base58

class SystemContractHelper(object):
    send_function_index = 0
    deposit_function_index = 1
    withdraw_function_index = 2
    transfer_function_index = 3

    def send_data_stack_generator(self, recipient, amount):
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [recipient_data_entry, amount_data_entry]

    def deposit_data_stack_generator(self, sender, contract, amount):
        sender_data_entry = DataEntry(sender, Type.address)
        contract_data_entry = DataEntry(contract, Type.contract_account)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [sender_data_entry, contract_data_entry, amount_data_entry]

    def withdraw_data_stack_generator(self, contract, recipient, amount):
        contract_data_entry = DataEntry(contract, Type.contract_account)
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [contract_data_entry, recipient_data_entry, amount_data_entry]

    def transfer_data_entry_generator(self, sender, recipient, amount):
        sender_data_entry = DataEntry(sender, Type.address)
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [sender_data_entry, recipient_data_entry, amount_data_entry]

class TokenWithSplitContractHelper(object):
    contract_object = Contract(Contract_Token_With_Split)
    supersede_function_index = 0
    issue_function_index = 1
    destroy_function_index = 2
    split_function_index = 3
    send_function_index = 4
    transfer_function_index = 5
    deposit_function_index = 6
    withdraw_function_index = 7
    totalSupply_function_index = 8
    maxSupply_function_index = 9
    balanceOf_function_index = 10
    get_issuer_function_index = 11

    def register_data_stack_generator(self, max, unity, description):
        max_data_entry = DataEntry(max, Type.amount)
        unity_data_entry = DataEntry(unity, Type.amount)
        description_data_entry = DataEntry(description, Type.short_text)
        return [max_data_entry, unity_data_entry, description_data_entry]

    def supersede_data_stack_generator(self, new_issuer):
        new_issuer_data_entry = DataEntry(new_issuer, Type.address)
        return [new_issuer_data_entry]

    def issue_data_stack_generator(self, amount):
        amount_data_entry = DataEntry(amount, Type.amount)
        return [amount_data_entry]

    def destroy_data_stack_generator(self, amount):
        amount_data_entry = DataEntry(amount, Type.amount)
        return [amount_data_entry]

    def split_data_stack_generator(self, newUnity):
        newUnity_data_entry = DataEntry(newUnity, Type.amount)
        return [newUnity_data_entry]

    def send_data_stack_generator(self, recipient, amount):
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [recipient_data_entry, amount_data_entry]

    def transfer_data_stack_generator(self, sender, recipient, amount):
        sender_data_entry = DataEntry(sender, Type.address)
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [sender_data_entry, recipient_data_entry, amount_data_entry]

    def deposit_data_stack_generator(self, sender, contract, amount):
        sender_data_entry = DataEntry(sender, Type.address)
        contract_data_entry = DataEntry(contract, Type.contract_account)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [sender_data_entry, contract_data_entry, amount_data_entry]

    def withdraw_data_stack_generator(self, contract, recipient, amount):
        contract_data_entry = DataEntry(contract, Type.contract_account)
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [contract_data_entry, recipient_data_entry, amount_data_entry]

    def totalSupply_data_stack_generator(self):
        return []

    def maxSupply_data_stack_generator(self):
        return []

    def balanceOf_data_stack_generator(self, address):
        address_data_entry = DataEntry(address, Type.address)
        return [address_data_entry]

    def get_issuer_data_stack_generator(self):
        return []

    def issuer_db_key_generator(self):
        issuer_key_bytes = struct.pack(">B", 0)
        return base58.b58encode(issuer_key_bytes).decode()

    def maker_db_key_generator(self):
        maker_key_bytes = struct.pack(">B", 1)
        return base58.b58encode(maker_key_bytes).decode()

class TokenWithoutSplitContractHelper(object):
    contract_object = Contract(Contract_Token_Without_Split)
    supersede_function_index = 0
    issue_function_index = 1
    destroy_function_index = 2
    send_function_index = 3
    transfer_function_index = 4
    deposit_function_index = 5
    withdraw_function_index = 6
    totalSupply_function_index = 7
    maxSupply_function_index = 8
    balanceOf_function_index = 9
    get_issuer_function_index = 10

    def register_data_stack_generator(self, max, unity, description):
        max_data_entry = DataEntry(max, Type.amount)
        unity_data_entry = DataEntry(unity, Type.amount)
        description_data_entry = DataEntry(description, Type.short_text)
        return [max_data_entry, unity_data_entry, description_data_entry]

    def supersede_data_stack_generator(self, new_issuer):
        new_issuer_data_entry = DataEntry(new_issuer, Type.address)
        return [new_issuer_data_entry]

    def issue_data_stack_generator(self, amount):
        amount_data_entry = DataEntry(amount, Type.amount)
        return [amount_data_entry]

    def destroy_data_stack_generator(self, amount):
        amount_data_entry = DataEntry(amount, Type.amount)
        return [amount_data_entry]

    def send_data_stack_generator(self, recipient, amount):
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [recipient_data_entry, amount_data_entry]

    def transfer_data_stack_generator(self, sender, recipient, amount):
        sender_data_entry = DataEntry(sender, Type.address)
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [sender_data_entry, recipient_data_entry, amount_data_entry]

    def deposit_data_stack_generator(self, sender, contract, amount):
        sender_data_entry = DataEntry(sender, Type.address)
        contract_data_entry = DataEntry(contract, Type.contract_account)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [sender_data_entry, contract_data_entry, amount_data_entry]

    def withdraw_data_stack_generator(self, contract, recipient, amount):
        contract_data_entry = DataEntry(contract, Type.contract_account)
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [contract_data_entry, recipient_data_entry, amount_data_entry]

    def totalSupply_data_stack_generator(self):
        return []

    def maxSupply_data_stack_generator(self):
        return []

    def balanceOf_data_stack_generator(self, address):
        address_data_entry = DataEntry(address, Type.address)
        return [address_data_entry]

    def get_issuer_data_stack_generator(self):
        return []

    def issuer_db_key_generator(self):
        issuer_key_bytes = struct.pack(">B", 0)
        return base58.b58encode(issuer_key_bytes).decode()

    def maker_db_key_generator(self):
        maker_key_bytes = struct.pack(">B", 1)
        return base58.b58encode(maker_key_bytes).decode()

class PaymentChannelContractHelper(object):
    contract_object = Contract(Contract_Payment_Channel)
    create_and_load_function_index = 0
    extend_expiration_time_function_index = 1
    load_function_index = 2
    abort_function_index = 3
    unload_function_index = 4
    collect_payment_function_index = 5

    def register_data_stack_generator(self, token_id):
        token_id_data_entry = DataEntry(token_id, Type.token_id)
        return [token_id_data_entry]

    def create_and_load_data_stack_generator(self, recipient, amount, expiration_time):
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        expiration_time_data_entry = DataEntry(expiration_time, Type.timestamp)
        return [recipient_data_entry, amount_data_entry, expiration_time_data_entry]

    def extend_expiration_time_data_stack_generator(self, channel_id, new_expiration_time):
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        new_expiration_time_data_entry = DataEntry(new_expiration_time, Type.timestamp)
        return [channel_id_data_entry, new_expiration_time_data_entry]

    def load_data_stack_generator(self, channel_id, amount):
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [channel_id_data_entry, amount_data_entry]

    def abort_data_stack_generator(self, channel_id):
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        return [channel_id_data_entry]

    def unload_data_stack_generator(self, channel_id):
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        return [channel_id_data_entry]

    def collect_payment_data_stack_generator(self, channel_id, amount, signature):
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        amount_data_entry = DataEntry(amount, Type.amount)
        signature_data_entry = DataEntry(signature, Type.short_bytes_string)
        return [channel_id_data_entry, amount_data_entry, signature_data_entry]

    def generate_off_chain_payment_signature(self, private_key, channel_id, amount):
        channel_id_bytes = base58.b58decode(channel_id)
        channel_id_bytes_with_length = struct.pack(">H", len(channel_id_bytes)) + channel_id_bytes
        payment_amount_bytes = struct.pack(">Q", amount)
        message = channel_id_bytes_with_length + payment_amount_bytes
        return bytes2str(sign(private_key, message))

    def maker_db_key_generator(self):
        maker_key_bytes = struct.pack(">B", 0)
        return base58.b58encode(maker_key_bytes).decode()

    def token_id_db_key_generator(self):
        token_id_key_bytes = struct.pack(">B", 1)
        return base58.b58encode(token_id_key_bytes).decode()

    def contract_balance_db_key_generator(self, address):
        contract_balance_index_byte = struct.pack(">B", 0)
        address_data_entry = DataEntry(address, Type.address)
        contract_balance_key_bytes = contract_balance_index_byte + address_data_entry.bytes
        return base58.b58encode(contract_balance_key_bytes).decode()

    def channel_creator_db_key_generator(self, channel_id):
        channel_creator_index_byte = struct.pack(">B", 1)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_creator_key_bytes = channel_creator_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_creator_key_bytes).decode()

    def channel_creator_public_key_db_key_generator(self, channel_id):
        channel_creator_public_key_index_byte = struct.pack(">B", 2)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_creator_public_key_key_bytes = channel_creator_public_key_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_creator_public_key_key_bytes).decode()

    def channel_recipient_db_key_generator(self, channel_id):
        channel_recipient_index_byte = struct.pack(">B", 3)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_recipient_key_bytes = channel_recipient_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_recipient_key_bytes).decode()

    def channel_accumulated_load_db_key_generator(self, channel_id):
        channel_accumulated_load_index_byte = struct.pack(">B", 4)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_accumulated_load_key_bytes = channel_accumulated_load_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_accumulated_load_key_bytes).decode()

    def channel_accumulated_payment_db_key_generator(self, channel_id):
        channel_accumulated_payment_index_byte = struct.pack(">B", 5)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_accumulated_payment_key_bytes = channel_accumulated_payment_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_accumulated_payment_key_bytes).decode()

    def channel_expiration_time_db_key_generator(self, channel_id):
        channel_expiration_time_index_byte = struct.pack(">B", 6)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_expiration_time_key_bytes = channel_expiration_time_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_expiration_time_key_bytes).decode()

    def channel_status_db_key_generator(self, channel_id):
        channel_status_index_byte = struct.pack(">B", 7)
        channel_id_data_entry = DataEntry(channel_id, Type.short_bytes_string)
        channel_status_key_bytes = channel_status_index_byte + channel_id_data_entry.bytes
        return base58.b58encode(channel_status_key_bytes).decode()

class LockContractHelper(object):
    contract_object = Contract(Contract_Lock)
    lock_function_index = 0

    def register_data_stack_generator(self, token_id):
        token_id_data_entry = DataEntry(token_id, Type.token_id)
        return [token_id_data_entry]

    def lock_data_stack_generator(self, timestamp):
        timestamp_data_entry = DataEntry(timestamp, Type.timestamp)
        return [timestamp_data_entry]

    def maker_db_key_generator(self):
        maker_key_bytes = struct.pack(">B", 0)
        return base58.b58encode(maker_key_bytes).decode()

    def token_id_db_key_generator(self):
        token_id_key_bytes = struct.pack(">B", 1)
        return base58.b58encode(token_id_key_bytes).decode()

    def contract_balance_db_key_generator(self, address):
        contract_balance_index_byte = struct.pack(">B", 0)
        address_data_entry = DataEntry(address, Type.address)
        contract_balance_key_bytes = contract_balance_index_byte + address_data_entry.bytes
        return base58.b58encode(contract_balance_key_bytes).decode()

    def contract_lock_time_db_key_generator(self, address):
        contract_lock_time_index_byte = struct.pack(">B", 1)
        address_data_entry = DataEntry(address, Type.address)
        contract_lock_time_key_bytes = contract_lock_time_index_byte + address_data_entry.bytes
        return base58.b58encode(contract_lock_time_key_bytes).decode()

class NonFungibleContractHelper(object):
    contract_object = Contract(Contract_Non_Fungible_Token)
    supersede_function_index = 0
    issue_function_index = 1
    send_function_index = 2
    transfer_function_index = 3
    deposit_function_index = 4
    withdraw_function_index = 5

    def register_data_stack_generator(self):
        return []

    def supersede_data_stack_generator(self, new_issuer):
        new_issuer_data_entry = DataEntry(new_issuer, Type.address)
        return [new_issuer_data_entry]

    def issue_data_stack_generator(self, description):
        description_data_entry = DataEntry(description, Type.short_text)
        return [description_data_entry]

    def send_data_stack_generator(self, recipient, token_index):
        recipient_data_entry = DataEntry(recipient, Type.address)
        token_index_data_entry = DataEntry(token_index, Type.int32)
        return [recipient_data_entry, token_index_data_entry]

    def transfer_data_stack_generator(self, sender, recipient, token_index):
        sender_data_entry = DataEntry(sender, Type.address)
        recipient_data_entry = DataEntry(recipient, Type.address)
        token_index_data_entry = DataEntry(token_index, Type.int32)
        return [sender_data_entry, recipient_data_entry, token_index_data_entry]

    def deposit_data_stack_generator(self, sender, contract, token_index):
        sender_data_entry = DataEntry(sender, Type.address)
        contract_data_entry = DataEntry(contract, Type.contract_account)
        token_index_data_entry = DataEntry(token_index, Type.int32)
        return [sender_data_entry, contract_data_entry, token_index_data_entry]

    def withdraw_data_stack_generator(self, contract, recipient, token_index):
        contract_data_entry = DataEntry(contract, Type.contract_account)
        recipient_data_entry = DataEntry(recipient, Type.address)
        token_index_data_entry  = DataEntry(token_index, Type.int32)
        return [contract_data_entry, recipient_data_entry, token_index_data_entry]

    def issuer_db_key_generator(self):
        issuer_key_bytes = struct.pack(">B", 0)
        return base58.b58encode(issuer_key_bytes).decode()

    def maker_db_key_generator(self):
        maker_key_bytes = struct.pack(">B", 1)
        return base58.b58encode(maker_key_bytes).decode()
