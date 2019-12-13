from .contract_methods import *
from .contract_builder import *
import base58


class Contract(object):
    def __init__(self, language_code='vdds', language_version=1, trigger=None, descriptor=None, state_var=None, textual=None, split=False):
        self.contract_lang_code = language_code_builder(language_code)
        self.contract_lang_ver = language_version_builder(language_version)
        if trigger is None:
            self.contract_trigger = ContractDefaults.trigger
        else:
            self.contract_trigger = bytes_builder_from_list(trigger)

        if descriptor is None:
            if split is False:
                self.contract_descriptor = ContractDefaults.descriptor_without_split
            else:
                self.contract_descriptor = ContractDefaults.descriptor_with_split
        else:
            self.contract_descriptor = bytes_builder_from_list(descriptor)

        if state_var is None:
            self.contract_state_var = ContractDefaults.state_var
        else:
            self.contract_state_var = bytes_builder_from_list(state_var)

        if textual is None:
            if split is False:
                self.contract_textual = ContractDefaults.textual_without_split
            else:
                self.contract_textual = ContractDefaults.textual_with_split
        else:
            self.contract_textual = deser.serialize_arrays(textual)
        self.contract_bytes = self.contract_lang_code + self.contract_lang_ver + self.contract_trigger\
                              + self.contract_descriptor + self.contract_state_var + self.contract_textual

        self.contract_bytes_string = bytes2str(base58.b58encode(self.contract_bytes))

    def show_functions(self):
        show_contract_function(bytes_string=self.contract_bytes_string)


def contract_from_json(contract_json):
    triggers = [base58.b58decode(item) for item in contract_json['triggers']]
    descriptors = [base58.b58decode(item) for item in contract_json['descriptors']]
    state_variables = [base58.b58decode(item) for item in contract_json['stateVariables']]
    textuals = [base58.b58decode(contract_json['textual']['triggers']), base58.b58decode(contract_json['textual']['descriptors']),
                base58.b58decode(contract_json['textual']['stateVariables'])]

    contract = Contract(contract_json['languageCode'], contract_json['languageVersion'],
                                                  triggers, descriptors, state_variables, textuals)
    return contract


def show_contract_function(bytes_string='', contract_id='', wrapper=None):
    if not bytes_string and not contract_id:
        msg = 'Input contract is empty!'
        throw_error(msg, InvalidParameterException)

    if bytes_string and contract_id:
        msg = 'Multiple input in contract!'
        throw_error(msg, InvalidParameterException)

    if contract_id:
        if not wrapper:
            msg = 'No wrapper information!'
            throw_error(msg, InvalidParameterException)
        contract_content = get_contract_content(wrapper, contract_id)
        bytes_string = str2bytes(contract_from_json(contract_content).contract_bytes_string)

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
    print_bytes_arrays(descriptor)

    [state_var_arrays, state_var_end] = parse_array_size(bytes_object, descriptor_end)
    [state_var, bytes_length] = parse_arrays(state_var_arrays)
    print("State Variable: " + "(" + str(bytes_length) + " Bytes)")
    print("id" + " | byte")
    print_bytes_arrays(state_var)

    [textual, _] = parse_arrays(bytes_object[state_var_end:len(bytes_object)])
    all_info = print_textual_from_bytes(textual)

    functions_bytes = copy.deepcopy(trigger + descriptor)
    print("All Functions with Opcode:")
    print_functions(functions_bytes, all_info)



