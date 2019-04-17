import sys
import copy


class Opcode(object):
    def __init__(self):
        self.function_name = {'0106': 'opc_assert_caller', '0107': 'opc_assert_singer',
                              '0201': 'opc_load_env_signer', '0202': 'opc_load_env_caller',
                              '0301': 'opc_cdbv_set', '0401': 'opc_cdbvr_get', '0501': 'opc_tdb_new',
                              '0601': 'opc_tdbr_get', '0602': 'opc_tdbr_total', '0701': 'opc_tdba_deposit',
                              '0702': 'opc_tdba_withdraw', '0703': 'opc_tdba_transfer', '0801': 'opc_tdbar_balance',
                              '0900': 'opc_return_last'}

    @staticmethod
    def opc_assert_caller(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + name_list[data[2]])
        return name_list

    @staticmethod
    def opc_assert_singer(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + name_list[data[2]])
        return name_list

    @staticmethod
    def opc_load_env_caller(arg):
        local_variable = ['caller']
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + local_variable[0])
        return name_list + local_variable

    @staticmethod
    def opc_load_env_signer(arg):
        local_variable = ['singer']
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + local_variable[0])
        return name_list + local_variable

    @staticmethod
    def opc_cdbv_set(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        state_var = copy.deepcopy(arg[2])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + 'db.', end='')
        print(state_var[data[2]][0] + ' ', end='')
        print(name_list[data[3]])
        return name_list

    @staticmethod
    def opc_cdbvr_get(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        state_var = copy.deepcopy(arg[2])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + 'db.', end='')
        print(state_var[data[2]][0] + ' ' + state_var[data[2]][0])
        return name_list + state_var[data[2]]

    @staticmethod
    def opc_tdb_new(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ', end='')
        print(name_list[data[6]] + ' ' + name_list[data[7]] + ' ' + name_list[data[8]])
        return name_list

    @staticmethod
    def opc_tdbr_get(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        state_var = copy.deepcopy(arg[2])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + 'tdb.', end='')
        print(state_var[data[2]][0] + ' ' + name_list[data[3]] + ' ' + state_var[data[2]][0])
        return name_list + state_var[data[2]]

    @staticmethod
    def opc_tdbr_total(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        state_var = copy.deepcopy(arg[2])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ' + 'tdb.', end='')
        print(state_var[data[2]][0] + ' ' + name_list[data[3]] + ' ' + state_var[data[2]][0])
        return name_list + state_var[data[2]]

    @staticmethod
    def opc_tdba_deposit(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ', end='')
        print(name_list[data[4]] + ' ' + name_list[data[5]] + ' ' + name_list[data[6]])
        return name_list

    @staticmethod
    def opc_tdba_withdraw(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ', end='')
        print(name_list[data[3]] + ' ' + name_list[data[4]] + ' ' + name_list[data[5]])
        return name_list

    @staticmethod
    def opc_tdba_transfer(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ', end='')
        print(name_list[data[2]] + ' ' + name_list[data[3]] + ' ' + name_list[data[4]] + ' ' + name_list[data[5]])
        return name_list

    @staticmethod
    def opc_tdbar_balance(arg):
        local_variable = ['balance']
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ', end='')
        print(name_list[data[2]] + ' ' + name_list[data[3]] + ' ' + local_variable[0])
        return name_list + local_variable

    @staticmethod
    def opc_return_last(arg):
        name_list = copy.deepcopy(arg[1])
        function_name = sys._getframe().f_code.co_name
        print(function_name + ' ', end='')
        print(name_list[-1])
        return name_list

    def get_opc(self, arg, arg_outside):
        return getattr(self, arg)(arg_outside)
