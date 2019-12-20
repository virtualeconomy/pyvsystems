import itertools
import logging
import struct

from .deser import serialize_string, serialize_array, serialize_arrays
from .contract_meta import ContractMeta as meta

from .crypto import *


data_type_list = {value: bytes([int(key)]) for key, value in meta.data_type_list.items()}
function_type_map = {value: bytes([int(key[1:])]) for key, value in meta.function_type_map.items()}

def opc_assert_is_caller_origin():
    return meta.assert_opc + meta.is_caller_origin_assert

def opc_assert_is_signer_origin():
    return meta.assert_opc + meta.is_signer_origin_assert

def opc_load_signer():
    return meta.load_opc + meta.signer_load

def opc_load_caller():
    return meta.load_opc + meta.caller_load

def opc_cdbv_set():
    return meta.cdbv_opc + meta.set_cdbv

def opc_cdbvr_get():
    return meta.cdbvr_opc + meta.get_cdbvr

def opc_tdb_new_token():
    return meta.tdb_opc + meta.new_token_tdb

def opc_tdb_split():
    return meta.tdb_opc + meta.split_tdb

def opc_tdbr_opc_max():
    return meta.tdbr_opc + meta.get_tdbr

def opc_tdbr_opc_total():
    return meta.tdbr_opc + meta.total_tdbr

def opc_tdba_deposit():
    return meta.tdba_opc + meta.deposit_tdba

def opc_tdba_withdraw():
    return meta.tdba_opc + meta.withdraw_tdba

def opc_tdba_transfer():
    return meta.tdba_opc + meta.transfer_tdba

def opc_tdbar_balance():
    return meta.tdbar_opc + meta.balance_tdbar

def opc_return_value():
    return meta.return_opc + bytes([1])

def language_code_builder(code):
    if len(code) == meta.language_code_byte_length:
        language_code = serialize_string(code)
        return language_code
    else:
        logging.error("Wrong language code length")
        raise Exception("Wrong language code length")

def language_version_builder(version):
    try:
        if len(struct.pack(">I", version)) == meta.language_version_byte_length:
            return struct.pack(">I", version)
        else:
            logging.error("Wrong language version length")
            raise Exception("Wrong language code length")
    except:
        print("Wrong language version length")


def bytes_builder_from_list(input_list):
    if type(input_list) is list:
        return serialize_array(serialize_arrays(input_list))
    else:
        logging.error("The input should be a list")

def textual_fun_gen(name, ret, para):
    func_byte = serialize_array(serialize_string(name))
    ret_byte = serialize_array(serialize_arrays([serialize_string(r) for r in ret]))
    para_byte = serialize_arrays([serialize_string(p) for p in para])
    textual = func_byte + ret_byte + para_byte
    return textual

def init_func_bytes():
    return textual_fun_gen("init", [], meta.init_para)

def supersede_func_bytes():
    return textual_fun_gen("supersede", [], meta.supersede_para)

def issue_func_bytes():
    return textual_fun_gen("issue", [], meta.issue_para)

def destroy_func_bytes():
    return textual_fun_gen("destroy", [], meta.destroy_para)

def split_func_bytes():
    return textual_fun_gen("split", [], meta.split_para)

def send_func_bytes():
    return textual_fun_gen("send", [], meta.send_para)

def transfer_func_bytes():
    return textual_fun_gen("transfer", [], meta.transfer_para)

def deposit_func_bytes():
    return textual_fun_gen("deposit", [], meta.deposit_para)

def withdraw_func_bytes():
    return textual_fun_gen("withdraw", [], meta.withdraw_para)

def total_supply_func_bytes():
    return textual_fun_gen("totalSupply", ["total"], meta.total_supply_para)

def max_supply_func_bytes():
    return textual_fun_gen("maxSupply", ["max"], meta.max_supply_para)

def balance_of_func_bytes():
    return textual_fun_gen("balanceOf", ["balance"], meta.balance_of_para)

def get_issuer_func_bytes():
    return textual_fun_gen("getIssuer", ["issuer"], meta.get_issuer_para)


def state_var_random_gen():
    fixed_size = 2
    state_var = bytearray(os.urandom(fixed_size))
    return state_var

def state_var_gen(state_vars):
    state_vars = serialize_arrays(state_vars)
    return state_vars

def a_function_gen(fun_idx, fun_type, proto_type, list_opc):
    fun = fun_idx + fun_type + proto_type + list_opc
    return fun

def init_fun_gen():
    fun = a_function_gen(init_fun_id_gen(), function_type_map.get("onInit"), proto_type_gen(meta.non_return_type, init_para_type()), list_opc_gen(init_opc(), init_opc_index()))
    return fun

def supersede_fun_gen():
    fun = a_function_gen(supersede_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, supersede_para_type()), list_opc_gen(supersede_opc(), supersede_opc_index()))
    return fun

def supersede_fun_without_split_gen():
    fun = a_function_gen(supersede_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, supersede_para_type()), list_opc_gen(supersede_opc(), supersede_opc_index()))
    return fun

def issue_fun_gen():
    fun = a_function_gen(issue_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, issue_para_type()), list_opc_gen(issue_opc(), issue_opc_index()))
    return fun

def issue_fun_without_split_gen():
    fun = a_function_gen(issue_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, issue_para_type()), list_opc_gen(issue_opc(), issue_opc_index()))
    return fun

def destroy_fun_gen():
    fun = a_function_gen(destroy_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, destroy_para_type()), list_opc_gen(destroy_opc(), destroy_opc_index()))
    return fun

def destroy_fun_without_split_gen():
    fun = a_function_gen(destroy_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, destroy_para_type()), list_opc_gen(destroy_opc(), destroy_opc_index()))
    return fun

def split_fun_gen():
    fun = a_function_gen(split_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, split_para_type()), list_opc_gen(split_opc(), split_opc_index()))
    return fun

def send_fun_gen():
    fun = a_function_gen(send_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, send_para_type()), list_opc_gen(send_opc(), send_opc_index()))
    return fun

def send_fun_without_split_gen():
    fun = a_function_gen(send_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, send_para_type()), list_opc_gen(send_opc(), send_opc_index()))
    return fun

def transfer_fun_gen():
    fun = a_function_gen(transfer_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, transfer_para_type()), list_opc_gen(transfer_opc(), transfer_opc_index()))
    return fun

def transfer_fun_without_split_gen():
    fun = a_function_gen(transfer_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, transfer_para_type()), list_opc_gen(transfer_opc(), transfer_opc_index()))
    return fun

def deposit_fun_gen():
    fun = a_function_gen(deposit_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, deposit_para_type()), list_opc_gen(deposit_opc(), deposit_opc_index()))
    return fun

def deposit_fun_without_split_gen():
    fun = a_function_gen(deposit_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, deposit_para_type()), list_opc_gen(deposit_opc(), deposit_opc_index()))
    return fun

def withdraw_fun_gen():
    fun = a_function_gen(withdraw_fun_id_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, withdraw_para_type()), list_opc_gen(withdraw_opc(), withdraw_opc_index()))
    return fun

def withdraw_fun_without_split_gen():
    fun = a_function_gen(withdraw_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen(meta.non_return_type, withdraw_para_type()), list_opc_gen(withdraw_opc(), withdraw_opc_index()))
    return fun

def total_supply_fun_gen():
    fun = a_function_gen(total_supply_fun_id_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Amount')], total_supply_para_type()), list_opc_gen(total_supply_opc(), total_supply_opc_index()))
    return fun

def total_supply_fun_without_split_gen():
    fun = a_function_gen(total_supply_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Amount')], total_supply_para_type()), list_opc_gen(total_supply_opc(), total_supply_opc_index()))
    return fun

def max_supply_fun_gen():
    fun = a_function_gen(max_supply_fun_id_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Amount')], max_supply_para_type()), list_opc_gen(max_supply_opc(), max_supply_opc_index()))
    return fun

def max_supply_fun_without_split_gen():
    fun = a_function_gen(max_supply_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Amount')], max_supply_para_type()), list_opc_gen(max_supply_opc(), max_supply_opc_index()))
    return fun

def balance_of_fun_gen():
    fun = a_function_gen(balance_of_fun_id_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Amount')], balance_of_para_type()), list_opc_gen(balance_of_opc(), balance_of_opc_index()))
    return fun

def balance_of_fun_without_split_gen():
    fun = a_function_gen(balance_of_fun_id_without_split_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Amount')], balance_of_para_type()), list_opc_gen(balance_of_opc(), balance_of_opc_index()))
    return fun

def get_issuer_fun_gen():
    fun = a_function_gen(get_issuer_fun_id_gen(), function_type_map.get("public"), proto_type_gen([data_type_list.get('Account')], get_issuer_para_type()), list_opc_gen(get_issuer_opc(), get_issuer_opc_index()))
    return fun

def get_issuer_fun_without_split_gen():
    fun = a_function_gen(get_issuer_fun_id_without_split_gen(),function_type_map.get("public"), proto_type_gen([data_type_list.get('Account')], get_issuer_para_type()), list_opc_gen(get_issuer_opc(), get_issuer_opc_index()))
    return fun

def init_fun_id_gen():
    return struct.pack(">H", meta.init)
def supersede_fun_id_gen():
    return struct.pack(">H", meta.supersede)
def supersede_fun_id_without_split_gen():
    return struct.pack(">H", meta.supersede_without_split)
def issue_fun_id_gen():
    return struct.pack(">H", meta.issue)
def issue_fun_id_without_split_gen():
    return struct.pack(">H", meta.issue_without_split)
def destroy_fun_id_gen():
    return struct.pack(">H", meta.destroy)
def destroy_fun_id_without_split_gen():
    return struct.pack(">H", meta.destroy_without_split)
def split_fun_id_gen():
    return struct.pack(">H", meta.split)
def send_fun_id_gen():
    return struct.pack(">H", meta.send)
def send_fun_id_without_split_gen():
    return struct.pack(">H", meta.send_without_split)
def transfer_fun_id_gen():
    return struct.pack(">H", meta.transfer)
def transfer_fun_id_without_split_gen():
    return struct.pack(">H", meta.transfer_without_split)
def deposit_fun_id_gen():
    return struct.pack(">H", meta.deposit)
def deposit_fun_id_without_split_gen():
    return struct.pack(">H", meta.deposit_without_split)
def withdraw_fun_id_gen():
    return struct.pack(">H", meta.withdraw)
def withdraw_fun_id_without_split_gen():
    return struct.pack(">H", meta.withdraw_without_split)
def total_supply_fun_id_gen():
    return struct.pack(">H", meta.total_supply)
def total_supply_fun_id_without_split_gen():
    return struct.pack(">H", meta.total_supply_without_split)
def max_supply_fun_id_gen():
    return struct.pack(">H", meta.max_supply)
def max_supply_fun_id_without_split_gen():
    return struct.pack(">H", meta.max_supply_without_split)
def balance_of_fun_id_gen():
    return struct.pack(">H", meta.balance_of)
def balance_of_fun_id_without_split_gen():
    return struct.pack(">H", meta.balance_of_without_split)
def get_issuer_fun_id_gen():
    return struct.pack(">H", meta.get_issuer)
def get_issuer_fun_id_without_split_gen():
    return struct.pack(">H", meta.get_issuer_without_split)


def proto_type_gen(return_type, list_para_types):
    proto_type = serialize_array(return_type) + serialize_array(list_para_types)
    return proto_type

def init_para_type_wrong():
    return [data_type_list.get('Amount'), data_type_list.get('Amount')]

def init_para_type():
    return [data_type_list.get('Amount'), data_type_list.get('Amount'), data_type_list.get('ShortText')]

def supersede_para_type():
    return [data_type_list.get('Account')]

def issue_para_type():
    return [data_type_list.get('Amount')]

def destroy_para_type():
    return [data_type_list.get('Amount')]

def split_para_type():
    return [data_type_list.get('Amount')]

def send_para_type():
    return [data_type_list.get('Account'), data_type_list.get('Amount')]

def transfer_para_type():
    return [data_type_list.get('Account'), data_type_list.get('Account'), data_type_list.get('Amount')]

def deposit_para_type():
    return [data_type_list.get('Account'), data_type_list.get('ContractAccount'), data_type_list.get('Amount')]

def withdraw_para_type():
    return [data_type_list.get('ContractAccount'), data_type_list.get('Account'), data_type_list.get('Amount')]

def total_supply_para_type():
    return no_return_bytes

def max_supply_para_type():
    return no_return_bytes

def balance_of_para_type():
    return [data_type_list.get('Account')]

def get_issuer_para_type():
    return no_return_bytes


def list_opc_gen(ids, index_input):
    length = struct.pack(">H", sum(list(map(lambda x: len(x[0]+x[1])+2, list(zip(ids, index_input))))) + 2)
    num_opc = struct.pack(">H", len(ids))
    list_opc = bytes(itertools.chain.from_iterable(list(map(lambda x: struct.pack(">H",len(x[0]+x[1]))+x[0]+x[1], list(zip(ids, index_input))))))
    len_list_opc = length + num_opc + list_opc
    return len_list_opc


def opc_load_signer_index():
    return bytes([3])

def opc_load_caller_index():
    return bytes([2])

def init_opc_cdbv_set_signer_index():
    return meta.state_var_issuer + meta.init_input_issuer_load_index

def init_opc_cdbv_set_maker_index():
    return meta.state_var_maker + meta.init_input_issuer_load_index

def init_opc_tdb_new_token_index():
    return meta.init_input_max_index + meta.init_input_unity_index + meta.init_input_short_text_index

def init_wrong_tdb_opc():
    return [opc_load_signer(), opc_cdbv_set(), opc_cdbv_set(), bytes([5]), bytes([3])]

def init_opc():
    return [opc_load_signer(), opc_cdbv_set(), opc_cdbv_set(), opc_tdb_new_token()]

def init_opc_index():
    return [opc_load_signer_index(), init_opc_cdbv_set_signer_index(), init_opc_cdbv_set_maker_index(), init_opc_tdb_new_token_index()]

def supersede_opc_cdbvr_get_index():
    return meta.state_var_maker + bytes([1])

def supersede_assert_is_signer_origin_index():
    return meta.supersede_input_maker

def supersede_opc_cdbv_set_index():
    return meta.state_var_issuer + meta.supersede_input_new_issuer_index

def supersede_opc():
    return [opc_cdbvr_get(), opc_assert_is_signer_origin(), opc_cdbv_set()]

def supersede_opc_index():
    return [supersede_opc_cdbvr_get_index(), supersede_assert_is_signer_origin_index(), supersede_opc_cdbv_set_index()]

def issue_opc_cdbvr_get_index():
    return meta.state_var_issuer + bytes([1])

def issue_opc_assert_is_caller_origin_index():
    return meta.issue_input_issuer_get_index

def issue_opc_tdba_deposit_index():
    return meta.issue_input_issuer_get_index + meta.issue_input_amount_index

def issue_opc():
    return [opc_cdbvr_get(), opc_assert_is_caller_origin(), opc_tdba_deposit()]

def issue_opc_index():
    return [issue_opc_cdbvr_get_index(), issue_opc_assert_is_caller_origin_index(), issue_opc_tdba_deposit_index()]

def destroy_opc_cdbvr_get_index():
    return meta.state_var_issuer + bytes([1])

def destroy_opc_assert_is_caller_origin_index():
    return meta.destroy_input_issuer_get_index

def destroy_opc_tdba_withdraw_index():
    return meta.destroy_input_issuer_get_index + meta.destroy_input_destroy_amount_index

def destroy_opc():
    return [opc_cdbvr_get(), opc_assert_is_caller_origin(), opc_tdba_withdraw()]

def destroy_opc_index():
    return [destroy_opc_cdbvr_get_index(), destroy_opc_assert_is_caller_origin_index(), destroy_opc_tdba_withdraw_index()]

def split_opc_cdbvr_get_index():
    return meta.state_var_issuer + bytes([1])

def split_opc_assert_is_caller_origin_index():
    return meta.split_input_issuer_get_index

def split_opc_tdb_split_index():
    return meta.split_input_new_unity_index

def split_opc():
    return [opc_cdbvr_get(), opc_assert_is_caller_origin(), opc_tdb_split()]

def split_opc_index():
    return [split_opc_cdbvr_get_index(), split_opc_assert_is_caller_origin_index(), split_opc_tdb_split_index()]

def send_opc_tdba_transfer_index():
    return meta.send_input_sender_index + meta.send_input_recipient_index + meta.send_input_amount_index

def send_opc():
    return [opc_load_caller(), opc_tdba_transfer()]

def send_opc_index():
    return [opc_load_caller_index(), send_opc_tdba_transfer_index()]

def transfer_opc_assert_is_caller_origin_index():
    return meta.transfer_input_sender_index

def transfer_opc_tdba_transfer_index():
    return meta.transfer_input_sender_index + meta.transfer_input_recipient_index + meta.transfer_input_amount_index

def transfer_opc():
    return [opc_assert_is_caller_origin(), opc_tdba_transfer()]

def transfer_opc_index():
    return [transfer_opc_assert_is_caller_origin_index(), transfer_opc_tdba_transfer_index()]

def deposit_opc_assert_is_caller_origin_index():
    return meta.deposit_input_sender_index

def deposit_opc_tdba_transfer_index():
    return meta.deposit_input_sender_index + meta.deposit_input_smart_contract_index + meta.deposit_input_amount_index

def deposit_opc():
    return [opc_assert_is_caller_origin(), opc_tdba_transfer()]

def deposit_opc_index():
    return [deposit_opc_assert_is_caller_origin_index(), deposit_opc_tdba_transfer_index()]

def withdraw_opc_assert_is_caller_origin_index():
    return meta.withdraw_input_recipient_index

def withdraw_opc_tdba_transfer_index():
    return meta.withdraw_input_smart_contract_index + meta.withdraw_input_recipient_index + meta.withdraw_input_amount_index

def withdraw_opc():
    return [opc_assert_is_caller_origin(), opc_tdba_transfer()]

def withdraw_opc_index():
    return [withdraw_opc_assert_is_caller_origin_index(), withdraw_opc_tdba_transfer_index()]

def total_supply_opc_tdbr_total_index():
    return bytes([0])

def total_supply_opc():
    return [opc_tdbr_opc_total(), opc_return_value()]

def total_supply_opc_index():
    return [total_supply_opc_tdbr_total_index(), bytes([0])]

def max_supply_opc_tdbr_max_index():
    return bytes([0])

def max_supply_opc():
    return [opc_tdbr_opc_max(), opc_return_value()]

def max_supply_opc_index():
    return [max_supply_opc_tdbr_max_index(), bytes([0])]

def balance_of_opc_tdbar_balance_index():
    return meta.balance_of_input_account_index + bytes([1])

def balance_of_opc():
    return [opc_tdbar_balance(), opc_return_value()]

def balance_of_opc_index():
    return [balance_of_opc_tdbar_balance_index(), bytes([1])]

def get_issuer_opc_cdbvr_get_index():
    return meta.state_var_issuer + bytes([0])

def get_issuer_opc():
    return [opc_cdbvr_get(), opc_return_value()]

def get_issuer_opc_index():
    return [get_issuer_opc_cdbvr_get_index(), bytes([0])]


class ContractDefaults:
    trigger = bytes_builder_from_list([init_fun_gen()])

    descriptor_without_split = bytes_builder_from_list(
        [supersede_fun_without_split_gen(), issue_fun_without_split_gen(),
         destroy_fun_without_split_gen(),
         send_fun_without_split_gen(), transfer_fun_without_split_gen(),
         deposit_fun_without_split_gen(), withdraw_fun_without_split_gen(),
         total_supply_fun_without_split_gen(),
         max_supply_fun_without_split_gen(), balance_of_fun_without_split_gen(),
         get_issuer_fun_without_split_gen()])

    descriptor_with_split = bytes_builder_from_list(
        [supersede_fun_gen(), issue_fun_gen(), destroy_fun_gen(), split_fun_gen(),
         send_fun_gen(),
         transfer_fun_gen(), deposit_fun_gen(), withdraw_fun_gen(), total_supply_fun_gen(),
         max_supply_fun_gen(), balance_of_fun_gen(), get_issuer_fun_gen()])

    state_var = bytes_builder_from_list([meta.state_var_issuer + data_type_list.get('Address'), meta.state_var_maker + data_type_list.get('Address')])

    state_var_textual = serialize_arrays([serialize_string(name) for name in meta.state_var_name])
    initializer_textual = serialize_arrays([init_func_bytes()])

    descriptor_textual_without_split = serialize_arrays([supersede_func_bytes(),
                                                      issue_func_bytes(),
                                                      destroy_func_bytes(),
                                                      send_func_bytes(),
                                                      transfer_func_bytes(),
                                                      deposit_func_bytes(),
                                                      withdraw_func_bytes(),
                                                      total_supply_func_bytes(),
                                                      max_supply_func_bytes(),
                                                      balance_of_func_bytes(),
                                                      get_issuer_func_bytes()])

    descriptor_textual_with_split = serialize_arrays([supersede_func_bytes(),
                                                      issue_func_bytes(),
                                                      destroy_func_bytes(),
                                                      split_func_bytes(),
                                                      send_func_bytes(),
                                                      transfer_func_bytes(),
                                                      deposit_func_bytes(),
                                                      withdraw_func_bytes(),
                                                      total_supply_func_bytes(),
                                                      max_supply_func_bytes(),
                                                      balance_of_func_bytes(),
                                                      get_issuer_func_bytes()])

    textual_without_split = serialize_arrays([initializer_textual, descriptor_textual_without_split, state_var_textual])
    textual_with_split = serialize_arrays(
        [initializer_textual, descriptor_textual_with_split, state_var_textual])


