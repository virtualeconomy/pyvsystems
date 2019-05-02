import itertools
import logging
import struct

from pyvsystems import deser
from pyvsystems.contract_meta import ContractMeta as meta

from .crypto import *


class ContractBuild(object):

    def __init__(self, default_contract=False):
        self.data_type_list = {value: bytes([int(key)]) for key, value in meta.data_type_list.items()}
        self.function_type_map = {value: bytes([int(key[1:])]) for key, value in meta.function_type_map.items()}

        if default_contract:
            self.trigger = self.bytes_builder_from_list([self.init_fun_gen()])

            self.descriptor_without_split = self.bytes_builder_from_list(
                [self.supersede_fun_without_split_gen(), self.issue_fun_without_split_gen(),
                 self.destroy_fun_without_split_gen(),
                 self.send_fun_without_split_gen(), self.transfer_fun_without_split_gen(),
                 self.deposit_fun_without_split_gen(), self.withdraw_fun_without_split_gen(),
                 self.total_supply_fun_without_split_gen(),
                 self.max_supply_fun_without_split_gen(), self.balance_of_fun_without_split_gen(),
                 self.get_issuer_fun_without_split_gen()])

            self.descriptor_with_split = self.bytes_builder_from_list(
                [self.supersede_fun_gen(), self.issue_fun_gen(), self.destroy_fun_gen(), self.split_fun_gen(),
                 self.send_fun_gen(),
                 self.transfer_fun_gen(), self.deposit_fun_gen(), self.withdraw_fun_gen(), self.total_supply_fun_gen(),
                 self.max_supply_fun_gen(), self.balance_of_fun_gen(), self.get_issuer_fun_gen()])

            self.state_var = self.bytes_builder_from_list([meta.state_var_issuer + self.data_type_list.get('Address'), meta.state_var_maker + self.data_type_list.get('Address')])

            self.state_var_texture = deser.serialize_arrays([deser.serialize_string(name) for name in meta.state_var_name])
            self.initializer_texture = deser.serialize_arrays([self.init_func_bytes()])

            self.descriptor_texture_without_split = deser.serialize_arrays([self.supersede_func_bytes(),
                                                              self.issue_func_bytes(),
                                                              self.destroy_func_bytes(),
                                                              self.send_func_bytes(),
                                                              self.transfer_func_bytes(),
                                                              self.deposit_func_bytes(),
                                                              self.withdraw_func_bytes(),
                                                              self.total_supply_func_bytes(),
                                                              self.max_supply_func_bytes(),
                                                              self.balance_of_func_bytes(),
                                                              self.get_issuer_func_bytes()])

            self.descriptor_texture_with_split = deser.serialize_arrays([self.supersede_func_bytes(),
                                                              self.issue_func_bytes(),
                                                              self.destroy_func_bytes(),
                                                              self.split_func_bytes(),
                                                              self.send_func_bytes(),
                                                              self.transfer_func_bytes(),
                                                              self.deposit_func_bytes(),
                                                              self.withdraw_func_bytes(),
                                                              self.total_supply_func_bytes(),
                                                              self.max_supply_func_bytes(),
                                                              self.balance_of_func_bytes(),
                                                              self.get_issuer_func_bytes()])

            self.texture_without_split = deser.serialize_arrays([self.initializer_texture, self.descriptor_texture_without_split, self.state_var_texture])
            self.texture_with_split = deser.serialize_arrays(
                [self.initializer_texture, self.descriptor_texture_with_split, self.state_var_texture])

    def create(self, language_code, language_version, trigger=None, descriptor=None, state_var=None, texture=None, split=False):
        contract_lang_code = self.language_code_builder(language_code)
        contract_lang_ver = self.language_version_builder(language_version)
        if trigger is None:
            contract_trigger = self.trigger
        else:
            contract_trigger = self.bytes_builder_from_list(trigger)

        if descriptor is None:
            if split is False:
                contract_descriptor = self.descriptor_without_split
            else:
                contract_descriptor = self.descriptor_with_split
        else:
            contract_descriptor = self.bytes_builder_from_list(descriptor)

        if state_var is None:
            contract_state_var = self.state_var
        else:
            contract_state_var = self.bytes_builder_from_list(state_var)

        if texture is None:
            if split is False:
                contract_texture = self.texture_without_split
            else:
                contract_texture = self.texture_with_split
        else:
            contract_texture = deser.serialize_arrays(texture)

        contract_bytes = contract_lang_code + contract_lang_ver + contract_trigger + contract_descriptor + contract_state_var + contract_texture
        contract_byte_str = base58.b58encode(contract_bytes)
        return bytes2str(contract_byte_str)


    def opc_assert_is_caller_origin(self):
        return meta.assert_opc + meta.is_caller_origin_assert

    def opc_assert_is_signer_origin(self):
        return meta.assert_opc + meta.is_signer_origin_assert

    def opc_load_signer(self):
        return meta.load_opc + meta.signer_load

    def opc_load_caller(self):
        return meta.load_opc + meta.caller_load

    def opc_cdbv_set(self):
        return meta.cdbv_opc + meta.set_cdbv

    def opc_cdbvr_get(self):
        return meta.cdbvr_opc + meta.get_cdbvr

    def opc_tdb_new_token(self):
        return meta.tdb_opc + meta.new_token_tdb

    def opc_tdb_split(self):
        return meta.tdb_opc + meta.split_tdb

    def opc_tdbr_opc_max(self):
        return meta.tdbr_opc + meta.get_tdbr

    def opc_tdbr_opc_total(self):
        return meta.tdbr_opc + meta.total_tdbr

    def opc_tdba_deposit(self):
        return meta.tdba_opc + meta.deposit_tdba

    def opc_tdba_withdraw(self):
        return meta.tdba_opc + meta.withdraw_tdba

    def opc_tdba_transfer(self):
        return meta.tdba_opc + meta.transfer_tdba

    def opc_tdbar_balance(self):
        return meta.tdbar_opc + meta.balance_tdbar

    def opc_return_value(self):
        return meta.return_opc + bytes([1])

    def language_code_builder(self, code):
        if len(code) == meta.language_code_byte_length:
            language_code = deser.serialize_string(code)
            return language_code
        else:
            logging.error("Wrong language code length")

    def language_version_builder(self, version):
        try:
            if len(struct.pack(">I", version)) == meta.language_version_byte_length:
                return struct.pack(">I", version)
            else:
                logging.error("Wrong language version length")
        except:
            print("Wrong language version length")


    def bytes_builder_from_list(self, input_list):
        if type(input_list) is list:
            return deser.serialize_array(deser.serialize_arrays(input_list))
        else:
            logging.error("The input should be a list")

    def texture_fun_gen(self, name, ret, para):
        func_byte = deser.serialize_array(deser.serialize_string(name))
        ret_byte = deser.serialize_array(deser.serialize_arrays([deser.serialize_string(r) for r in ret]))
        para_byte = deser.serialize_arrays([deser.serialize_string(p) for p in para])
        texture = func_byte + ret_byte + para_byte
        return texture

    def init_func_bytes(self):
        return self.texture_fun_gen("init", [], meta.init_para)

    def supersede_func_bytes(self):
        return self.texture_fun_gen("supersede", [], meta.supersede_para)

    def issue_func_bytes(self):
        return self.texture_fun_gen("issue", [], meta.issue_para)

    def destroy_func_bytes(self):
        return self.texture_fun_gen("destroy", [], meta.destroy_para)

    def split_func_bytes(self):
        return self.texture_fun_gen("split", [], meta.split_para)

    def send_func_bytes(self):
        return self.texture_fun_gen("send", [], meta.send_para)

    def transfer_func_bytes(self):
        return self.texture_fun_gen("transfer", [], meta.transfer_para)

    def deposit_func_bytes(self):
        return self.texture_fun_gen("deposit", [], meta.deposit_para)

    def withdraw_func_bytes(self):
        return self.texture_fun_gen("withdraw", [], meta.withdraw_para)

    def total_supply_func_bytes(self):
        return self.texture_fun_gen("totalSupply", ["total"], meta.total_supply_para)

    def max_supply_func_bytes(self):
        return self.texture_fun_gen("maxSupply", ["max"], meta.max_supply_para)

    def balance_of_func_bytes(self):
        return self.texture_fun_gen("balanceOf", ["balance"], meta.balance_of_para)

    def get_issuer_func_bytes(self):
        return self.texture_fun_gen("getIssuer", ["issuer"], meta.get_issuer_para)


    def state_var_random_gen(self):
        self.fixed_size = 2
        state_var = bytearray(os.urandom(self.fixed_size))
        return state_var

    def state_var_gen(self, state_vars):
        state_vars = deser.serialize_arrays(state_vars)
        return state_vars

    def a_function_gen(self, fun_idx, fun_type, proto_type, list_opc):
        fun = fun_idx + fun_type + proto_type + list_opc
        return fun

    def init_fun_gen(self):
        fun = self.a_function_gen(self.init_fun_id_gen(), self.function_type_map.get("onInit"), self.proto_type_gen(meta.non_return_type, self.init_para_type()), self.list_opc_gen(self.init_opc(), self.init_opc_index()))
        return fun

    def supersede_fun_gen(self):
        fun = self.a_function_gen(self.supersede_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.supersede_para_type()), self.list_opc_gen(self.supersede_opc(), self.supersede_opc_index()))
        return fun

    def supersede_fun_without_split_gen(self):
        fun = self.a_function_gen(self.supersede_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.supersede_para_type()), self.list_opc_gen(self.supersede_opc(), self.supersede_opc_index()))
        return fun

    def issue_fun_gen(self):
        fun = self.a_function_gen(self.issue_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.issue_para_type()), self.list_opc_gen(self.issue_opc(), self.issue_opc_index()))
        return fun

    def issue_fun_without_split_gen(self):
        fun = self.a_function_gen(self.issue_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.issue_para_type()), self.list_opc_gen(self.issue_opc(), self.issue_opc_index()))
        return fun

    def destroy_fun_gen(self):
        fun = self.a_function_gen(self.destroy_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.destroy_para_type()), self.list_opc_gen(self.destroy_opc(), self.destroy_opc_index()))
        return fun

    def destroy_fun_without_split_gen(self):
        fun = self.a_function_gen(self.destroy_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.destroy_para_type()), self.list_opc_gen(self.destroy_opc(), self.destroy_opc_index()))
        return fun

    def split_fun_gen(self):
        fun = self.a_function_gen(self.split_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.split_para_type()), self.list_opc_gen(self.split_opc(), self.split_opc_index()))
        return fun

    def send_fun_gen(self):
        fun = self.a_function_gen(self.send_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.send_para_type()), self.list_opc_gen(self.send_opc(), self.send_opc_index()))
        return fun

    def send_fun_without_split_gen(self):
        fun = self.a_function_gen(self.send_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.send_para_type()), self.list_opc_gen(self.send_opc(), self.send_opc_index()))
        return fun

    def transfer_fun_gen(self):
        fun = self.a_function_gen(self.transfer_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.transfer_para_type()), self.list_opc_gen(self.transfer_opc(), self.transfer_opc_index()))
        return fun

    def transfer_fun_without_split_gen(self):
        fun = self.a_function_gen(self.transfer_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.transfer_para_type()), self.list_opc_gen(self.transfer_opc(), self.transfer_opc_index()))
        return fun

    def deposit_fun_gen(self):
        fun = self.a_function_gen(self.deposit_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.deposit_para_type()), self.list_opc_gen(self.deposit_opc(), self.deposit_opc_index()))
        return fun

    def deposit_fun_without_split_gen(self):
        fun = self.a_function_gen(self.deposit_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.deposit_para_type()), self.list_opc_gen(self.deposit_opc(), self.deposit_opc_index()))
        return fun

    def withdraw_fun_gen(self):
        fun = self.a_function_gen(self.withdraw_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.withdraw_para_type()), self.list_opc_gen(self.withdraw_opc(), self.withdraw_opc_index()))
        return fun

    def withdraw_fun_without_split_gen(self):
        fun = self.a_function_gen(self.withdraw_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen(meta.non_return_type, self.withdraw_para_type()), self.list_opc_gen(self.withdraw_opc(), self.withdraw_opc_index()))
        return fun

    def total_supply_fun_gen(self):
        fun = self.a_function_gen(self.total_supply_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Amount')], self.total_supply_para_type()), self.list_opc_gen(self.total_supply_opc(), self.total_supply_opc_index()))
        return fun

    def total_supply_fun_without_split_gen(self):
        fun = self.a_function_gen(self.total_supply_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Amount')], self.total_supply_para_type()), self.list_opc_gen(self.total_supply_opc(), self.total_supply_opc_index()))
        return fun

    def max_supply_fun_gen(self):
        fun = self.a_function_gen(self.max_supply_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Amount')], self.max_supply_para_type()), self.list_opc_gen(self.max_supply_opc(), self.max_supply_opc_index()))
        return fun

    def max_supply_fun_without_split_gen(self):
        fun = self.a_function_gen(self.max_supply_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Amount')], self.max_supply_para_type()), self.list_opc_gen(self.max_supply_opc(), self.max_supply_opc_index()))
        return fun

    def balance_of_fun_gen(self):
        fun = self.a_function_gen(self.balance_of_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Amount')], self.balance_of_para_type()), self.list_opc_gen(self.balance_of_opc(), self.balance_of_opc_index()))
        return fun

    def balance_of_fun_without_split_gen(self):
        fun = self.a_function_gen(self.balance_of_fun_id_without_split_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Amount')], self.balance_of_para_type()), self.list_opc_gen(self.balance_of_opc(), self.balance_of_opc_index()))
        return fun

    def get_issuer_fun_gen(self):
        fun = self.a_function_gen(self.get_issuer_fun_id_gen(), self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Account')], self.get_issuer_para_type()), self.list_opc_gen(self.get_issuer_opc(), self.get_issuer_opc_index()))
        return fun

    def get_issuer_fun_without_split_gen(self):
        fun = self.a_function_gen(self.get_issuer_fun_id_without_split_gen(),self.function_type_map.get("public"), self.proto_type_gen([self.data_type_list.get('Account')], self.get_issuer_para_type()), self.list_opc_gen(self.get_issuer_opc(), self.get_issuer_opc_index()))
        return fun

    def init_fun_id_gen(self):
        return struct.pack(">H", meta.init)
    def supersede_fun_id_gen(self):
        return struct.pack(">H", meta.supersede)
    def supersede_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.supersede_without_split)
    def issue_fun_id_gen(self):
        return struct.pack(">H", meta.issue)
    def issue_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.issue_without_split)
    def destroy_fun_id_gen(self):
        return struct.pack(">H", meta.destroy)
    def destroy_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.destroy_without_split)
    def split_fun_id_gen(self):
        return struct.pack(">H", meta.split)
    def send_fun_id_gen(self):
        return struct.pack(">H", meta.send)
    def send_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.send_without_split)
    def transfer_fun_id_gen(self):
        return struct.pack(">H", meta.transfer)
    def transfer_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.transfer_without_split)
    def deposit_fun_id_gen(self):
        return struct.pack(">H", meta.deposit)
    def deposit_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.deposit_without_split)
    def withdraw_fun_id_gen(self):
        return struct.pack(">H", meta.withdraw)
    def withdraw_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.withdraw_without_split)
    def total_supply_fun_id_gen(self):
        return struct.pack(">H", meta.total_supply)
    def total_supply_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.total_supply_without_split)
    def max_supply_fun_id_gen(self):
        return struct.pack(">H", meta.max_supply)
    def max_supply_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.max_supply_without_split)
    def balance_of_fun_id_gen(self):
        return struct.pack(">H", meta.balance_of)
    def balance_of_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.balance_of_without_split)
    def get_issuer_fun_id_gen(self):
        return struct.pack(">H", meta.get_issuer)
    def get_issuer_fun_id_without_split_gen(self):
        return struct.pack(">H", meta.get_issuer_without_split)


    def proto_type_gen(self, return_type, list_para_types):
        proto_type = deser.serialize_array(return_type) + deser.serialize_array(list_para_types)
        return proto_type

    def init_para_type_wrong(self):
        return [self.data_type_list.get('Amount'), self.data_type_list.get('Amount')]

    def init_para_type(self):
        return [self.data_type_list.get('Amount'), self.data_type_list.get('Amount'), self.data_type_list.get('ShortText')]

    def supersede_para_type(self):
        return [self.data_type_list.get('Account')]

    def issue_para_type(self):
        return [self.data_type_list.get('Amount')]

    def destroy_para_type(self):
        return [self.data_type_list.get('Amount')]

    def split_para_type(self):
        return [self.data_type_list.get('Amount')]

    def send_para_type(self):
        return [self.data_type_list.get('Account'), self.data_type_list.get('Amount')]

    def transfer_para_type(self):
        return [self.data_type_list.get('Account'), self.data_type_list.get('Account'), self.data_type_list.get('Amount')]

    def deposit_para_type(self):
        return [self.data_type_list.get('Account'), self.data_type_list.get('ContractAccount'), self.data_type_list.get('Amount')]

    def withdraw_para_type(self):
        return [self.data_type_list.get('ContractAccount'), self.data_type_list.get('Account'), self.data_type_list.get('Amount')]

    def total_supply_para_type(self):
        return bytes('', encoding='utf-8')

    def max_supply_para_type(self):
        return bytes('', encoding='utf-8')

    def balance_of_para_type(self):
        return [self.data_type_list.get('Account')]

    def get_issuer_para_type(self):
        return bytes('', encoding='utf-8')


    def list_opc_gen(self, ids, index_input):
        length = struct.pack(">H", sum(list(map(lambda x: len(x[0]+x[1])+2, list(zip(ids, index_input))))) + 2)
        num_opc = struct.pack(">H", len(ids))
        list_opc = bytes(itertools.chain.from_iterable(list(map(lambda x: struct.pack(">H",len(x[0]+x[1]))+x[0]+x[1], list(zip(ids, index_input))))))
        len_list_opc = length + num_opc + list_opc
        return len_list_opc


    def opc_load_signer_index(self):
        return bytes([3])

    def opc_load_caller_index(self):
        return bytes([2])

    def init_opc_cdbv_set_signer_index(self):
        return meta.state_var_issuer + meta.init_input_issuer_load_index

    def init_opc_cdbv_set_maker_index(self):
        return meta.state_var_maker + meta.init_input_issuer_load_index

    def init_opc_tdb_new_token_index(self):
        return meta.init_input_max_index + meta.init_input_unity_index + meta.init_input_short_text_index

    def init_wrong_tdb_opc(self):
        return [self.opc_load_signer(), self.opc_cdbv_set(), self.opc_cdbv_set(), bytes([5]), bytes([3])]

    def init_opc(self):
        return [self.opc_load_signer(), self.opc_cdbv_set(), self.opc_cdbv_set(), self.opc_tdb_new_token()]

    def init_opc_index(self):
        return [self.opc_load_signer_index(), self.init_opc_cdbv_set_signer_index(), self.init_opc_cdbv_set_maker_index(), self.init_opc_tdb_new_token_index()]

    def supersede_opc_cdbvr_get_index(self):
        return meta.state_var_maker + bytes([1])

    def supersede_assert_is_signer_origin_index(self):
        return meta.supersede_input_maker

    def supersede_opc_cdbv_set_index(self):
        return meta.state_var_issuer + meta.supersede_input_new_issuer_index

    def supersede_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_signer_origin(), self.opc_cdbv_set()]

    def supersede_opc_index(self):
        return [self.supersede_opc_cdbvr_get_index(), self.supersede_assert_is_signer_origin_index(), self.supersede_opc_cdbv_set_index()]

    def issue_opc_cdbvr_get_index(self):
        return meta.state_var_issuer + bytes([1])

    def issue_opc_assert_is_caller_origin_index(self):
        return meta.issue_input_issuer_get_index

    def issue_opc_tdba_deposit_index(self):
        return meta.issue_input_issuer_get_index + meta.issue_input_amount_index

    def issue_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdba_deposit()]

    def issue_opc_index(self):
        return [self.issue_opc_cdbvr_get_index(), self.issue_opc_assert_is_caller_origin_index(), self.issue_opc_tdba_deposit_index()]

    def destroy_opc_cdbvr_get_index(self):
        return meta.state_var_issuer + bytes([1])

    def destroy_opc_assert_is_caller_origin_index(self):
        return meta.destroy_input_issuer_get_index

    def destroy_opc_tdba_withdraw_index(self):
        return meta.destroy_input_issuer_get_index + meta.destroy_input_destroy_amount_index

    def destroy_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdba_withdraw()]

    def destroy_opc_index(self):
        return [self.destroy_opc_cdbvr_get_index(), self.destroy_opc_assert_is_caller_origin_index(), self.destroy_opc_tdba_withdraw_index()]

    def split_opc_cdbvr_get_index(self):
        return meta.state_var_issuer + bytes([1])

    def split_opc_assert_is_caller_origin_index(self):
        return meta.split_input_issuer_get_index

    def split_opc_tdb_split_index(self):
        return meta.split_input_new_unity_index

    def split_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdb_split()]

    def split_opc_index(self):
        return [self.split_opc_cdbvr_get_index(), self.split_opc_assert_is_caller_origin_index(), self.split_opc_tdb_split_index()]

    def send_opc_tdba_transfer_index(self):
        return meta.send_input_sender_index + meta.send_input_recipient_index + meta.send_input_amount_index

    def send_opc(self):
        return [self.opc_load_caller(), self.opc_tdba_transfer()]

    def send_opc_index(self):
        return [self.opc_load_caller_index(), self.send_opc_tdba_transfer_index()]

    def transfer_opc_assert_is_caller_origin_index(self):
        return meta.transfer_input_sender_index

    def transfer_opc_tdba_transfer_index(self):
        return meta.transfer_input_sender_index + meta.transfer_input_recipient_index + meta.transfer_input_amount_index

    def transfer_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def transfer_opc_index(self):
        return [self.transfer_opc_assert_is_caller_origin_index(), self.transfer_opc_tdba_transfer_index()]

    def deposit_opc_assert_is_caller_origin_index(self):
        return meta.deposit_input_sender_index

    def deposit_opc_tdba_transfer_index(self):
        return meta.deposit_input_sender_index + meta.deposit_input_smart_contract_index + meta.deposit_input_amount_index

    def deposit_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def deposit_opc_index(self):
        return [self.deposit_opc_assert_is_caller_origin_index(), self.deposit_opc_tdba_transfer_index()]

    def withdraw_opc_assert_is_caller_origin_index(self):
        return meta.withdraw_input_recipient_index

    def withdraw_opc_tdba_transfer_index(self):
        return meta.withdraw_input_smart_contract_index + meta.withdraw_input_recipient_index + meta.withdraw_input_amount_index

    def withdraw_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def withdraw_opc_index(self):
        return [self.withdraw_opc_assert_is_caller_origin_index(), self.withdraw_opc_tdba_transfer_index()]

    def total_supply_opc_tdbr_total_index(self):
        return bytes([0])

    def total_supply_opc(self):
        return [self.opc_tdbr_opc_total(), self.opc_return_value()]

    def total_supply_opc_index(self):
        return [self.total_supply_opc_tdbr_total_index(), bytes([0])]

    def max_supply_opc_tdbr_max_index(self):
        return bytes([0])

    def max_supply_opc(self):
        return [self.opc_tdbr_opc_max(), self.opc_return_value()]

    def max_supply_opc_index(self):
        return [self.max_supply_opc_tdbr_max_index(), bytes([0])]

    def balance_of_opc_tdbar_balance_index(self):
        return meta.balance_of_input_account_index + bytes([1])

    def balance_of_opc(self):
        return [self.opc_tdbar_balance(), self.opc_return_value()]

    def balance_of_opc_index(self):
        return [self.balance_of_opc_tdbar_balance_index(), bytes([1])]

    def get_issuer_opc_cdbvr_get_index(self):
        return meta.state_var_issuer + bytes([0])

    def get_issuer_opc(self):
        return [self.opc_cdbvr_get(), self.opc_return_value()]

    def get_issuer_opc_index(self):
        return [self.get_issuer_opc_cdbvr_get_index(), bytes([0])]

