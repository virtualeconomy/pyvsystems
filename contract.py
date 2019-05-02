from .crypto import *
from .error import *
import pyvsystems
from .opcode import *
from .deser import *
from .contract_build import *
from .contract_translator import *
from .contract_meta import ContractMeta as meta


class Contract(object):
    def __init__(self):
        self.contract_without_split_default = ContractBuild().create('vdds', 1, split=False)
        self.contract_with_split_default = ContractBuild().create('vdds', 1, split=True)

    def show_contract_function(self, bytes_string='', contract_id=''):
        contract_translator = ContractTranslator()
        if not bytes_string and not contract_id:
            msg = 'Input contract is empty!'
            pyvsystems.throw_error(msg, InvalidParameterException)

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

    # def sign_register_contract(self, privatekey):
    #     a = 1
    #
    # def sign_execute_contract(self):

    def contract_permitted(self, split=True):
        if split:
            contract = self.contract_with_split_default
        else:
            contract = self.contract_without_split_default
        return contract
