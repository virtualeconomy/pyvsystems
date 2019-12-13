from __future__ import print_function
from .error import *
from .opcode import Opcode
from .deser import *
import copy
from .contract_meta import ContractMeta as meta


def print_functions(functions_opcode, all_info):
    trigger = all_info[0]
    execute_fun = all_info[1]
    if len(functions_opcode) != (len(trigger) + len(execute_fun)):
        msg = 'Functions are not well defined in opc and textual!'
        throw_error(msg, InvalidParameterException)
    else:
        functions_spec = copy.deepcopy([trigger[0]] + execute_fun)
        for i in range(len(functions_opcode)):
            [function_id_byte, function_type_byte, return_type_bytes, list_para_type_bytes, list_opc_bytes] = \
                details_from_opcode(functions_opcode[i])
            function_hex = convert_bytes_to_hex(function_id_byte)
            if i == 0:
                prefix = "0"
            else:
                prefix = "1"
            function_type_key = prefix + "{:02d}".format(int(function_type_byte.hex(), 16))
            function_type = meta.function_type_map[function_type_key]
            function_hex.append(function_type_byte.hex())
            if len(list_para_type_bytes) > 0:
                list_para_type = [meta.data_type_list[para]
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
            print_a_function(function_type, function_hex, functions_spec[i], list_para_type, list_opc, all_info[2])

def print_a_function(function_type, function_hex, functions_spec, list_para_type, list_opc, all_state_var):
    return_type = functions_spec[1]
    function_name = functions_spec[2]
    para_name = functions_spec[3]
    state_var = all_state_var[0]
    if len(list_para_type) >= 1:
        list_para = para_name[:len(list_para_type)]
    else:
        list_para = []
    if len(list_para_type) != len(list_para):
        msg = 'List of parameter is not right!'
        throw_error(msg, InvalidParameterException)
    else:
        if function_type == meta.function_type_map['000']:
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
            print('return ' + meta.data_type_list[function_hex[4][i]] + ' ' + return_type[0])
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
    list_opc_name = [Opcode().function_name[opc[0] + opc[1]]
                     if len(opc) >= 2 else
                     throw_error('Opc function is not right!', InvalidParameterException)
                     for opc in list_opc]
    if len(list_opc_name) != len(list_opc):
        msg = 'Opc function is not right!'
        throw_error(msg, InvalidParameterException)
    else:
        name_list = copy.deepcopy(para_name)
        for i in range(len(list_opc_name)):
            data = copy.deepcopy([int(index) for index in list_opc[i]])
            print(' ' * 13, end='')
            Opcode().get_opc(list_opc_name[i], [data, name_list, state_var])
            print(' ' * 13, end='')
            print('| ' + list_opc[i][0] + ' ' + list_opc[i][1] + ' | ' + ' '.join(list_opc[i][2:]) + ' |')
        print(" ")

def print_textual_from_bytes(bytes_arrays):
    all_info = []
    if len(bytes_arrays) != 3:
        msg = 'Textual is invalid!'
        throw_error(msg, InvalidParameterException)
    [initializer_bytes, _] = parse_arrays(bytes_arrays[0])
    initializer_spec = specification_from_bytes(initializer_bytes, 0)
    print("Initializer Function:")
    specification_header = ['id', 'return_type', 'function_name', 'variables...']
    info = copy.deepcopy([specification_header, initializer_spec])
    print_function_specification(info)
    info[1].pop(0)
    all_info.append(info[1])

    [descriptor_bytes, _] = parse_arrays(bytes_arrays[1])
    descriptor_spec = specification_from_bytes(descriptor_bytes, 1)
    print("Descriptor Functions:")
    info = copy.deepcopy([specification_header, descriptor_spec])
    print_function_specification(info)
    info[1].pop(0)
    all_info.append(info[1])

    [state_var_bytes, _] = parse_arrays(bytes_arrays[2])
    state_var = specification_from_bytes(state_var_bytes, 2)
    specification_header = ['id', 'variable_name']
    print("State Variables:")
    info = copy.deepcopy([specification_header, state_var])
    print_state_var_specification(info)
    info[1].pop(0)
    all_info.append(info[1])
    return all_info

def details_from_opcode(opcode):
    function_id_two_bytes = opcode[0:2]
    function_type_byte = opcode[2:3]
    [return_type_bytes, return_type_end] = parse_array_size(opcode, 3)
    [list_para_type_bytes, list_para_type_end] = parse_array_size(opcode, return_type_end)
    [list_opc, _] = parse_array_size(opcode, list_para_type_end)
    [list_opc_bytes, _] = parse_arrays(list_opc)

    return [function_id_two_bytes, function_type_byte, return_type_bytes, list_para_type_bytes, list_opc_bytes]

def print_bytes_arrays(bytes_arrays):
    length = len(bytes_arrays)
    total_length = 0
    for i in range(length):
        info = convert_bytes_to_hex(bytes_arrays[i])
        print("{:02d}".format(i) + " | " + ' '.join(info) + " | (" + str(len(info)) + " Bytes)")
        total_length += len(info)
    print("(sum of length for the above Bytes: " + str(total_length) + ")")

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
            msg = 'Textual in function is invalid!'
            throw_error(msg, InvalidParameterException)
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

def specification_from_bytes(spec_bytes, spec_type):
    string_list = []
    id_count = 0
    max_length_string = 2
    if spec_type != 2:
        for info in spec_bytes:
            start_position = 0
            string_sublist = []
            [function_name_bytes, function_name_end] = parse_array_size(info, start_position)
            function_name = function_name_bytes.decode("utf-8")
            string_sublist.append("{:02d}".format(id_count))
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
            id_count += 1
    else:
        for info in spec_bytes:
            string_sublist = ["{:02d}".format(id_count)]
            para_name = info.decode("utf-8")
            string_sublist.append(para_name)
            if max_length_string < len(para_name):
                max_length_string = len(para_name)
            string_list.append(string_sublist)
            id_count += 1
    string_list.insert(0, max_length_string)
    return string_list


