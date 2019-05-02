from .setting import *
from .crypto import *
from .error import *
from .words import WORDS
from pyvsystems import is_offline
import pyvsystems
import time
import struct
import json
import math
import base58
import logging
import copy
from .opcode import *
from .deser import *
from .contract_build import *
from .contract_translator import *
from .contract_meta import ContractMeta as meta


class Contract(object):
    def __init__(self):
        self.default_contract = ContractBuild(True)

    def show_contract_function(self, bytes_string='', contract_id='', wrapper=None):
        if not bytes_string and not contract_id:
            msg = 'Input contract is empty!'
            pyvsystems.throw_error(msg, InvalidParameterException)

        if bytes_string and contract_id:
            msg = 'Multiple input in contract!'
            pyvsystems.throw_error(msg, InvalidParameterException)

        contract_translator = ContractTranslator()

        if contract_id:
            if not wrapper:
                msg = 'No wrapper information!'
                pyvsystems.throw_error(msg, InvalidParameterException)
            contract_content = self.get_contract_content(wrapper, contract_id)
            bytes_string = contract_translator.contract_from_json(contract_content)

        bytes_object = base58.b58decode(bytes_string)
        start_position = 0
        print("Total Length of Contract:", str(len(bytes_object)) + ' (Bytes)')

        language_code = bytes_object[start_position: meta.language_code_byte_length]
        bytes_to_hex = convert_bytes_to_hex(language_code)
        print("Language Code: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print(' '.join(bytes_to_hex))

        language_version = bytes_object[meta.language_code_byte_length:(meta.language_code_byte_length
                                                                        + meta.language_version_byte_length)]
        bytes_to_hex = convert_bytes_to_hex(language_version)
        print("Language Version: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print(' '.join(bytes_to_hex))

        [trigger_with_header, trigger_end] = parse_array_size(bytes_object, meta.language_code_byte_length
                                                              + meta.language_version_byte_length)
        [trigger, _] = parse_arrays(trigger_with_header)
        bytes_to_hex = convert_bytes_to_hex(trigger[0])
        print("Trigger: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print("id" + " | byte")
        print("00 | " + ' '.join(bytes_to_hex))

        [descriptor_arrays, descriptor_end] = parse_array_size(bytes_object, trigger_end)
        [descriptor, bytes_length] = parse_arrays(descriptor_arrays)
        print("Descriptor: " + "(" + str(bytes_length) + " Bytes)")
        print("id" + " | byte")
        contract_translator.print_bytes_arrays(descriptor)

        [state_var_arrays, state_var_end] = parse_array_size(bytes_object, descriptor_end)
        [state_var, bytes_length] = parse_arrays(state_var_arrays)
        print("State Variable: " + "(" + str(bytes_length) + " Bytes)")
        print("id" + " | byte")
        contract_translator.print_bytes_arrays(state_var)

        [texture, _] = parse_arrays(bytes_object[state_var_end:len(bytes_object)])
        all_info = contract_translator.print_texture_from_bytes(texture)

        functions_bytes = copy.deepcopy(trigger + descriptor)
        print("All Functions with Opcode:")
        contract_translator.print_functions(functions_bytes, all_info)

    def get_contract_info(self, wrapper, contract_id):
        try:
            resp = wrapper.request('contract/info/%s' % (contract_id))
            logging.debug(resp)
            return resp['info']
        except Exception as ex:
            msg = "Failed to get contract info. ({})".format(ex)
            pyvsystems.throw_error(msg, NetworkException)
            return 0

    def get_contract_content(self, wrapper, contract_id):
        try:
            resp = wrapper.request('contract/content/%s' % (contract_id))
            logging.debug(resp)
            return resp
        except Exception as ex:
            msg = "Failed to get contract content. ({})".format(ex)
            pyvsystems.throw_error(msg, NetworkException)
            return 0

    def get_token_balance(self, wrapper, address, token_id):
        if not address:
            msg = 'Address required'
            pyvsystems.throw_error(msg, MissingAddressException)
            return None
        try:
            resp = wrapper.request('/balance/%s/%s' % (address, token_id))
            logging.debug(resp)
            return resp
        except Exception as ex:
            msg = "Failed to get token balance. ({})".format(ex)
            pyvsystems.throw_error(msg, NetworkException)
            return 0

    def contract_permitted(self, split=True):
        if split:
            contract = self.default_contract.create('vdds', 1, split=True)
        else:
            contract = self.default_contract.create('vdds', 1, split=False)
        return contract

    @staticmethod
    def register_contract(account, contract, data_stack, description='', tx_fee=DEFAULT_REGISTER_CONTRACT_FEE,
                          fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        MIN_CONTRACT_STRING_SIZE = int(math.ceil(math.log(256) / math.log(58) * MIN_CONTRACT_BYTE_SIZE))
        if not account.privateKey:
            msg = 'Private key required'
            pyvsystems.throw_error(msg, MissingPrivateKeyException)
        elif len(contract) < MIN_CONTRACT_STRING_SIZE:
            msg = 'Contract String must be at least %d long' % MIN_CONTRACT_STRING_SIZE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif tx_fee < DEFAULT_REGISTER_CONTRACT_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_REGISTER_CONTRACT_FEE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif len(description) > MAX_ATTACHMENT_SIZE:
            msg = 'Attachment length must be <= %d' % MAX_ATTACHMENT_SIZE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif not is_offline() and account.balance() < tx_fee:
            msg = 'Insufficient VSYS balance'
            pyvsystems.throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", REGISTER_CONTRACT_TX_TYPE) + \
                    struct.pack(">H", len(base58.b58decode(contract))) + \
                    base58.b58decode(contract) + \
                    struct.pack(">H", len(data_stack)) + \
                    data_stack + \
                    struct.pack(">H", len(description)) + \
                    str2bytes(description) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(account.privateKey, sData))
            description_str = bytes2str(base58.b58encode(str2bytes(description)))
            data_stack_str = bytes2str(base58.b58encode(data_stack))
            data = json.dumps({
                "senderPublicKey": account.publicKey,
                "contract": contract,
                "initData": data_stack_str,
                "description": description_str,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "signature": signature
            })

            return account.wrapper.request('/contract/broadcast/register', data)


    @staticmethod
    def execute_contract(account, contract_id, func_id, data_stack, attachment='', tx_fee=DEFAULT_EXECUTE_CONTRACT_FEE,
                         fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if not account.privateKey:
            msg = 'Private key required'
            pyvsystems.throw_error(msg, MissingPrivateKeyException)
        elif tx_fee < DEFAULT_EXECUTE_CONTRACT_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_EXECUTE_CONTRACT_FEE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif len(attachment) > MAX_ATTACHMENT_SIZE:
            msg = 'Attachment length must be <= %d' % MAX_ATTACHMENT_SIZE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            pyvsystems.throw_error(msg, InvalidParameterException)
        elif not is_offline() and account.balance() < tx_fee:
            msg = 'Insufficient VSYS balance'
            pyvsystems.throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", EXECUTE_CONTRACT_FUNCTION_TX_TYPE) + \
                    base58.b58decode(contract_id) + \
                    struct.pack(">H", func_id) + \
                    struct.pack(">H", len(data_stack)) + \
                    data_stack + \
                    struct.pack(">H", len(attachment)) + \
                    str2bytes(attachment) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(account.privateKey, sData))
            description_str = bytes2str(base58.b58encode(str2bytes(attachment)))
            data_stack_str = bytes2str(base58.b58encode(data_stack))
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


    def get_contract_status(self, wrapper, tx_id):
        try:
            resp = wrapper.request('/transactions/info/%s' % (tx_id))
            logging.debug(resp)
        except:
            resp = 0
            pass
        try:
            status = resp["status"]
            if status == "Success":
                print("height: " + resp["height"])
                return True
            else:
                return False
        except KeyError:
            pass
            return False

    def timed_get_contract_status(self, wrapper, tx_id):
        retries = 1
        while retries > 0:
            status = self.get_contract_status(wrapper, tx_id)
            if status is True:
                return True
            else:
                time.sleep(10.0)
                status = self.get_contract_status(wrapper, tx_id)
                if status is True:
                    return True
                else:
                    return False



