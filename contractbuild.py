import itertools
import os
import struct

import base58

from pyvsystems import deser
from pyvsystems.dataentry import DataEntry
from pyvsystems.deser import serialize_string


class ContractBuild(object):
    # texture
    init_para = ["max", "unity", "tokenDescription", "signer"]
    supersede_para = ["newIssuer", "maker"]
    issue_para = ["amount", "issuer"]
    destroy_para = ["amount", "issuer"]
    split_para = ["newUnity", "issuer"]
    send_para = ["recipient", "amount", "caller"]
    transfer_para = ["sender", "recipient", "amount"]
    deposit_para = ["sender", "smart", "amount"]
    withdraw_para = ["smart", "recipient", "amount"]
    total_supply_para = ["total"]
    max_supply_para = ["max"]
    balance_of_para = ["address", "balance"]
    get_issuer_para = ["issuer"]

    # statevar
    state_var_issuer = bytes([0])
    state_var_maker = bytes([1])

    # datatype
    public_key = bytes([1])
    address = bytes([2])
    amount = bytes([3])
    int32 = bytes([4])
    short_text = bytes([5])
    contract_account = bytes([6])
    account = bytes([7])

    # assertype
    gteq_zero_assert = bytes([1])
    lteq_assert = bytes([2])
    lt_int64_assert = bytes([3])
    gt_zero_assert = bytes([4])
    eq_assert =bytes([5])
    is_caller_origin_assert = bytes([6])
    is_signer_origin_assert = bytes([7])

    # cdbvtype
    set_cdbv = bytes([1])

    # cdbvrtype
    get_cdbvr = bytes([1])

    # loadtype
    signer_load = bytes([1])
    caller_load =bytes([2])

    # opctype
    assert_opc = bytes([1])
    load_opc = bytes([2])
    cdbv_opc = bytes([3])
    cdbvr_opc = bytes([4])
    tdb_opc = bytes([5])
    tdbr_opc = bytes([6])
    tdba_opc = bytes([7])
    tdbar_opc = bytes([8])
    return_opc = bytes([9])

    # tdbatype
    deposit_tdba = bytes([1])
    withdraw_tdba = bytes([2])
    transfer_tdba = bytes([3])

    # tdbartype
    balance_tdbar = bytes([1])

    # tdbtype
    new_token_tdb = bytes([1])
    split_tdb = bytes([2])

    # tdbrtype
    get_tdbr = bytes([1])
    total_tdbr = bytes([2])

    # funid
    init = 0
    supersede = 0
    issue = 1
    destroy = 2
    split = 3
    send = 4
    transfer = 5
    deposit = 6
    withdraw = 7
    total_supply = 8
    max_supply = 9
    balance_of = 10
    get_issuer = 11

    supersede_without_split = 0
    issue_without_split = 1
    destroy_without_split = 2
    send_without_split = 3
    transfer_without_split = 4
    deposit_without_split = 5
    withdraw_without_split = 6
    total_supply_without_split = 7
    max_supply_without_split = 8
    balance_of_without_split = 9
    get_issuer_without_split = 10

    supersede_index = bytes([0])
    issue_index = bytes([1])
    destroy_index = bytes([2])
    split_index = bytes([3])
    send_index = bytes([4])
    transfer_index = bytes([5])
    deposit_index = bytes([6])
    withdraw_index = bytes([7])
    total_supply_index = bytes([8])
    max_supply_index = bytes([9])
    balance_of_index = bytes([10])
    get_issuer_index = bytes([11])

    # funtype
    non_return_type = bytes('',encoding ='utf-8')
    on_init_trigger_type = 0
    public_func_type = 0

    # datastack
    init_input_max_index = bytes([0])
    init_input_unity_index = bytes([1])
    init_input_short_text_index = bytes([2])
    init_input_issuer_load_index = bytes([3])

    supersede_input_new_issuer_index = bytes([0])
    supersede_input_maker = bytes([1])

    split_input_new_unity_index = bytes([0])
    split_input_issuer_get_index = bytes([1])

    destroy_input_destroy_amount_index = bytes([0])
    destroy_input_issuer_get_index = bytes([1])

    issue_input_amount_index = bytes([0])
    issue_input_issuer_get_index = bytes([1])

    send_input_recipient_index = bytes([0])
    send_input_amount_index = bytes([1])
    send_input_sender_index = bytes([2])

    transfer_input_sender_index = bytes([0])
    transfer_input_recipient_index = bytes([1])
    transfer_input_amount_index = bytes([2])

    deposit_input_sender_index = bytes([0])
    deposit_input_smart_contract_index = bytes([1])
    deposit_input_amount_index = bytes([2])

    withdraw_input_smart_contract_index = bytes([0])
    withdraw_input_recipient_index = bytes([1])
    withdraw_input_amount_index = bytes([2])

    balance_of_input_account_index = bytes([0])

    def __init__(self, language_code, language_version, split=False):
        self.lang_code = self.language_code_builder(language_code)
        self.lang_ver = self.language_version_builder(language_version)
        self.trigger = self.trigger_builder()
        self.descriptor = self.descriptor_builder(split)
        self.state_var = self.state_var_builder()
        self.texture = self.texture_builder(split)
        self.contract_bytes = self.lang_code + self.lang_ver + self.trigger + self.descriptor + self.state_var + self.texture
        self.contract_byte_str = base58.b58encode(self.contract_bytes)

    # OpcId
    def assert_gteq_zero_gen(self):
        return self.opc_assert_gteq_zero()
    def assert_lteq_gen(self):
        return self.opc_assert_lteq()
    def assert_lt_int64_gen(self):
        return self.opc_assert_lt_int64()
    def assert_gt_zero_gen(self):
        return self.opc_assert_gt_zero()
    def assert_eq_gen(self):
        return self.opc_assert_eq()
    def assert_is_caller_origin_gen(self):
        return self.opc_assert_is_caller_origin()
    def assert_is_signer_origin_gen(self):
        return self.opc_assert_is_signer_origin()
    def load_signer_gen(self):
        return self.opc_load_signer()
    def load_caller_gen(self):
        return self.opc_load_caller()
    def cdbv_set_gen(self):
        return self.opc_cdbv_set()
    def cdbvr_get_gen(self):
        return self.opc_cdbvr_get()
    def tdb_new_token_gen(self):
        return self.opc_tdb_new_token()
    def tdb_split_gen(self):
        return self.opc_tdb_split()
    def tdbr_opc_max(self):
        return self.opc_tdbr_opc_max()
    def tdbr_opc_total_gen(self):
        return self.opc_tdbr_opc_total()
    def tdba_deposit_gen(self):
        return self.opc_tdba_deposit()
    def tdba_withdraw_gen(self):
        return self.opc_tdba_withdraw()
    def tdba_transfer_gen(self):
        return self.opc_tdba_transfer()
    def tdbar_balance_gen(self):
        return self.opc_tdbar_balance()

    def opc_assert_gteq_zero(self):
        return self.assert_opc + self.gteq_zero_assert

    def opc_assert_lteq(self):
        return self.assert_opc + self.lteq_assert

    def opc_assert_lt_int64(self):
        return self.assert_opc + self.lt_int64_assert

    def opc_assert_gt_zero(self):
        return self.assert_opc + self.gt_zero_assert

    def opc_assert_eq(self):
        return self.assert_opc + self.eq_assert

    def opc_assert_is_caller_origin(self):
        return self.assert_opc + self.is_caller_origin_assert

    def opc_assert_is_signer_origin(self):
        return self.assert_opc + self.is_signer_origin_assert

    def opc_load_signer(self):
        return self.load_opc + self.signer_load

    def opc_load_caller(self):
        return self.load_opc + self.caller_load

    def opc_cdbv_set(self):
        return self.cdbv_opc + self.set_cdbv

    def opc_cdbvr_get(self):
        return self.cdbvr_opc + self.get_cdbvr

    def opc_tdb_new_token(self):
        return self.tdb_opc + self.new_token_tdb

    def opc_tdb_split(self):
        return self.tdb_opc + self.split_tdb

    def opc_tdbr_opc_max(self):
        return self.tdbr_opc + self.get_tdbr

    def opc_tdbr_opc_total(self):
        return self.tdbr_opc + self.total_tdbr

    def opc_tdba_deposit(self):
        return self.tdba_opc + self.deposit_tdba

    def opc_tdba_withdraw(self):
        return self.tdba_opc + self.withdraw_tdba

    def opc_tdba_transfer(self):
        return self.tdba_opc + self.transfer_tdba

    def opc_tdbar_balance(self):
        return self.tdbar_opc + self.balance_tdbar

    def opc_return_value(self):
        return self.return_opc + bytes([1])

    # languageCode
    def language_code_builder(self, code):
        language_code = deser.serialize_string(code)
        return language_code

    # languageVersion
    def language_version_builder(self, version):
        return struct.pack(">I", version)

    # trigger
    def trigger_builder(self):
        return deser.serialize_array(deser.serialize_arrays([self.init_fun_gen()]))

    # descriptor
    def descriptor_builder(self, split):
        if(split is False):
            descriptor = deser.serialize_arrays(
                [self.supersede_fun_without_split_gen(), self.issue_fun_without_split_gen(), self.destroy_fun_without_split_gen(),
                 self.send_fun_without_split_gen(), self.transfer_fun_without_split_gen(), self.deposit_fun_without_split_gen(), self.withdraw_fun_without_split_gen(), self.total_supply_fun_without_split_gen(),
                 self.max_supply_fun_without_split_gen(), self.balance_of_fun_without_split_gen(), self.get_issuer_fun_without_split_gen()])
        else:
            descriptor = deser.serialize_arrays([self.supersede_fun_gen(), self.issue_fun_gen(), self.destroy_fun_gen(), self.split_fun_gen(), self.send_fun_gen(),
                                                self.transfer_fun_gen(), self.deposit_fun_gen(), self.withdraw_fun_gen(), self.total_supply_fun_gen(),
                                                self.max_supply_fun_gen(), self.balance_of_fun_gen(), self.get_issuer_fun_gen()])

        return deser.serialize_array(descriptor)


    # stateVar
    def state_var_builder(self):
        state_var = self.state_var_gen([self.state_var_issuer + self.address, self.state_var_maker + self.address])
        return deser.serialize_array(state_var)

    # texture
    def texture_builder(self, split):
        self._fixed_size = 4
        self.state_var_name = ["issuer", "maker"]
        self.state_var_texture = deser.serialize_arrays([deser.serialize_string(name) for name in self.state_var_name])
        self.initializer_texture = deser.serialize_arrays([self.init_func_bytes()])
        if(split is False):
            self.descriptor_texture = deser.serialize_arrays([self.supersede_func_bytes(),
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
        else:
            self.descriptor_texture = deser.serialize_arrays([self.supersede_func_bytes(),
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

        self.texture_right_gen = self.texture_gen(self.initializer_texture, self.descriptor_texture, self.state_var_texture)

        return self.texture_right_gen

    def texture_random_gen(self):
        texture = bytearray(os.urandom(self._fixed_size))
        return texture

    def texture_gen(self, initialization, description, state_var):
        return deser.serialize_arrays([initialization, description, state_var])

    def texture_fun_gen(self, name, ret, para):
        func_byte = deser.serialize_array(deser.serialize_string(name))
        ret_byte = deser.serialize_array(deser.serialize_arrays([deser.serialize_string(r) for r in ret]))
        para_byte = deser.serialize_arrays([deser.serialize_string(p) for p in para])
        texture = func_byte + ret_byte + para_byte
        return texture


    def init_func_bytes(self):
        return self.texture_fun_gen("init", [], self.init_para)

    def supersede_func_bytes(self):
        return self.texture_fun_gen("supersede", [], self.supersede_para)

    def issue_func_bytes(self):
        return self.texture_fun_gen("issue", [], self.issue_para)

    def destroy_func_bytes(self):
        return self.texture_fun_gen("destroy", [], self.destroy_para)

    def split_func_bytes(self):
        return self.texture_fun_gen("split", [], self.split_para)

    def send_func_bytes(self):
        return self.texture_fun_gen("send", [], self.send_para)

    def transfer_func_bytes(self):
        return self.texture_fun_gen("transfer", [], self.transfer_para)

    def deposit_func_bytes(self):
        return self.texture_fun_gen("deposit", [], self.deposit_para)

    def withdraw_func_bytes(self):
        return self.texture_fun_gen("withdraw", [], self.withdraw_para)

    def total_supply_func_bytes(self):
        return self.texture_fun_gen("totalSupply", ["total"], self.total_supply_para)

    def max_supply_func_bytes(self):
        return self.texture_fun_gen("maxSupply", ["max"], self.max_supply_para)

    def balance_of_func_bytes(self):
        return self.texture_fun_gen("balanceOf", ["balance"], self.balance_of_para)

    def get_issuer_func_bytes(self):
        return self.texture_fun_gen("getIssuer", ["issuer"], self.get_issuer_para)


    # statevar
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
        fun = self.a_function_gen(self.init_fun_id_gen(), self.init_fun_type_gen(), self.proto_type_init_gen(), self.init_opc_line_gen())
        return fun

    def supersede_fun_gen(self):
        fun = self.a_function_gen(self.supersede_fun_id_gen(), self.supersede_fun_type_gen(), self.proto_type_supersede_gen(), self.supersede_opc_line_gen())
        return fun

    def supersede_fun_without_split_gen(self):
        fun = self.a_function_gen(self.supersede_fun_id_without_split_gen(), self.supersede_fun_type_gen(), self.proto_type_supersede_gen(), self.supersede_opc_line_gen())
        return fun

    def issue_fun_gen(self):
        fun = self.a_function_gen(self.issue_fun_id_gen(), self.issue_fun_type_gen(), self.proto_type_issue_gen(), self.issue_opc_line_gen())
        return fun

    def issue_fun_without_split_gen(self):
        fun = self.a_function_gen(self.issue_fun_id_without_split_gen(), self.issue_fun_type_gen(), self.proto_type_issue_gen(), self.issue_opc_line_gen())
        return fun

    def destroy_fun_gen(self):
        fun = self.a_function_gen(self.destroy_fun_id_gen(), self.destroy_fun_type_gen(), self.proto_type_destroy_gen(), self.destroy_opc_line_gen())
        return fun

    def destroy_fun_without_split_gen(self):
        fun = self.a_function_gen(self.destroy_fun_id_without_split_gen(), self.destroy_fun_type_gen(), self.proto_type_destroy_gen(), self.destroy_opc_line_gen())
        return fun

    def split_fun_gen(self):
        fun = self.a_function_gen(self.split_fun_id_gen(), self.split_fun_type_gen(), self.proto_type_split_gen(), self.split_opc_line_gen())
        return fun

    def send_fun_gen(self):
        fun = self.a_function_gen(self.send_fun_id_gen(), self.send_fun_type_gen(), self.proto_type_send_gen(), self.send_opc_line_gen())
        return fun

    def send_fun_without_split_gen(self):
        fun = self.a_function_gen(self.send_fun_id_without_split_gen(), self.send_fun_type_gen(), self.proto_type_send_gen(), self.send_opc_line_gen())
        return fun

    def transfer_fun_gen(self):
        fun = self.a_function_gen(self.transfer_fun_id_gen(), self.transfer_fun_type_gen(), self.proto_type_transfer_gen(), self.transfer_opc_line_gen())
        return fun

    def transfer_fun_without_split_gen(self):
        fun = self.a_function_gen(self.transfer_fun_id_without_split_gen(), self.transfer_fun_type_gen(), self.proto_type_transfer_gen(), self.transfer_opc_line_gen())
        return fun

    def deposit_fun_gen(self):
        fun = self.a_function_gen(self.deposit_fun_id_gen(), self.deposit_fun_type_gen(), self.proto_type_deposit_gen(), self.deposit_opc_line_gen())
        return fun

    def deposit_fun_without_split_gen(self):
        fun = self.a_function_gen(self.deposit_fun_id_without_split_gen(), self.deposit_fun_type_gen(), self.proto_type_deposit_gen(), self.deposit_opc_line_gen())
        return fun

    def withdraw_fun_gen(self):
        fun = self.a_function_gen(self.withdraw_fun_id_gen(), self.withdraw_fun_type_gen(), self.proto_type_withdraw_gen(), self.withdraw_opc_line_gen())
        return fun

    def withdraw_fun_without_split_gen(self):
        fun = self.a_function_gen(self.withdraw_fun_id_without_split_gen(), self.withdraw_fun_type_gen(), self.proto_type_withdraw_gen(), self.withdraw_opc_line_gen())
        return fun

    def total_supply_fun_gen(self):
        fun = self.a_function_gen(self.total_supply_fun_id_gen(), self.total_supply_fun_type_gen(), self.proto_type_total_supply_gen(), self.total_supply_opc_line_gen())
        return fun

    def total_supply_fun_without_split_gen(self):
        fun = self.a_function_gen(self.total_supply_fun_id_without_split_gen(), self.total_supply_fun_type_gen(), self.proto_type_total_supply_gen(), self.total_supply_opc_line_gen())
        return fun

    def max_supply_fun_gen(self):
        fun = self.a_function_gen(self.max_supply_fun_id_gen(), self.max_supply_fun_type_gen(), self.proto_type_max_supply_gen(), self.max_supply_opc_line_gen())
        return fun

    def max_supply_fun_without_split_gen(self):
        fun = self.a_function_gen(self.max_supply_fun_id_without_split_gen(), self.max_supply_fun_type_gen(), self.proto_type_max_supply_gen(), self.max_supply_opc_line_gen())
        return fun

    def balance_of_fun_gen(self):
        fun = self.a_function_gen(self.balance_of_fun_id_gen(), self.balance_of_fun_type_gen(), self.proto_type_balance_of_gen(), self.balance_of_opc_line_gen())
        return fun

    def balance_of_fun_without_split_gen(self):
        fun = self.a_function_gen(self.balance_of_fun_id_without_split_gen(), self.balance_of_fun_type_gen(), self.proto_type_balance_of_gen(), self.balance_of_opc_line_gen())
        return fun

    def get_issuer_fun_gen(self):
        fun = self.a_function_gen(self.get_issuer_fun_id_gen(), self.get_issuer_fun_type_gen(), self.proto_type_get_issuer_gen(), self.get_issuer_opc_line_gen())
        return fun

    def get_issuer_fun_without_split_gen(self):
        fun = self.a_function_gen(self.get_issuer_fun_id_without_split_gen(), self.get_issuer_fun_type_gen(), self.proto_type_get_issuer_gen(), self.get_issuer_opc_line_gen())
        return fun

    # funid
    def init_fun_id_gen(self):
        return struct.pack(">H", self.init)
    def supersede_fun_id_gen(self):
        return struct.pack(">H", self.supersede)
    def supersede_fun_id_without_split_gen(self):
        return struct.pack(">H", self.supersede_without_split)
    def issue_fun_id_gen(self):
        return struct.pack(">H", self.issue)
    def issue_fun_id_without_split_gen(self):
        return struct.pack(">H", self.issue_without_split)
    def destroy_fun_id_gen(self):
        return struct.pack(">H", self.destroy)
    def destroy_fun_id_without_split_gen(self):
        return struct.pack(">H", self.destroy_without_split)
    def split_fun_id_gen(self):
        return struct.pack(">H", self.split)
    def send_fun_id_gen(self):
        return struct.pack(">H", self.send)
    def send_fun_id_without_split_gen(self):
        return struct.pack(">H", self.send_without_split)
    def transfer_fun_id_gen(self):
        return struct.pack(">H", self.transfer)
    def transfer_fun_id_without_split_gen(self):
        return struct.pack(">H", self.transfer_without_split)
    def deposit_fun_id_gen(self):
        return struct.pack(">H", self.deposit)
    def deposit_fun_id_without_split_gen(self):
        return struct.pack(">H", self.deposit_without_split)
    def withdraw_fun_id_gen(self):
        return struct.pack(">H", self.withdraw)
    def withdraw_fun_id_without_split_gen(self):
        return struct.pack(">H", self.withdraw_without_split)
    def total_supply_fun_id_gen(self):
        return struct.pack(">H", self.total_supply)
    def total_supply_fun_id_without_split_gen(self):
        return struct.pack(">H", self.total_supply_without_split)
    def max_supply_fun_id_gen(self):
        return struct.pack(">H", self.max_supply)
    def max_supply_fun_id_without_split_gen(self):
        return struct.pack(">H", self.max_supply_without_split)
    def balance_of_fun_id_gen(self):
        return struct.pack(">H", self.balance_of)
    def balance_of_fun_id_without_split_gen(self):
        return struct.pack(">H", self.balance_of_without_split)
    def get_issuer_fun_id_gen(self):
        return struct.pack(">H", self.get_issuer)
    def get_issuer_fun_id_without_split_gen(self):
        return struct.pack(">H", self.get_issuer_without_split)

    # funtype
    def init_fun_type_gen(self):
        return bytes([self.on_init_trigger_type])
    def supersede_fun_type_gen(self):
        return bytes([self.public_func_type])
    def issue_fun_type_gen(self):
        return bytes([self.public_func_type])
    def destroy_fun_type_gen(self):
        return bytes([self.public_func_type])
    def split_fun_type_gen(self):
        return bytes([self.public_func_type])
    def send_fun_type_gen(self):
        return bytes([self.public_func_type])
    def transfer_fun_type_gen(self):
        return bytes([self.public_func_type])
    def deposit_fun_type_gen(self):
        return bytes([self.public_func_type])
    def withdraw_fun_type_gen(self):
        return bytes([self.public_func_type])
    def total_supply_fun_type_gen(self):
        return bytes([self.public_func_type])
    def max_supply_fun_type_gen(self):
        return bytes([self.public_func_type])
    def balance_of_fun_type_gen(self):
        return bytes([self.public_func_type])
    def get_issuer_fun_type_gen(self):
        return bytes([self.public_func_type])

    # prototype
    def proto_type_gen(self, return_type, list_para_types):
        proto_type = deser.serialize_array(return_type) + deser.serialize_array(list_para_types)
        return proto_type

    def init_para_type_wrong(self):
        return [self.amount, self.amount]

    def init_para_type(self):
        return [self.amount, self.amount, self.short_text]

    def supersede_para_type(self):
        return [self.account]

    def issue_para_type(self):
        return [self.amount]

    def destroy_para_type(self):
        return [self.amount]

    def split_para_type(self):
        return [self.amount]

    def send_para_type(self):
        return [self.account, self.amount]

    def transfer_para_type(self):
        return [self.account, self.account, self.amount]

    def deposit_para_type(self):
        return [self.account, self.contract_account, self.amount]

    def withdraw_para_type(self):
        return [self.contract_account, self.account, self.amount]

    def total_supply_para_type(self):
        return bytes('', encoding='utf-8')

    def max_supply_para_type(self):
        return bytes('', encoding='utf-8')

    def balance_of_para_type(self):
        return [self.account]

    def get_issuer_para_type(self):
        return bytes('', encoding='utf-8')

    def proto_type_init_wrong_gen(self):
        return self.proto_type_gen(self.non_return_type, self.init_para_type_wrong())

    def proto_type_init_gen(self):
        return self.proto_type_gen(self.non_return_type, self.init_para_type())

    def proto_type_supersede_gen(self):
        return self.proto_type_gen(self.non_return_type, self.supersede_para_type())

    def proto_type_issue_gen(self):
        return self.proto_type_gen(self.non_return_type, self.issue_para_type())

    def proto_type_destroy_gen(self):
        return self.proto_type_gen(self.non_return_type, self.destroy_para_type())

    def proto_type_split_gen(self):
        return self.proto_type_gen(self.non_return_type, self.split_para_type())

    def proto_type_send_gen(self):
        return self.proto_type_gen(self.non_return_type, self.send_para_type())

    def proto_type_transfer_gen(self):
        return self.proto_type_gen(self.non_return_type, self.transfer_para_type())

    def proto_type_deposit_gen(self):
        return self.proto_type_gen(self.non_return_type, self.deposit_para_type())

    def proto_type_withdraw_gen(self):
        return self.proto_type_gen(self.non_return_type, self.withdraw_para_type())

    def proto_type_total_supply_gen(self):
        return self.proto_type_gen([self.amount], self.total_supply_para_type())

    def proto_type_max_supply_gen(self):
        return self.proto_type_gen([self.amount], self.max_supply_para_type())

    def proto_type_balance_of_gen(self):
        return self.proto_type_gen([self.amount], self.balance_of_para_type())

    def proto_type_get_issuer_gen(self):
        return self.proto_type_gen([self.account], self.get_issuer_para_type())


    # listopc
    def list_opc_gen(self, ids, index_input):
        length = struct.pack(">H", sum(list(map(lambda x: len(x[0]+x[1])+2, list(zip(ids, index_input))))) + 2)
        num_opc = struct.pack(">H", len(ids))
        list_opc = bytes(itertools.chain.from_iterable(list(map(lambda x: struct.pack(">H",len(x[0]+x[1]))+x[0]+x[1], list(zip(ids, index_input))))))
        len_list_opc = length + num_opc + list_opc
        return len_list_opc


    def init_opc_line_wrong_tdb_gen(self):
        return self.list_opc_gen(self.init_wrong_tdb_opc(), self.init_opc_index())

    def init_opc_line_gen(self):
        return self.list_opc_gen(self.init_opc(), self.init_opc_index())

    def supersede_opc_line_gen(self):
        return self.list_opc_gen(self.supersede_opc(), self.supersede_opc_index())

    def issue_opc_line_gen(self):
        return self.list_opc_gen(self.issue_opc(), self.issue_opc_index())

    def destroy_opc_line_gen(self):
        return self.list_opc_gen(self.destroy_opc(), self.destroy_opc_index())

    def split_opc_line_gen(self):
        return self.list_opc_gen(self.split_opc(), self.split_opc_index())

    def send_opc_line_gen(self):
        return self.list_opc_gen(self.send_opc(), self.send_opc_index())

    def transfer_opc_line_gen(self):
        return self.list_opc_gen(self.transfer_opc(), self.transfer_opc_index())

    def deposit_opc_line_gen(self):
        return self.list_opc_gen(self.deposit_opc(), self.deposit_opc_index())

    def withdraw_opc_line_gen(self):
        return self.list_opc_gen(self.withdraw_opc(), self.withdraw_opc_index())

    def total_supply_opc_line_gen(self):
        return self.list_opc_gen(self.total_supply_opc(), self.total_supply_opc_index())

    def max_supply_opc_line_gen(self):
        return self.list_opc_gen(self.max_supply_opc(), self.max_supply_opc_index())

    def balance_of_opc_line_gen(self):
        return self.list_opc_gen(self.balance_of_opc(), self.balance_of_opc_index())

    def get_issuer_opc_line_gen(self):
        return self.list_opc_gen(self.get_issuer_opc(), self.get_issuer_opc_index())

    def opc_load_signer_index(self):
        return bytes([3])

    def opc_load_caller_index(self):
        return bytes([2])

    def init_opc_cdbv_set_signer_index(self):
        return self.state_var_issuer + self.init_input_issuer_load_index

    def init_opc_cdbv_set_maker_index(self):
        return self.state_var_maker + self.init_input_issuer_load_index

    def init_opc_tdb_new_token_index(self):
        return self.init_input_max_index + self.init_input_unity_index + self.init_input_short_text_index

    def init_wrong_tdb_opc(self):
        return [self.opc_load_signer(), self.opc_cdbv_set(), self.opc_cdbv_set(), bytes([5]), bytes([3])]

    def init_opc(self):
        return [self.opc_load_signer(), self.opc_cdbv_set(), self.opc_cdbv_set(), self.opc_tdb_new_token()]

    def init_opc_index(self):
        return [self.opc_load_signer_index(), self.init_opc_cdbv_set_signer_index(), self.init_opc_cdbv_set_maker_index(), self.init_opc_tdb_new_token_index()]

    def supersede_opc_cdbvr_get_index(self):
        return self.state_var_maker + bytes([1])

    def supersede_assert_is_signer_origin_index(self):
        return self.supersede_input_maker

    def supersede_opc_cdbv_set_index(self):
        return self.state_var_issuer + self.supersede_input_new_issuer_index

    def supersede_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_signer_origin(), self.opc_cdbv_set()]

    def supersede_opc_index(self):
        return [self.supersede_opc_cdbvr_get_index(), self.supersede_assert_is_signer_origin_index(), self.supersede_opc_cdbv_set_index()]

    def issue_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([1])

    def issue_opc_assert_is_caller_origin_index(self):
        return self.issue_input_issuer_get_index

    def issue_opc_tdba_deposit_index(self):
        return self.issue_input_issuer_get_index + self.issue_input_amount_index

    def issue_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdba_deposit()]

    def issue_opc_index(self):
        return [self.issue_opc_cdbvr_get_index(), self.issue_opc_assert_is_caller_origin_index(), self.issue_opc_tdba_deposit_index()]

    def destroy_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([1])

    def destroy_opc_assert_is_caller_origin_index(self):
        return self.destroy_input_issuer_get_index

    def destroy_opc_tdba_withdraw_index(self):
        return self.destroy_input_issuer_get_index + self.destroy_input_destroy_amount_index

    def destroy_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdba_withdraw()]

    def destroy_opc_index(self):
        return [self.destroy_opc_cdbvr_get_index(), self.destroy_opc_assert_is_caller_origin_index(), self.destroy_opc_tdba_withdraw_index()]

    def split_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([1])

    def split_opc_assert_is_caller_origin_index(self):
        return self.split_input_issuer_get_index

    def split_opc_tdb_split_index(self):
        return self.split_input_new_unity_index

    def split_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdb_split()]

    def split_opc_index(self):
        return [self.split_opc_cdbvr_get_index(), self.split_opc_assert_is_caller_origin_index(), self.split_opc_tdb_split_index()]

    def send_opc_tdba_transfer_index(self):
        return self.send_input_sender_index + self.send_input_recipient_index + self.send_input_amount_index

    def send_opc(self):
        return [self.opc_load_caller(), self.opc_tdba_transfer()]

    def send_opc_index(self):
        return [self.opc_load_caller_index(), self.send_opc_tdba_transfer_index()]

    def transfer_opc_assert_is_caller_origin_index(self):
        return self.transfer_input_sender_index

    def transfer_opc_tdba_transfer_index(self):
        return self.transfer_input_sender_index + self.transfer_input_recipient_index + self.transfer_input_amount_index

    def transfer_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def transfer_opc_index(self):
        return [self.transfer_opc_assert_is_caller_origin_index(), self.transfer_opc_tdba_transfer_index()]

    def deposit_opc_assert_is_caller_origin_index(self):
        return self.deposit_input_sender_index

    def deposit_opc_tdba_transfer_index(self):
        return self.deposit_input_sender_index + self.deposit_input_smart_contract_index + self.deposit_input_amount_index

    def deposit_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def deposit_opc_index(self):
        return [self.deposit_opc_assert_is_caller_origin_index(), self.deposit_opc_tdba_transfer_index()]

    def withdraw_opc_assert_is_caller_origin_index(self):
        return self.withdraw_input_recipient_index

    def withdraw_opc_tdba_transfer_index(self):
        return self.withdraw_input_smart_contract_index + self.withdraw_input_recipient_index + self.withdraw_input_amount_index

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
        return self.balance_of_input_account_index + bytes([1])

    def balance_of_opc(self):
        return [self.opc_tdbar_balance(), self.opc_return_value()]

    def balance_of_opc_index(self):
        return [self.balance_of_opc_tdbar_balance_index(), bytes([1])]

    def get_issuer_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([0])

    def get_issuer_opc(self):
        return [self.opc_cdbvr_get(), self.opc_return_value()]

    def get_issuer_opc_index(self):
        return [self.get_issuer_opc_cdbvr_get_index(), bytes([0])]

    # datastack
    def init_data_stack_gen(self, amount, unity, desc):

        max = DataEntry(bytes([amount]), self.amount)
        unit = DataEntry(bytes([unity]), self.amount)
        short_text = DataEntry.create(desc.getBytes(), self.short_text)
        return [max, unit, short_text]

    def supersede_data_stack_gen(self, new_issuer):
        iss = DataEntry(new_issuer.bytes.arr, self.address)
        return iss

    def split_data_stack_gen(self, new_unity, token_index):
        unit = DataEntry(bytes([new_unity]), self.amount)
        index =   DataEntry(bytes([token_index]), self.int32)
        return [unit, index]

    def destroy_data_stack_gen(self, amount, token_index):
        am = DataEntry(bytes([amount]), self.amount)
        index = DataEntry(bytes([token_index]), self.int32)
        return [am, index]

    def issue_data_stack_gen(self, amount, token_index):
        max = DataEntry(bytes([amount]), self.amount)
        index = DataEntry(bytes([token_index]), self.int32)
        return [max, index]

    def send_data_stack_gen(self, recipient, amount, token_index):
        reci = DataEntry(recipient.bytes.arr, self.address)
        am = DataEntry(bytes([amount]), self.amount)
        index = DataEntry(bytes([token_index]), self.int32)
        return [reci, am, index]

    def transfer_data_stack_gen(self, sender, recipient, amount, token_index):
        se = DataEntry(sender.bytes.arr, self.address)
        reci = DataEntry(recipient.bytes.arr, self.address)
        am = DataEntry(bytes([amount]), self.amount)
        index = DataEntry(bytes([token_index]), self.int32)
        return [se, reci, am, index]

    def deposit_data_stack_gen(self, sender, smart_contract, amount, token_index):
        se = DataEntry(sender.bytes.arr, self.address)
        sc = DataEntry(smart_contract.bytes.arr, self.address)
        am = DataEntry(bytes([amount]), self.amount)
        index = DataEntry(bytes([token_index]), self.int32)
        return [se, sc, am, index]

    def withdraw_data_stack_gen(self, smart_contract, recipient, amount, token_index):
        sc = DataEntry(smart_contract.bytes.arr, self.address)
        reci = DataEntry(recipient.bytes.arr, self.address)
        am = DataEntry(bytes([amount]), self.amount)
        index = DataEntry(bytes([token_index]), self.int32)
        return [sc, reci, am, index]

    def total_supply_data_stack_gen(self, token_index):
        index = DataEntry(bytes([token_index]), self.int32)
        return [index]

    def max_supply_data_stack_gen(self, token_index):
        index = DataEntry(bytes([token_index]), self.int32)
        return [index]

    def balance_of_data_stack_gen(self, account, token_index):
        acc =  DataEntry(account.bytes.arr, self.address)
        index = DataEntry(bytes([token_index]), self.int32)
        return [acc, index]
