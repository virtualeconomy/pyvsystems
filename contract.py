#from .setting import *
from .crypto import *
from .error import *
import pyvsystems
import time
import struct
import json
import base58
import logging
import copy
from .opcode import *
from .deser import *


class Contract(object):
    def __init__(self):
        self.language_code_byte_length = 4
        self.language_version_byte_length = 4
        self.data_type_list = {'01': 'PublicKey', '02': 'Address', '03': 'Amount', '04': 'Int32', '05': 'ShortText',
                               '06': 'ContractAccount', '07': 'Account'}
        # self.test = 'JC9U69xcoTWJ71v82TojKETj3SAsxyh3nYACiheZMDBgE6XKshzgupsRmSk3y1aijZJxWu4DSX96nMpStH2ESv3P4VC4MogHcN8UcCiaLiCt2af1b7zkhZtGq6ckrvHjijJ7ZHZugp8bzyUTs55SnZ5o2tockgM8jhtnfVNRPEPq8My9QNDDyZRJyxyJnE6p8kB3PDEPk1WsBxe68APAaLqjN4ACRCv5kyhKTjaEixRz6yn62W8PRi5PpzD4KEtg1DrxwhwqsFWCLrNPsw8vTuSB3DrNgCq72FEQJAAtdDS29kPmaQYeQG2YQzUrtKyteAdMzQw2B17wUsQj4tnkFkec5VbbV4mFZ5zhVsCv5UErZiKKPiBgefjQjfnuYNV6PA4r5T6XrtW2zi5MvzEym3vt3PpzodHd9xY5UftGRmkWjZ1atRfRsheDw6CKcsjdEGNS5J7bfvLj3KAckRPjp1wAP5CTKASSLvGVBCyieNyJLmdfguhEEg5xpKXiJdzTAnQDrBYdhCpRq9xTcBK5ueQZ5vqEZt1vbBBLVzkdmmt54tZXvpvW3TPwKqLtz26zdtAPntmjLyqqNKbmzb8MrgiyjyC8YmYgnLUkeU8q2ksmZKZ8aoHEW5zF3ztQ7qNvaxY86NY3AHkpcuUjbdaMxEMKAQ3Qc2fVcwHVoJoEz7pSSUHvnUcZcnYMMmGR52gwNasUxVAm2LmbNbuyQvnxpJXd2yQryWQjgHcgDoRSroRuV6rftvGz6d9FbhytyrUEc9Ae6uZu7W6cAtB75jBtaBUk9K9cootsqEu2Y1PUE7B832X3j4UWveC73XnkRsz5U8EStNWvJXYZ2QitmZBSpCYMP8bnEfnqtxmGk7B1iT3tqWaJ5QX5DgkQ189UXimGCjAs31LtFSCuGWzkJnoR3H5Yno465v7WHLkbewKqrDpaAbgj82pja8uuSj8uZGBrEDXu2KdP4R4UbfDUXYmGtiNTwDDfwdyAv4BrvyQFuWKVWnMDhkSjsjSVJmLx5qwNq3EBZzN7tZd9UBQ3552rSfu48Y7fvTh54x9FjYMDCmtUFmsxrnWFgbGe8Gypfwpk9qKHe4Pe7Qjx5ppzAW48FDtdtjznh6wk4wF33y46cfrTEogULvkifb8WjqoXaRytdxUzcm6M23XiKUfQAVygFJXBJfCU3VbxFZgLib2Lgp2dAeB5myJzRayKi9tJQVzLrYr4NEFWpzJbxiZxyY14XyHXWTyvGgQHW5DGkgRiWDm7mbybtb9BvKrEtkKCZ'
        #self.test = 'kpUFTV4BMU2mLarm7iTmJMxw7RLSx2SBZvA22e26pEAp9CfxxppnPCaM4YMZYptdewVirdTdLPboQs9bn18VgeSSz3zRXSN8xAmgUs3JVr4v6Xw2YKHP8zKbngErdvr3YKZCu8hjjZv1MfRbPyWbaDCoXo4q3ngJrZ2hmDok1PxxaN8dwXT4M4PkfnQyaCqVhbNpwmYaSQoHVMfLAMnJXBtxfbrfTj6M8Gg6gjmnHcvXJy59oZtWhqK6H83fYuK8cydNj7cZWn43L5S9pZEjHFZZA37pxbdiwKRvbFNkocNuU9kpVySTPyLLUd5pSYMtUfNkMhQwkDASLrzdyfbQ8G9WxKNucbSbDzoA1F5tTP1a7LzeQZ14ABbztaJKaqStxXhX2hBEmxHGwdhiwNM2UbVLgjiomzw1s1EupH7zseoBpTPKZRsVso8j3SoSsfGpwf2YeCAds47SQqVsjGFMsp3WHeuRQd2U5DV2AQyYshHoTkad3akT7QYcrZ39ypMPj2KGizg2wdJSw3Z6LknyyKviu12vkpaMxsR74jGUAA54PkNRNEYyP62BWM35eDDkxS62tcRP5R1Xp9acsgJq2J9uqrrEseeTC8icMJUQY4E7bpQwdwgsnzeLHnfADEoaNBh45DEdB4mRoGCWoqiZeX341VDmBjQW44uTjXvQ46zHiR34g2KzDJ178cbmTaYzcBZHsqu8MZFDimsGALk81C1U5wKCN63x3FqcNS436M3f23op7hUm8Rf4FDsCvCu5NaytUvFKMmLfBtg6D3MqBVEzV6nuhSPHsnU5JiiAfUx93ZivtjmDAYGCcANrTzdDB1PeKj9BbE2SoyJ9TxkAXgUBZoZneZJnuqLAoEookS9zT7LKxyU4T7DwWVWDuX9j2XYB8Pi2DDYkydfbssics6XJjDkeG8cMPKi3p3jeZN8Qaf7KraE4SHZEatvCZb5fJdSPaDWQiJ6XhUpNCGYqb8htPou9bPqQL6hTj6yX44WSedMqw2bArrXAwh4MXvgxGJBt89CXG6qGm4wHYM6bjpQ8bNuQvUDNQ5HueHLSTJNtiCHTDgfH7MvmVm1xfJF7dFeKmeRwbFiRK7E3dBKr6wANmkUzM7ezdFMsPDr8PQkbipHJAM6j1uDujNci9TcQYgpviUg6uaUvqPKsZa3q3Hw4NsCxDNRGKFtwPUyTFXJAEeAqoiFmUQDfjeTFCFpHr4DfuqHdpwwVQebsEKUdcnQdoEgP1Dmav2JKbffTcL8wJgtGjoVpUzMb55DBe31uqf7Ri2UZFbAq3APw9yqCbLM1jNN9dBizQ48fdmgHxhHGAM1kiDdtFVJwPt974GPGQ7cnbTqdePbHFcEkkxXmrVjymmf'

        #self.test = '3cH33Y6c6AM23HqLCBhtyUnFbkUsVKM8qwqSMZvgxWfU3RKmdMUNQBtupFFznBb75PX5gKBNE5mRxLJrP353QQ8RUuwu7X4jLbb7YpxqSHEhLdcwkg1gGcD3iLxaQA79ycGVaipnYSNjcSc6vdsLYhH8eCY4f7cJk4jVtnA686aw8CnrpwK1bGi5pLBz2bVDYhFeuAbHZpEsvx7mAAdY7xQu7LyHaRoHhSdeZc7AbbF6ZcGY3DTFi6Me2KkG8rJb22pAv3Cg6cDcQw2eiFLivZJHzsdAwqZKCvUuprs2va2J16RckD27o1wpwQtUHBFkG7jszMo7A47RGcSseQPSKWTCtMQc9y98A9zKg2mzRyo2rMqLL3AXbFjgPAXPuhvFvKPrWUcpgde2DeLiXfSYD2nguHLGKsYdSHtaDjzmbnzo1xBibjzHUEKmnkEoMZWZYJXzoA4yvx9FNreGv8DzqEQFwyxppvvYz39umJmwt6kh2D1XEu88EvnEtm45pdXmt8caua72ABLAP9QCgcbQzjf5SVUKPoeg4PrQg3CsfNsZNEs8zpngHfVgVk7opckJUNEESAGXpBFy4JX6wptq5RhqGT8TEbk5JVYtw2xfDuFpNy7p3FT1nN2jWB3K3ZeTR6xvEW3caaPsgRf7PSb2MLsLjC1tZhccD1ZQttQEcRJCaprEkvbmeaQgLEsTibeg31wGUktMy6pM3AY7ggYcW4eK8bNfFzdubCSTnw8pYoscbTb2f5rAvRzMvr3xaSpaY2SnUGZJNixNFuPZtyYw4N5JMykfUmXLep6wm8vXX3pb9LN4A6y3DUE2Gq8an7XzGvjmRd5b7kNeoKDpTTJ4Mea6zfEopL7Gfwgfq77pwiQq9PHdRXEC8vr1ec67c6Bue1T67aWDMcNM3XUSZ69nti6Q9ZnSAFbJPAjBvH2RMQpe235vDWDt4Ppj9DFmXjYy64UbhBEbLK9kDHbe6WsGZujf6xwmG4k3zBTsqQyoKaj6zDyUDxSU3rU3C3tcuYifFXqRxUHotn4ftRQFH2Xmv1emDbs7MxWRcWrShXg4Qvkmnk9fCZXYFXS6x7SGDCCCP79RhxCgZaKww3WctCtx2Q5gYFkmwUkWxtovm1RspDczxPADxdW85bUuMKPactPSHKJRsCFE8eM7a6J77y5FGK8ZpHFKzuYKp1cMzXnvqzQRd2qZ5jcxhF8T5HADVLXR3UMUkptcx44hS9KS3z4VjvWMTtsejNQvn79MAfrtj7UU9kYNbV32YmEQorTcJV4BCYTkh9NjN7zcFzqMZqR9XXxiY3zYUiPiVcgSrg1VBGJqgLYHGd6sGVLBRj6CVY9xGCnufU7fWQjbXBfwjd4ERFAzLhdP4boVeYu5qP5mQ4ZZ6CwwkDszXQSPUkvb9rBJV6vZQi4hryV3Wh1hDK25Qf3gy6gVWSckgb3oxPhoiuFX6LZ'
        self.test = '3dPGAWbTw4srh5hmMiRUhHtcxmXXLUooKGAfnmz11j5NruyJpBzZpgvADMdZS7Mevy5MAHqFbfHYdfqaAe1JEpLWt1pJWLHZBV62zUhLGmVLXUP5UDvSs24jsBRHqZMC71ciE1uYtgydKxCoFJ3rAgsYqp7GDeTU2PXS5ygDmL6WXmbAYPS8jE4sfNUbJVwpvL1cTw4nnjnJvmLET8VmQybxFt415RemV3MFPeYZay5i5gMmyZa63bjzK1uMZAVWA9TpF5YQ1NTZjPaRPvQGYVY4kY9L4LFJvUG2bib1QaNh7wUAQnTzJfRYJoy1aegFGFZFnBGp9GugH4fHAY69vGmZQnhDw3jU45G9odFyXo3T5Ww4R5szegbjCUKdUGpXf9vY2cKEMJ7i8eCkFVG1dDFZeVov1KMjkVNV8rDBDYfcp3oSGNWQQvGSUT5iGUvDRN8phy1UpR3A9uMVebvjLnVzPx9RyqQ8HaXLM8vPhLuWLoh5hk1Zi1n9nwz55XvKDYjP6eeB55yK5vpg8xjaYDnw9bjYV7ZmS7LAsHvXfnwi8y2W6vk2hGvs4rtR1vNRZSQMPGRRSuwCRJL1yngH6uHWwm2ajWxc684jApuoLdyjZomfCtdpabSyU3kp9Lrn8zT8BVY332sJPQU6gTQi8ke9s9dBxCae4cfSQM6HhuBmFc5KKWHCVG4bm4KZRYbMtidw8ZZnjaAMtcGq7k3Se6GXaTxdS3GcuttB3VB7njypyzuqAcfCdYb9ht8Y1WuTCZ1aLsXsL6eydfk2WLJVrqYpbTk6AchV5gMAEopvc3qXvzrDCedjtNsDmA56Lh6PxrrKr8aV8Wzz8aMaQ88YsVBpE8J4cDkxzo31AojhzEGVBKLmpb3bjmsaw9VkpB6yL8ngYs8eJMSPdM289TSMaEmG4eHt1jezpHTKxkuB9cwqcvhGNLWuv8KXQkik5pRMXV67Qs2FvjpzeJ81z2hnVh1wCtsa6M6qAG1gsqLHa1AVMRzsowafC99uDexwWMBS2RqsZWZBXJcUiNVULjApSnoBREYfHYEpjJ152hnTYZCAwpZMWEkVdBQpZ3zk8gbfLxB4fWMfKgJJucbKPGp1K56u7P8MHQu9aNb9dEof2mwX8rTHjk8jSQ7kXVX4Mf1JqMRWWftkV3GmU1nqYhxRGu4FjDNAomwTr5epHpcMF6P5oiXcLWh5BFQVmGYKz129oizAyUJBsZdxr2WZEGDieLxUg8cve25g28oTuCVENST4z1ZsFAN9wTa1'
        # self.assert_opc = {'01': 'GteqZeroAssert', '02': 'LteqAssert', '03': 'LtInt64Assert', '04': 'GtZeroAssert',
        #                    '05': 'EqAssert', '06': 'IsCallerOriginAssert', '07': 'IsSignerOriginAssert'}
        # self.load_opc = {'01': 'SignerLoad', '02': 'CallerLoad'}
        # self.cdbv_opc = {'01': 'SetCDBV'}
        # self.cdbvr_opc = {'01': 'GetCDBVR'}
        # self.tdb_opc = {'01': 'NewTokenTDB', '02': 'SplitTDB'}
        # self.tdbr_opc = {'01': 'GetTDBR', '02': 'TotalTDBR'}
        # self.tdba_opc = {'01': 'DepositTDBA', '02': 'WithdrawTDBA', '03': 'TransferTDBA'}
        # self.tdbar_opc = {'01': 'BalanceTBDAR'}
        # self.opc_type = {'01': ['AssertOpc', self.assert_opc], '02': ['LoadOpc', self.load_opc], '03': ['CDBVOpc', self.cdbv_opc],
        #                  '04': ['CDBVROpc', self.cdbvr_opc], '05': ['TDBOpc', self.tdb_opc], '06': ['TDBROpc', self.tdbr_opc],
        #                  '07': ['TDBAOpc', self.tdba_opc], '08': ['TDBAROpc', self.tdbar_opc], '09': ['ReturnOpc', {}]}
        self.function_type_map = {'000': 'onInit', '100': 'public'}
        self.opcode_info = Opcode()

    def show_contract_function(self, byte_string = '', contract_json = ''):
        byte_string = self.test
        bytes_object = base58.b58decode(byte_string)
        # print("All Bytes: ")
        # print(bytes_object)
        start_position = 0
        print("Total Length of Contract: ", str(len(bytes_object)) + ' Bytes')

        language_code = bytes_object[start_position:self.language_code_byte_length]
        bytes_to_hex = convert_bytes_to_hex(language_code)
        print("Language Code: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print(' '.join(bytes_to_hex))

        language_version = bytes_object[self.language_code_byte_length:(self.language_code_byte_length
                                                                        + self.language_version_byte_length)]
        bytes_to_hex = convert_bytes_to_hex(language_version)
        print("Language Version: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print(' '.join(bytes_to_hex))

        [trigger_with_header, trigger_end] = parse_array_size(bytes_object, self.language_code_byte_length
                                                          + self.language_version_byte_length)
        [trigger, _] = parse_arrays(trigger_with_header)
        bytes_to_hex = convert_bytes_to_hex(trigger[0])
        print("Trigger: " + "(" + str(len(bytes_to_hex)) + " Bytes)")
        print("id" + " | byte")
        print("00 | " + ' '.join(bytes_to_hex))

        [descriptor_arrays, descriptor_end] = parse_array_size(bytes_object, trigger_end)
        [descriptor, bytes_length] = parse_arrays(descriptor_arrays)
        print("Descriptor: " + "(" + str(bytes_length) + " Bytes)")
        print("id" + " | byte")
        self.print_bytes_arrays(descriptor)

        [state_var_arrays, state_var_end] = parse_array_size(bytes_object, descriptor_end)
        [state_var, bytes_length] = parse_arrays(state_var_arrays)
        print("State Variable: " + "(" + str(bytes_length) + " Bytes)")
        print("id" + " | byte")
        self.print_bytes_arrays(state_var)

        [texture, _] = parse_arrays(bytes_object[state_var_end:len(bytes_object)])
        all_info = self.print_texture_from_bytes(texture)

        functions_bytes = copy.deepcopy(trigger + descriptor)
        print("All Functions with Opcode:")
        self.print_functions(functions_bytes, all_info)

    def print_functions(self, functions_opcode, all_info):
        trigger = all_info[0][0]
        execute_fun = all_info[1][0]
        if len(functions_opcode) != (len(trigger) + len(execute_fun)):
            msg = 'Functions are not well defined in opc and texture!'
            pyvsystems.throw_error(msg, InvalidParameterException)
        else:
            functions_spec = copy.deepcopy([trigger[0]] + execute_fun)
            for i in range(len(functions_opcode)):
                [function_id_byte, function_type_byte, return_type_bytes, list_para_type_bytes, list_opc_bytes] = \
                    self.details_from_opcode(functions_opcode[i])
                function_hex = convert_bytes_to_hex(function_id_byte)
                if i == 0:
                    prefix = "0"
                else:
                    prefix = "1"
                function_type_key = prefix + "{:02d}".format(int(function_type_byte.hex(), 16))
                function_type = self.function_type_map[function_type_key]
                function_hex.append(function_type_byte.hex())
                if len(list_para_type_bytes) > 0:
                    list_para_type = [self.data_type_list[para]
                                      for para in convert_bytes_to_hex(list_para_type_bytes)]
                    function_hex.append([para for para in convert_bytes_to_hex(list_para_type_bytes)])
                else:
                    list_para_type = []
                    function_hex.append([])
                list_opc = [convert_bytes_to_hex(list_opc_line) for list_opc_line in list_opc_bytes]

                if len(return_type_bytes) > 0:
                    function_hex.append([para for para in convert_bytes_to_hex(return_type_bytes)])
                else:
                    function_hex.append([])
                self.print_a_function(function_type, function_hex, functions_spec[i], list_para_type, list_opc, all_info[2])

    def print_a_function(self, function_type, function_hex, functions_spec, list_para_type, list_opc, all_state_var):
        return_type = functions_spec[1]
        function_name = functions_spec[2]
        para_name = functions_spec[3]
        state_var = all_state_var[0]
        if len(list_para_type) >= 1:
            list_para = para_name[:len(list_para_type)]
        else:
            list_para = []
        if len(list_para_type) != len(list_para):
            logging.exception("Error: list of parameter is not right!")
        else:
            if function_type == 'OnInit':
                prefix = "trigger"
                if shorts_from_byte_array(function_hex[0:2]) == 0:
                    print("Triggers: ")
            else:
                prefix = "function"
                if shorts_from_byte_array(function_hex[0:2]) == 0:
                    print("Descriptor Functions: ")
            print(function_type + ' ' + prefix + ' ' + function_name + "(", end='')
            if len(list_para_type) > 0:
                for i in range(len(list_para_type)):
                    print(list_para_type[i] + ' ', end='')
                    if i == (len(list_para_type) - 1):
                        print(list_para[i] + ') ', end='')
                    else:
                        print(list_para[i] + ', ', end='')
            else:
                print(') ', end='')

        if function_hex[4]:
            for i in range(len(return_type)):
                print('return ' + self.data_type_list[function_hex[4][i]] + ' ' + return_type[0])
        else:
            print(' ')

        print("| " + ' '.join(function_hex[0:2]) + " | " + function_hex[2] + " ", end='')
        if function_hex[3]:
            print("| " + ' '.join(function_hex[3]) + " ", end='')
        else:
            print("| - ", end='')
        if function_hex[4]:
            print("| " + ' '.join(function_hex[4]) + " ", end='')
        else:
            print("| - ", end='')
        print("| ")
        list_opc_name = [self.opcode_info.function_name[opc[0] + opc[1]]
                         if len(opc) >= 2 else logging.exception("Error: opc function is not right!")
                         for opc in list_opc]
        if len(list_opc_name) != len(list_opc):
            logging.exception("Error: opc function is not right!")
        else:
            name_list = copy.deepcopy(para_name)
            for i in range(len(list_opc_name)):
                data = copy.deepcopy([int(index) for index in list_opc[i]])
                print(' ' * 13, end='')
                self.opcode_info.get_opc(list_opc_name[i], [data, name_list, state_var])
                print(' ' * 13, end='')
                print('| ' + list_opc[i][0] + ' ' + list_opc[i][1] + ' | ' + ' '.join(list_opc[i][2:]) + ' |')
            print(" ")

    def print_texture_from_bytes(self, bytes_arrays):
        all_info = []
        if len(bytes_arrays) != 3:
            msg = 'Texture is invalid!'
            pyvsystems.throw_error(msg, InvalidParameterException)
        [initializer_bytes, _] = parse_arrays(bytes_arrays[0])
        initializer_spec = self.specification_from_bytes(initializer_bytes, 0)
        print("Initializer Function:")
        specification_header = ['id', 'return_type', 'function_name', 'variables...']
        info = copy.deepcopy([specification_header, initializer_spec])
        self.print_function_specification(info)
        info.pop(0)
        [item.pop(0) for item in info]
        all_info.append(info)

        [descriptor_bytes, _] = parse_arrays(bytes_arrays[1])
        descriptor_spec = self.specification_from_bytes(descriptor_bytes, 1)
        print("Descriptor Functions:")
        info = copy.deepcopy([specification_header, descriptor_spec])
        self.print_function_specification(info)
        info.pop(0)
        [item.pop(0) for item in info]
        all_info.append(info)

        [state_var_bytes, _] = parse_arrays(bytes_arrays[2])
        state_var = self.specification_from_bytes(state_var_bytes, 2)
        specification_header = ['id', 'variable_name']
        print("State Variables:")
        info = copy.deepcopy([specification_header, state_var])
        self.print_state_var_specification(info)
        info.pop(0)
        [item.pop(0) for item in info]
        all_info.append(info)
        return all_info

    @staticmethod
    def details_from_opcode(opcode):
        function_id_two_bytes = opcode[0:2]
        function_type_byte = opcode[2:3]
        [return_type_bytes, return_type_end] = parse_array_size(opcode, 3)
        [list_para_type_bytes, list_para_type_end] = parse_array_size(opcode, return_type_end)
        [list_opc, _] = parse_array_size(opcode, list_para_type_end)
        [list_opc_bytes, _] = parse_arrays(list_opc)

        return [function_id_two_bytes, function_type_byte, return_type_bytes, list_para_type_bytes, list_opc_bytes]

    @staticmethod
    def print_bytes_arrays(bytes_arrays):
        length = len(bytes_arrays)
        total_length = 0
        for i in range(length):
            info = convert_bytes_to_hex(bytes_arrays[i])
            print("{:02d}".format(i) + " | " + ' '.join(info) + " | (" + str(len(info)) + " Bytes)")
            total_length += len(info)
        print("(sum of length for the above Bytes: " + str(total_length) + ")")

    @staticmethod
    def print_function_specification(nested_list):
        header = nested_list[0]
        all_info = nested_list[1]
        max_length = max(all_info[0]*len(item[1]) for item in all_info[1:])
        for item in header:
            if max_length < len(item):
                max_length = len(item)

        print(header[0] + " | ", end='')
        for item in header[1:]:
            if header.index(item) != (len(header) - 1):
                print(item + " " * (max_length - len(item) + 1), end='')
            else:
                print(item + " " * (max_length - len(item) + 1))

        for items in all_info[1:]:
            if len(items) != 4:
                msg = 'Texture in function is invalid!'
                pyvsystems.throw_error(msg, InvalidParameterException)
            function_id = items[0]
            return_type = items[1]
            function_name = items[2]
            para_list = items[3]
            print(function_id + " | ", end='')
            for return_name in return_type:
                print(return_name + " " * (max_length - len(return_name) + 1), end='')
            print(function_name + " " * (max_length - len(function_name) + 1), end='')
            for item in para_list:
                if para_list.index(item) != (len(para_list) - 1):
                    print(item + " " * (max_length - len(item) + 1), end='')
                else:
                    print(item + " " * (max_length - len(item) + 1))

    @staticmethod
    def print_state_var_specification(nested_list):
        header = nested_list[0]
        all_info = nested_list[1]
        max_length = all_info[0]
        for item in header:
            if max_length < len(item):
                max_length = len(item)
        print(header[0] + " | ", end='')
        for item in header[1:]:
            if header.index(item) != (len(header) - 1):
                print(item + " " * (max_length - len(item) + 1), end='')
            else:
                print(item + " " * (max_length - len(item) + 1))
        for item in all_info[1:]:
            print(item[0] + " | " + item[1])

    @staticmethod
    def specification_from_bytes(spec_bytes, spec_type):
        string_list = []
        function_count = 0
        max_length_string = 2
        if spec_type != 2:
            for info in spec_bytes:
                start_position = 0
                string_sublist = []
                [function_name_bytes, function_name_end] = parse_array_size(info, start_position)
                function_name = function_name_bytes.decode("utf-8")
                string_sublist.append("{:02d}".format(function_count))
                string_sublist.append(function_name)
                if max_length_string < len(function_name):
                    max_length_string = len(function_name)

                [return_names_bytes, return_name_end] = parse_array_size(info, function_name_end)
                [return_names, _] = parse_arrays(return_names_bytes)
                return_name_string = []
                for name in return_names:
                    return_name = name.decode("utf-8")
                    return_name_string.append(return_name)
                    if max_length_string < len(return_name):
                        max_length_string = len(return_name)
                if return_name_string:
                    string_sublist.insert(1, return_name_string)
                else:
                    string_sublist.insert(1, ['-'])

                [list_parameter_name_bytes, _] = parse_arrays(info[return_name_end:len(info)])
                para_name_string = []
                for para in list_parameter_name_bytes:
                    para_name = para.decode("utf-8")
                    para_name_string.append(para_name)
                    if max_length_string < len(para_name):
                        max_length_string = len(para_name)
                string_sublist.append(para_name_string)
                string_list.append(string_sublist)
                function_count += 1
        else:
            for info in spec_bytes:
                string_sublist = ["{:02d}".format(function_count)]
                para_name = info.decode("utf-8")
                string_sublist.append(para_name)
                if max_length_string < len(para_name):
                    max_length_string = len(para_name)
                string_list.append(string_sublist)
                function_count += 1
        string_list.insert(0, max_length_string)
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
