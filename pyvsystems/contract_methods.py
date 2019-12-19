import json

from .data_entry import serialize_data
from .contract_translator import *
from .setting import *
from .crypto import *
import time


def get_contract_info(wrapper, contract_id):
    resp = wrapper.request('/contract/info/%s' % contract_id)
    if resp.get('error'):
        return resp
    else:
        logging.debug(resp)
        return resp.get('info')


def get_contract_content(wrapper, contract_id):
    resp = wrapper.request('/contract/content/%s' % contract_id)
    logging.debug(resp)
    return resp


def get_token_balance(wrapper, address, token_id):
    if not address:
        msg = 'Address required'
        throw_error(msg, MissingAddressException)
        return None
    if token_id is None:
        msg = 'Token ID required'
        throw_error(msg, MissingTokenIdException)
        return None
    resp = wrapper.request('/contract/balance/%s/%s' % (address, token_id))

    if resp.get('error'):
        return resp
    else:
        return resp.get('balance')


def get_token_info(wrapper, token_id):
    if token_id is None:
        msg = 'Token ID required'
        throw_error(msg, MissingTokenIdException)
        return None

    resp = wrapper.request('/contract/tokenInfo/%s' % token_id)
    logging.debug(resp)
    return resp


def register_contract(account, contract, data_stack, description='', tx_fee=DEFAULT_REGISTER_CONTRACT_FEE,
                      fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
    data_stack_bytes = serialize_data(data_stack)
    if timestamp == 0:
        timestamp = int(time.time() * 1000000000)
    sData = struct.pack(">B", REGISTER_CONTRACT_TX_TYPE) + \
            struct.pack(">H", len(contract.contract_bytes)) + \
            contract.contract_bytes + \
            struct.pack(">H", len(data_stack_bytes)) + \
            data_stack_bytes + \
            struct.pack(">H", len(description)) + \
            str2bytes(description) + \
            struct.pack(">Q", tx_fee) + \
            struct.pack(">H", fee_scale) + \
            struct.pack(">Q", timestamp)
    signature = bytes2str(sign(account.privateKey, sData))
    description_str = description
    data_stack_str = bytes2str(base58.b58encode(data_stack_bytes))
    data = json.dumps({
        "senderPublicKey": account.publicKey,
        "contract": contract.contract_bytes_string,
        "initData": data_stack_str,
        "description": description_str,
        "fee": tx_fee,
        "feeScale": fee_scale,
        "timestamp": timestamp,
        "signature": signature
    })

    return account.wrapper.request('/contract/broadcast/register', data)


def execute_contract(account, contract_id, func_id, data_stack, attachment='', tx_fee=DEFAULT_EXECUTE_CONTRACT_FEE,
                     fee_scale=DEFAULT_FEE_SCALE, timestamp=0):

    data_stack_bytes = serialize_data(data_stack)
    if timestamp == 0:
        timestamp = int(time.time() * 1000000000)
    sData = struct.pack(">B", EXECUTE_CONTRACT_FUNCTION_TX_TYPE) + \
            base58.b58decode(contract_id) + \
            struct.pack(">H", func_id) + \
            struct.pack(">H", len(data_stack_bytes)) + \
            data_stack_bytes + \
            struct.pack(">H", len(attachment)) + \
            str2bytes(attachment) + \
            struct.pack(">Q", tx_fee) + \
            struct.pack(">H", fee_scale) + \
            struct.pack(">Q", timestamp)
    signature = bytes2str(sign(account.privateKey, sData))
    description_str = bytes2str(base58.b58encode(str2bytes(attachment)))
    data_stack_str = bytes2str(base58.b58encode(data_stack_bytes))
    data = json.dumps({
        "senderPublicKey": account.publicKey,
        "contractId": contract_id,
        "functionIndex": func_id,
        "functionData": data_stack_str,
        "attachment": description_str,
        "fee": tx_fee,
        "feeScale": fee_scale,
        "timestamp": timestamp,
        "signature": signature
    })

    return account.wrapper.request('/contract/broadcast/execute', data)


def calc_check_sum(without_check_sum):
    return str2bytes(hashChain(without_check_sum)[0:meta.check_sum_length])


def token_id_from_bytes(contract_id, idx):
    address_bytes = base58.b58decode(contract_id)
    contract_id_no_check_sum = address_bytes[1:(len(address_bytes) - meta.check_sum_length)]
    without_check_sum = struct.pack("b", meta.token_address_version) + contract_id_no_check_sum + struct.pack(">I", idx)
    return bytes2str(base58.b58encode(without_check_sum + calc_check_sum(without_check_sum)))




