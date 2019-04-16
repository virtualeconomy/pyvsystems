#from .setting import *
from .crypto import *
from .error import *
from .words import WORDS
from pyvsystems import is_offline
import pyvsystems
import time
import struct
import json
import base58
import logging
import copy


class Contract(object):
    def __init__(self):
        self.str2bytes = lambda s: s.encode('hex')
        self.language_code_byte_length = 4
        self.language_version_byte_length = 4
        self.data_type_list = {'01': 'PublicKey', '02': 'Address', '03': 'Amount', '04': 'Int32', '05': 'ShortText',
                               '06': 'ContractAccount', '07': 'Account'}
        self.test = 'JC9U69xcoTWJ71v82TojKETj3SAsxyh3nYACiheZMDBgE6XKshzgupsRmSk3y1aijZJxWu4DSX96nMpStH2ESv3P4VC4MogHcN8UcCiaLiCt2af1b7zkhZtGq6ckrvHjijJ7ZHZugp8bzyUTs55SnZ5o2tockgM8jhtnfVNRPEPq8My9QNDDyZRJyxyJnE6p8kB3PDEPk1WsBxe68APAaLqjN4ACRCv5kyhKTjaEixRz6yn62W8PRi5PpzD4KEtg1DrxwhwqsFWCLrNPsw8vTuSB3DrNgCq72FEQJAAtdDS29kPmaQYeQG2YQzUrtKyteAdMzQw2B17wUsQj4tnkFkec5VbbV4mFZ5zhVsCv5UErZiKKPiBgefjQjfnuYNV6PA4r5T6XrtW2zi5MvzEym3vt3PpzodHd9xY5UftGRmkWjZ1atRfRsheDw6CKcsjdEGNS5J7bfvLj3KAckRPjp1wAP5CTKASSLvGVBCyieNyJLmdfguhEEg5xpKXiJdzTAnQDrBYdhCpRq9xTcBK5ueQZ5vqEZt1vbBBLVzkdmmt54tZXvpvW3TPwKqLtz26zdtAPntmjLyqqNKbmzb8MrgiyjyC8YmYgnLUkeU8q2ksmZKZ8aoHEW5zF3ztQ7qNvaxY86NY3AHkpcuUjbdaMxEMKAQ3Qc2fVcwHVoJoEz7pSSUHvnUcZcnYMMmGR52gwNasUxVAm2LmbNbuyQvnxpJXd2yQryWQjgHcgDoRSroRuV6rftvGz6d9FbhytyrUEc9Ae6uZu7W6cAtB75jBtaBUk9K9cootsqEu2Y1PUE7B832X3j4UWveC73XnkRsz5U8EStNWvJXYZ2QitmZBSpCYMP8bnEfnqtxmGk7B1iT3tqWaJ5QX5DgkQ189UXimGCjAs31LtFSCuGWzkJnoR3H5Yno465v7WHLkbewKqrDpaAbgj82pja8uuSj8uZGBrEDXu2KdP4R4UbfDUXYmGtiNTwDDfwdyAv4BrvyQFuWKVWnMDhkSjsjSVJmLx5qwNq3EBZzN7tZd9UBQ3552rSfu48Y7fvTh54x9FjYMDCmtUFmsxrnWFgbGe8Gypfwpk9qKHe4Pe7Qjx5ppzAW48FDtdtjznh6wk4wF33y46cfrTEogULvkifb8WjqoXaRytdxUzcm6M23XiKUfQAVygFJXBJfCU3VbxFZgLib2Lgp2dAeB5myJzRayKi9tJQVzLrYr4NEFWpzJbxiZxyY14XyHXWTyvGgQHW5DGkgRiWDm7mbybtb9BvKrEtkKCZ'

        self.assert_opc = {'01': 'GteqZeroAssert', '02': 'LteqAssert', '03': 'LtInt64Assert', '04': 'GtZeroAssert',
                           '05': 'EqAssert', '06': 'IsCallerOriginAssert', '07': 'IsSignerOriginAssert'}
        self.load_opc = {'01': 'SignerLoad', '02': 'CallerLoad'}
        self.CDBV_opc = {'01': 'SetCDBV'}
        self.CDBVR_opc = {'01': 'GetCDBVR'}
        self.TDB_opc = {'01': 'NewTokenTDB', '02': 'SplitTDB'}
        self.TDBR_opc = {'01': 'GetTDBR', '02': 'TotalTDBR'}
        self.TDBA_opc = {'01': 'DepositTDBA', '02': 'WithdrawTDBA', '03': 'TransferTDBA'}
        self.TDBAR_opc = {'01': 'BalanceTBDAR'}
        self.opc_type = {'01': ['AssertOpc', self.assert_opc], '02': ['LoadOpc', self.load_opc], '03': ['CDBVOpc', self.CDBV_opc],
                         '04': ['CDBVROpc', self.CDBVR_opc], '05': ['TDBOpc', self.TDB_opc], '06': ['TDBROpc', self.TDBR_opc],
                         '07': ['TDBAOpc', self.TDBA_opc], '08': ['TDBAROpc', self.TDBAR_opc], '09': ['ReturnOpc', {}]}
        self.opc_function_name = {'0106': 'opc_assert_caller', '0107': 'opc_assert_singer',
                                  '0201': 'opc_load_env_signer signer', '0202': 'opc_load_env_caller caller',
                                  '0301': 'opc_cdbv_set db.', '0401': 'opc_cdbvr_get db.', '0501': 'opc_tdb_new',
                                  '0601': 'opc_tdbr_get tdb.', '0602': 'opc_tdbr_total tdb.', '0701': 'opc_tdba_deposit',
                                  '0702': 'opc_tdba_withdraw', '0703': 'opc_tdba_transfer', '0801': 'opc_tdbar_balance',
                                  '0900': 'opc_return_last'}

    def show_contract_function(self, byte_string = '', contract_json = ''):
        byte_string = self.test
        bytes_object = base58.b58decode(byte_string)
        start_position = 0

        language_code = bytes_object[start_position:self.language_code_byte_length]
        bytes_to_hex = self.convert_bytes_to_hex(language_code)
        print("Language Code: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print(' '.join(bytes_to_hex))

        language_version = bytes_object[self.language_code_byte_length:(self.language_code_byte_length
                                                                        + self.language_version_byte_length)]
        bytes_to_hex = self.convert_bytes_to_hex(language_version)
        print("Language Version: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print(' '.join(bytes_to_hex))

        [initializer, initializer_end] = self.parse_array_size(bytes_object, self.language_code_byte_length
                                                               + self.language_version_byte_length)
        bytes_to_hex = self.convert_bytes_to_hex(initializer)
        print("Initializer: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print("id" + " | byte")
        print("00 | " + ' '.join(bytes_to_hex))

        [descriptor_arrays, descriptor_end] = self.parse_array_size(bytes_object, initializer_end)
        [descriptor, bytes_length]= self.parse_arrays(descriptor_arrays)
        print("Descriptor: " + "(" + str(bytes_length) + " Bytes)")
        print("id" + " | byte")
        self.print_bytes_arrays(descriptor)

        [state_var_arrays, state_var_end] = self.parse_array_size(bytes_object, descriptor_end)
        [state_var, bytes_length] = self.parse_arrays(state_var_arrays)
        print("State Variable: " + "(" + str(bytes_length) + " Bytes)")
        print("id" + " | byte")
        self.print_bytes_arrays(state_var)

        [texture, _] = self.parse_arrays(bytes_object[state_var_end:len(bytes_object)])
        all_info = self.texture_from_bytes(texture)

        functions = copy.deepcopy([initializer] + descriptor)
        print("All Functions with Opcode:")
        self.print_functions(functions, all_info)

    def print_functions(self, functions_opcode, all_info):
        if len(functions_opcode) != (len(all_info[0]) + len(all_info[1])):
            logging.exception("Error: Functions are not well defined in opc and texture!")
        else:
            functions_spec = copy.deepcopy([all_info[0][0]] + all_info[1])
            for i in range(len(functions_opcode)):
                [function_id_byte, _, list_para_type_bytes, list_opc_bytes] = \
                    self.details_from_opcode(functions_opcode[i])
                function_id = "{:02d}".format(self.shorts_from_byte_array(self.convert_bytes_to_hex(function_id_byte)))
                if len(list_para_type_bytes) > 0:
                    list_para_type = [self.data_type_list[para]
                                      for para in self.convert_bytes_to_hex(list_para_type_bytes)]
                else:
                    list_para_type = []
                list_opc = [self.convert_bytes_to_hex(list_opc_line) for list_opc_line in list_opc_bytes]
                list_opc_name = [self.opc_function_name[opc_list[0] + opc_list[1]]
                                 if len(opc_list) >= 2 else logging.exception("Error: opc function is not right!")
                                 for opc_list in list_opc]
                database_index = all_info[2]
                self.print_a_function(function_id, functions_spec[i], list_para_type, list_opc_name, list_opc, database_index)

    @staticmethod
    def print_a_function(function_id, functions_spec, list_para_type, list_opc_name, list_opc, database_index):
        function_name = functions_spec[0]
        return_type = functions_spec[1]
        if len(functions_spec) >= 2:
            list_para = functions_spec[2:]
        else:
            list_para = []
        if len(list_para_type) != len(list_para):
            logging.exception("Error: list of parameter is not right!")
        else:
            print("(id: " + function_id + ") " + return_type + " function " + function_name + "(", end='')
            if len(list_para_type) > 0:
                for i in range(len(list_para_type)):
                    print(list_para_type[i] + ' ', end='')
                    if i == (len(list_para_type) - 1):
                        print(list_para[i] + ')')
                    else:
                        print(list_para[i] + ', ', end='')
            else:
                print(")")
        if len(list_opc_name) != len(list_opc):
            logging.exception("Error: opc function is not right!")
        else:
            for i in range(len(list_opc_name)):
                if len(list_opc[i]) > 2:
                    data_index = [int(index) for index in list_opc[i][2:]]
                    data_index_name = [database_index[index][0] for index in data_index]
                else:
                    data_index_name = []
                print(' '*13, end='')
                print(list_opc_name[i], end='')
                # print(' '.join(data_index_name))
                print(' ')
                print(' ' * 13, end='')
                print(' '.join(list_opc[i]))
            print(" ")

    def details_from_opcode(self, opcode):
        function_id_byte = opcode[0:2]
        [proto_type_bytes, proto_type_end] = self.parse_array_size(opcode, 2)
        return_type_byte = proto_type_bytes[0:1]
        list_para_type_bytes = proto_type_bytes[1:len(proto_type_bytes)]
        [list_opc, _] = self.parse_array_size(opcode, proto_type_end)
        [list_opc_bytes, _] = self.parse_arrays(list_opc)

        return [function_id_byte, return_type_byte, list_para_type_bytes, list_opc_bytes]

    def print_bytes_arrays(self, bytes_arrays):
        length = len(bytes_arrays)
        total_length = 0
        for i in range(length):
            info = self.convert_bytes_to_hex(bytes_arrays[i])
            print("{:02d}".format(i + 1) + " | " + ' '.join(info) + " | (" + str(len(info)) + " Bytes)")
            total_length += len(info)
        print("(sum of length for the above Bytes: " + str(total_length) + ")")

    @staticmethod
    def print_function_specification(nested_list):
        max_length = max([len(item) for items in nested_list for item in items])
        for items in nested_list:
            print(items[0] + " | ", end='')
            items.pop(0)
            for item in items:
                if items.index(item) != (len(items) - 1):
                    print(item + " "*(max_length - len(item) + 1), end='')
                else:
                    print(item + " "*(max_length - len(item) + 1))

    @staticmethod
    def convert_bytes_to_hex(bytes_object):
        return [bytes([byte]).hex() for byte in bytes_object]

    def parse_array_size(self, bytes_object, start_position):
        length_byte_array = self.convert_bytes_to_hex(bytes_object[start_position:(start_position + 2)])
        length = self.shorts_from_byte_array(length_byte_array)

        return [bytes_object[(start_position + 2):(start_position + 2 + length)], start_position + 2 + length]

    def parse_arrays(self, bytes_object):
        length_byte_array = self.convert_bytes_to_hex(bytes_object[0:2])
        length = self.shorts_from_byte_array(length_byte_array)
        all_info = []
        pos_drift = 2
        for pos in range(length):
            [array_info, pos_drift] = self.parse_array_size(bytes_object, pos_drift)
            all_info.append(array_info)
        return [all_info, pos_drift - 2 - 2*length]

    @staticmethod
    def shorts_from_byte_array(byte_array):
        if len(byte_array) != 2:
            logging.exception("Error: Input is not shorts!")
        return int(''.join(byte_array), 16)

    def texture_from_bytes(self, bytes_arrays):
        all_info = []
        if len(bytes_arrays) != 3:
            logging.exception("Error: texture is invalid!")
        specification_header = ['id', 'function_name', 'return_type', 'variables...']
        [initializer_bytes, _] = self.parse_arrays(bytes_arrays[0])
        initializer_spec = self.specification_from_bytes(initializer_bytes, 0)
        print("Initializer Function:")
        info = copy.deepcopy([specification_header] + initializer_spec)
        self.print_function_specification(info)
        info.pop(0)
        all_info.append(info)

        [descriptor_bytes, _] = self.parse_arrays(bytes_arrays[1])
        descriptor_spec = self.specification_from_bytes(descriptor_bytes, 1)
        print("Descriptor Functions:")
        info = copy.deepcopy([specification_header] + descriptor_spec)
        self.print_function_specification(info)
        info.pop(0)
        all_info.append(info)

        [state_var_bytes, _] = self.parse_arrays(bytes_arrays[2])
        state_var = self.specification_from_bytes(state_var_bytes, 2)
        specification_header = ['id', 'variable_name']
        print("State Variables:")
        info = copy.deepcopy([specification_header] + state_var)
        self.print_function_specification(info)
        info.pop(0)
        all_info.append(info)

        return all_info

    def specification_from_bytes(self, spec_bytes, spec_type):
        string_list = []
        function_count = 0
        if spec_type != 2:
            for info in spec_bytes:
                function_count += 1
                start_position = 0
                string_sublist = []
                [function_name_bytes, function_name_end] = self.parse_array_size(info, start_position)
                function_name = function_name_bytes.decode("utf-8")
                if function_name == 'init':
                    function_id = 0
                else:
                    function_id = function_count
                string_sublist.append("{:02d}".format(function_id))
                string_sublist.append(function_name)

                [return_name_bytes, return_name_end] = self.parse_array_size(info, function_name_end)
                return_name = return_name_bytes.decode("utf-8")
                string_sublist.append(return_name)

                [list_parameter_name_bytes, _] = self.parse_arrays(info[return_name_end:len(info)])
                for para in list_parameter_name_bytes:
                    para_name = para.decode("utf-8")
                    string_sublist.append(para_name)
                string_list.append(string_sublist)
        else:
            for info in spec_bytes:
                string_sublist = ["{:02d}".format(function_count)]
                para_name = info.decode("utf-8")
                string_sublist.append(para_name)
                string_list.append(string_sublist)
                function_count += 1
        return string_list

    # def deserilize_string(self, string_bytes):


    # def get_contract_info(self):
    #
    # def get_token_balance(self):
    #
    # def sign_register_contract(self):
    #
    # def sign_execute_contract(self):
    #
    # def contract_permitted(self, split = True):

    # def __str__(self):
    #     if not self.address:
    #         raise InvalidAddressException("No address")
    #     result = 'address = %s\npublicKey = %s\nprivateKey = %s\nseed = %s\nnonce = %d' % \
    #            (self.address, self.publicKey, self.privateKey, self.seed, self.nonce)
    #     if not is_offline():
    #         try:
    #             balance = self.balance()
    #             result += "\nbalance: {}".format(balance)
    #         except NetworkException:
    #             logging.error("Failed to get balance")
    #     return result
    #
    # __repr__ = __str__
    #
    # def balance(self, confirmations=0):
    #     if is_offline():
    #         pyvsystems.throw_error("Cannot check balance in offline mode.", NetworkException)
    #         return 0
    #     try:
    #         confirmations_str = '' if confirmations == 0 else '/%d' % confirmations
    #         resp = self.wrapper.request('/addresses/balance/%s%s' % (self.address, confirmations_str))
    #         logging.debug(resp)
    #         return resp['balance']
    #     except Exception as ex:
    #         msg = "Failed to get balance. ({})".format(ex)
    #         pyvsystems.throw_error(msg, NetworkException)
    #         return 0
    #
    # def balance_detail(self):
    #     try:
    #         resp = self.wrapper.request('/addresses/balance/details/%s' % self.address)
    #         logging.debug(resp)
    #         return resp
    #     except Exception as ex:
    #         msg = "Failed to get balance detail. ({})".format(ex)
    #         pyvsystems.throw_error(msg, NetworkException)
    #         return None
    #
    # def _generate(self, public_key='', private_key='', seed='', nonce=0):
    #     self.seed = seed
    #     self.nonce = nonce
    #     if not public_key and not private_key and not seed:
    #         wordCount = 2048
    #         words = []
    #         for i in range(5):
    #             r = bytes2str(os.urandom(4))
    #             x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
    #             w1 = x % wordCount
    #             w2 = ((int(x / wordCount) >> 0) + w1) % wordCount
    #             w3 = ((int((int(x / wordCount) >> 0) / wordCount) >> 0) + w2) % wordCount
    #             words.append(WORDS[w1])
    #             words.append(WORDS[w2])
    #             words.append(WORDS[w3])
    #         self.seed = ' '.join(words)
    #     if public_key:
    #         pubKey = base58.b58decode(public_key)
    #         privKey = ""
    #     else:
    #         seedHash = hashChain(str2bytes(str(nonce)+self.seed))
    #         accountSeedHash = sha256(seedHash)
    #         if not private_key:
    #             privKey = curve.generatePrivateKey(accountSeedHash)
    #         else:
    #             privKey = base58.b58decode(private_key)
    #         pubKey = curve.generatePublicKey(privKey)
    #     self.address = self.chain.public_key_to_address(pubKey)
    #     self.publicKey = bytes2str(base58.b58encode(pubKey))
    #     if privKey != "":
    #         self.privateKey = bytes2str(base58.b58encode(privKey))

    # def send_payment(self, recipient, amount, attachment='', tx_fee=DEFAULT_PAYMENT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
    #     if not self.privateKey:
    #         msg = 'Private key required'
    #         pyvsystems.throw_error(msg, MissingPrivateKeyException)
    #     if not self.chain.validate_address(recipient.address):
    #         msg = 'Invalid recipient address'
    #         pyvsystems.throw_error(msg, InvalidAddressException)
    #     elif amount <= 0:
    #         msg = 'Amount must be > 0'
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif tx_fee < DEFAULT_PAYMENT_FEE:
    #         msg = 'Transaction fee must be >= %d' % DEFAULT_PAYMENT_FEE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif len(attachment) > MAX_ATTACHMENT_SIZE:
    #         msg = 'Attachment length must be <= %d' % MAX_ATTACHMENT_SIZE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
    #         msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif not is_offline() and self.balance() < amount + tx_fee:
    #         msg = 'Insufficient VSYS balance'
    #         pyvsystems.throw_error(msg, InsufficientBalanceException)
    #     else:
    #         if timestamp == 0:
    #             timestamp = int(time.time() * 1000000000)
    #         sData = struct.pack(">B", PAYMENT_TX_TYPE) + \
    #                 struct.pack(">Q", timestamp) + \
    #                 struct.pack(">Q", amount) + \
    #                 struct.pack(">Q", tx_fee) + \
    #                 struct.pack(">H", fee_scale) + \
    #                 base58.b58decode(recipient.address) + \
    #                 struct.pack(">H", len(attachment)) + \
    #                 str2bytes(attachment)
    #         signature = bytes2str(sign(self.privateKey, sData))
    #         attachment_str = bytes2str(base58.b58encode(str2bytes(attachment)))
    #         data = json.dumps({
    #             "senderPublicKey": self.publicKey,
    #             "recipient": recipient.address,
    #             "amount": amount,
    #             "fee": tx_fee,
    #             "feeScale": fee_scale,
    #             "timestamp": timestamp,
    #             "attachment": attachment_str,
    #             "signature": signature
    #         })
    #
    #         return self.wrapper.request('/vsys/broadcast/payment', data)
    #
    # def contend(self, slot_id, tx_fee=DEFAULT_CONTEND_SLOT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
    #     if not self.privateKey:
    #         msg = 'Private key required'
    #         pyvsystems.throw_error(msg, MissingPrivateKeyException)
    #     elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
    #         msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif self.check_contend(slot_id, tx_fee):
    #         if timestamp == 0:
    #             timestamp = int(time.time() * 1000000000)
    #         sData = struct.pack(">B", CONTEND_SLOT_TX_TYPE) + \
    #                 struct.pack(">I", slot_id) + \
    #                 struct.pack(">Q", tx_fee) + \
    #                 struct.pack(">H", fee_scale) + \
    #                 struct.pack(">Q", timestamp)
    #         signature = bytes2str(sign(self.privateKey, sData))
    #         data = json.dumps({
    #             "senderPublicKey": self.publicKey,
    #             "fee": tx_fee,
    #             "feeScale": fee_scale,
    #             "slotId": slot_id,
    #             "timestamp": timestamp,
    #             "signature": signature
    #         })
    #         return self.wrapper.request('/spos/broadcast/contend', data)
    #
    # def check_contend(self, slot_id, tx_fee):
    #     if tx_fee < DEFAULT_CONTEND_SLOT_FEE:
    #         msg = 'Transaction fee must be >= %d' % DEFAULT_CONTEND_SLOT_FEE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #         return False
    #     if slot_id >= 60 or slot_id < 0:
    #         msg = 'Slot id must be in 0 to 59'
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #         return False
    #     if is_offline():  # if offline, skip other check
    #         return True
    #     balance_detail = self.get_info()
    #     min_effective_balance = MIN_CONTEND_SLOT_BALANCE + tx_fee
    #     if balance_detail["effective"] < min_effective_balance:
    #         msg = 'Insufficient VSYS balance. (The effective balance must be >= %d)' % min_effective_balance
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #         return False
    #     slot_info = self.chain.slot_info(slot_id)
    #     if not slot_info or slot_info.get("mintingAverageBalance") is None:
    #         msg = 'Failed to get slot minting average balance'
    #         pyvsystems.throw_error(msg, NetworkException)
    #         return False
    #     elif slot_info["mintingAverageBalance"] >= balance_detail["mintingAverage"]:
    #         msg = 'The minting average balance of slot %d is greater than or equals to yours. ' \
    #               'You will contend this slot failed.' % slot_id
    #         pyvsystems.throw_error(msg, InsufficientBalanceException)
    #         return False
    #     return True
    #
    # def release(self, slot_id, tx_fee=DEFAULT_RELEASE_SLOT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
    #     if not self.privateKey:
    #         msg = 'Private key required'
    #         pyvsystems.throw_error(msg, MissingPrivateKeyException)
    #     elif tx_fee < DEFAULT_RELEASE_SLOT_FEE:
    #         msg = 'Transaction fee must be >= %d' % DEFAULT_RELEASE_SLOT_FEE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif slot_id >= 60 or slot_id < 0:
    #         msg = 'Slot id must be in 0 to 59'
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
    #         msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif not is_offline() and self.balance() < tx_fee:
    #         msg = 'Insufficient VSYS balance'
    #         pyvsystems.throw_error(msg, InsufficientBalanceException)
    #     else:
    #         if timestamp == 0:
    #             timestamp = int(time.time() * 1000000000)
    #         sData = struct.pack(">B", RELEASE_SLOT_TX_TYPE) + \
    #                 struct.pack(">I", slot_id) + \
    #                 struct.pack(">Q", tx_fee) + \
    #                 struct.pack(">H", fee_scale) + \
    #                 struct.pack(">Q", timestamp)
    #         signature = bytes2str(sign(self.privateKey, sData))
    #         data = json.dumps({
    #             "senderPublicKey": self.publicKey,
    #             "fee": tx_fee,
    #             "feeScale": fee_scale,
    #             "slotId": slot_id,
    #             "timestamp": timestamp,
    #             "signature": signature
    #         })
    #         return self.wrapper.request('/spos/broadcast/release', data)
    #
    # def dbput(self, db_key, db_data, db_data_type="ByteArray", tx_fee=DEFAULT_DBPUT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
    #     if not self.privateKey:
    #         msg = 'Private key required'
    #         pyvsystems.throw_error(msg, MissingPrivateKeyException)
    #     elif tx_fee < DEFAULT_DBPUT_FEE:
    #         msg = 'Transaction fee must be >= %d' % DEFAULT_DBPUT_FEE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif len(db_key) > MAX_DB_KEY_SIZE or len(db_key) < MIN_DB_KEY_SIZE:
    #         msg = 'DB key length must be greater than %d and smaller than %d' % (MIN_DB_KEY_SIZE, MAX_ATTACHMENT_SIZE)
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
    #         msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
    #         pyvsystems.throw_error(msg, InvalidParameterException)
    #     elif not is_offline() and self.balance() < tx_fee:
    #         msg = 'Insufficient VSYS balance'
    #         pyvsystems.throw_error(msg, InsufficientBalanceException)
    #     else:
    #         if timestamp == 0:
    #             timestamp = int(time.time() * 1000000000)
    #         # "ByteArray" is the only supported type in first version
    #         if db_data_type == "ByteArray":
    #             data_type_id = b'\x01'
    #         # TODO: add more DB data type here
    #         else:
    #             msg = 'Unsupported data type: {}'.format(db_data_type)
    #             pyvsystems.throw_error(msg, InvalidParameterException)
    #             return
    #         sData = struct.pack(">B", DBPUT_TX_TYPE) + \
    #                 struct.pack(">H", len(db_key)) + \
    #                 str2bytes(db_key) + \
    #                 struct.pack(">H", len(db_data)+1) + \
    #                 data_type_id + \
    #                 str2bytes(db_data) + \
    #                 struct.pack(">Q", tx_fee) + \
    #                 struct.pack(">H", fee_scale) + \
    #                 struct.pack(">Q", timestamp)
    #         signature = bytes2str(sign(self.privateKey, sData))
    #         data = json.dumps({
    #               "senderPublicKey": self.publicKey,
    #               "dbKey": db_key,
    #               "dataType": db_data_type,
    #               "data": db_data,
    #               "fee": tx_fee,
    #               "feeScale": fee_scale,
    #               "timestamp": timestamp,
    #               "signature": signature
    #         })
    #
    #         return self.wrapper.request('/database/broadcast/put', data)
    #
    # def get_info(self):
    #     if not (self.address and self.publicKey):
    #         msg = 'Address required'
    #         pyvsystems.throw_error(msg, MissingAddressException)
    #         return None
    #     if not self.publicKey:
    #         msg = 'Public key and address required'
    #         pyvsystems.throw_error(msg, MissingPublicKeyException)
    #         return None
    #     if is_offline():
    #         info = {
    #             "publicKey": self.publicKey,
    #             "address": self.address
    #         }
    #         return info
    #     info = self.balance_detail()
    #     if not info:
    #         msg = 'Failed to get balance detail'
    #         pyvsystems.throw_error(msg, NetworkException)
    #     else:
    #         info["publicKey"] = self.publicKey
    #         return info