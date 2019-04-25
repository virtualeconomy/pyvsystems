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
from .opcode import *

class Contract(object):
    def __init__(self):
        self.language_code_byte_length = 4
        self.language_version_byte_length = 4
        self.data_type_list = {'01': 'PublicKey', '02': 'Address', '03': 'Amount', '04': 'Int32', '05': 'ShortText',
                               '06': 'ContractAccount', '07': 'Account'}
        # self.test = 'JC9U69xcoTWJ71v82TojKETj3SAsxyh3nYACiheZMDBgE6XKshzgupsRmSk3y1aijZJxWu4DSX96nMpStH2ESv3P4VC4MogHcN8UcCiaLiCt2af1b7zkhZtGq6ckrvHjijJ7ZHZugp8bzyUTs55SnZ5o2tockgM8jhtnfVNRPEPq8My9QNDDyZRJyxyJnE6p8kB3PDEPk1WsBxe68APAaLqjN4ACRCv5kyhKTjaEixRz6yn62W8PRi5PpzD4KEtg1DrxwhwqsFWCLrNPsw8vTuSB3DrNgCq72FEQJAAtdDS29kPmaQYeQG2YQzUrtKyteAdMzQw2B17wUsQj4tnkFkec5VbbV4mFZ5zhVsCv5UErZiKKPiBgefjQjfnuYNV6PA4r5T6XrtW2zi5MvzEym3vt3PpzodHd9xY5UftGRmkWjZ1atRfRsheDw6CKcsjdEGNS5J7bfvLj3KAckRPjp1wAP5CTKASSLvGVBCyieNyJLmdfguhEEg5xpKXiJdzTAnQDrBYdhCpRq9xTcBK5ueQZ5vqEZt1vbBBLVzkdmmt54tZXvpvW3TPwKqLtz26zdtAPntmjLyqqNKbmzb8MrgiyjyC8YmYgnLUkeU8q2ksmZKZ8aoHEW5zF3ztQ7qNvaxY86NY3AHkpcuUjbdaMxEMKAQ3Qc2fVcwHVoJoEz7pSSUHvnUcZcnYMMmGR52gwNasUxVAm2LmbNbuyQvnxpJXd2yQryWQjgHcgDoRSroRuV6rftvGz6d9FbhytyrUEc9Ae6uZu7W6cAtB75jBtaBUk9K9cootsqEu2Y1PUE7B832X3j4UWveC73XnkRsz5U8EStNWvJXYZ2QitmZBSpCYMP8bnEfnqtxmGk7B1iT3tqWaJ5QX5DgkQ189UXimGCjAs31LtFSCuGWzkJnoR3H5Yno465v7WHLkbewKqrDpaAbgj82pja8uuSj8uZGBrEDXu2KdP4R4UbfDUXYmGtiNTwDDfwdyAv4BrvyQFuWKVWnMDhkSjsjSVJmLx5qwNq3EBZzN7tZd9UBQ3552rSfu48Y7fvTh54x9FjYMDCmtUFmsxrnWFgbGe8Gypfwpk9qKHe4Pe7Qjx5ppzAW48FDtdtjznh6wk4wF33y46cfrTEogULvkifb8WjqoXaRytdxUzcm6M23XiKUfQAVygFJXBJfCU3VbxFZgLib2Lgp2dAeB5myJzRayKi9tJQVzLrYr4NEFWpzJbxiZxyY14XyHXWTyvGgQHW5DGkgRiWDm7mbybtb9BvKrEtkKCZ'
        self.test = 'kpUFTV4BMU2mLarm7iTmJMxw7RLSx2SBZvA22e26pEAp9CfxxppnPCaM4YMZYptdewVirdTdLPboQs9bn18VgeSSz3zRXSN8xAmgUs3JVr4v6Xw2YKHP8zKbngErdvr3YKZCu8hjjZv1MfRbPyWbaDCoXo4q3ngJrZ2hmDok1PxxaN8dwXT4M4PkfnQyaCqVhbNpwmYaSQoHVMfLAMnJXBtxfbrfTj6M8Gg6gjmnHcvXJy59oZtWhqK6H83fYuK8cydNj7cZWn43L5S9pZEjHFZZA37pxbdiwKRvbFNkocNuU9kpVySTPyLLUd5pSYMtUfNkMhQwkDASLrzdyfbQ8G9WxKNucbSbDzoA1F5tTP1a7LzeQZ14ABbztaJKaqStxXhX2hBEmxHGwdhiwNM2UbVLgjiomzw1s1EupH7zseoBpTPKZRsVso8j3SoSsfGpwf2YeCAds47SQqVsjGFMsp3WHeuRQd2U5DV2AQyYshHoTkad3akT7QYcrZ39ypMPj2KGizg2wdJSw3Z6LknyyKviu12vkpaMxsR74jGUAA54PkNRNEYyP62BWM35eDDkxS62tcRP5R1Xp9acsgJq2J9uqrrEseeTC8icMJUQY4E7bpQwdwgsnzeLHnfADEoaNBh45DEdB4mRoGCWoqiZeX341VDmBjQW44uTjXvQ46zHiR34g2KzDJ178cbmTaYzcBZHsqu8MZFDimsGALk81C1U5wKCN63x3FqcNS436M3f23op7hUm8Rf4FDsCvCu5NaytUvFKMmLfBtg6D3MqBVEzV6nuhSPHsnU5JiiAfUx93ZivtjmDAYGCcANrTzdDB1PeKj9BbE2SoyJ9TxkAXgUBZoZneZJnuqLAoEookS9zT7LKxyU4T7DwWVWDuX9j2XYB8Pi2DDYkydfbssics6XJjDkeG8cMPKi3p3jeZN8Qaf7KraE4SHZEatvCZb5fJdSPaDWQiJ6XhUpNCGYqb8htPou9bPqQL6hTj6yX44WSedMqw2bArrXAwh4MXvgxGJBt89CXG6qGm4wHYM6bjpQ8bNuQvUDNQ5HueHLSTJNtiCHTDgfH7MvmVm1xfJF7dFeKmeRwbFiRK7E3dBKr6wANmkUzM7ezdFMsPDr8PQkbipHJAM6j1uDujNci9TcQYgpviUg6uaUvqPKsZa3q3Hw4NsCxDNRGKFtwPUyTFXJAEeAqoiFmUQDfjeTFCFpHr4DfuqHdpwwVQebsEKUdcnQdoEgP1Dmav2JKbffTcL8wJgtGjoVpUzMb55DBe31uqf7Ri2UZFbAq3APw9yqCbLM1jNN9dBizQ48fdmgHxhHGAM1kiDdtFVJwPt974GPGQ7cnbTqdePbHFcEkkxXmrVjymmf'

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
        self.opcode_info = Opcode()

    def show_contract_function(self, byte_string = '', contract_json = ''):
        byte_string = self.test
        bytes_object = base58.b58decode(byte_string)
        # print("all: ", bytes_object)
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

        print(bytes_object[state_var_end:len(bytes_object)], len(bytes_object[state_var_end:len(bytes_object)]))
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
                self.print_a_function(function_id, functions_spec[i], list_para_type, list_opc, all_info[2])

    def print_a_function(self, function_id, functions_spec, list_para_type, list_opc, all_state_var):
        function_name = functions_spec[0]
        return_type = functions_spec[1]
        if len(functions_spec) > 2:
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
        list_opc_name = [self.opcode_info.function_name[opc[0] + opc[1]]
                         if len(opc) >= 2 else logging.exception("Error: opc function is not right!")
                         for opc in list_opc]
        if len(list_opc_name) != len(list_opc):
            logging.exception("Error: opc function is not right!")
        else:
            name_list = copy.deepcopy(list_para)
            for i in range(len(list_opc_name)):
                data = copy.deepcopy([int(index) for index in list_opc[i]])
                print(' ' * 13, end='')
                name_list = self.opcode_info.get_opc(list_opc_name[i], [data, name_list, all_state_var])
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
            for item in items[1:]:
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
        [item.pop(0) for item in info]
        all_info.append(info)

        [descriptor_bytes, _] = self.parse_arrays(bytes_arrays[1])
        descriptor_spec = self.specification_from_bytes(descriptor_bytes, 1)
        print("Descriptor Functions:")
        info = copy.deepcopy([specification_header] + descriptor_spec)
        self.print_function_specification(info)
        info.pop(0)
        [item.pop(0) for item in info]
        all_info.append(info)

        [state_var_bytes, _] = self.parse_arrays(bytes_arrays[2])
        state_var = self.specification_from_bytes(state_var_bytes, 2)
        specification_header = ['id', 'variable_name']
        print("State Variables:")
        info = copy.deepcopy([specification_header] + state_var)
        self.print_function_specification(info)
        info.pop(0)
        [item.pop(0) for item in info]
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

    def get_contract_info(self, wrapper, contract_id):
        try:
            resp = wrapper.request('/info/%s' % (contract_id))
            logging.debug(resp)
            return resp['info']
        except Exception as ex:
            msg = "Failed to get contract info. ({})".format(ex)
            pyvsystems.throw_error(msg, NetworkException)
            return 0

    def get_contract_content(self, wrapper, contract_id):
        try:
            resp = wrapper.request('/content/%s' % (contract_id))
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

    # def get_contract_info(self):
    #
    # def get_token_balance(self):
    #
    # def sign_register_contract(self, privatekey):
    #     a = 1
    #
    # def sign_execute_contract(self):

    def contract_permitted(self, split = True):
        a = 1
