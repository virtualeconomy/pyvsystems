from __future__ import print_function
import copy


class Opcode(object):
    def __init__(self):
        self.function_name = {'0106': 'opc_assert_caller', '0107': 'opc_assert_singer',
                              '0201': 'opc_load_env_signer', '0202': 'opc_load_env_caller',
                              '0301': 'opc_cdbv_set', '0401': 'opc_cdbvr_get', '0501': 'opc_tdb_new',
                              '0502': 'opc_tdb_split', '0601': 'opc_tdbr_max', '0602': 'opc_tdbr_total',
                              '0701': 'opc_tdba_deposit', '0702': 'opc_tdba_withdraw', '0703': 'opc_tdba_transfer',
                              '0801': 'opc_tdbar_balance', '0901': 'opc_value_return'}

    @staticmethod
    def opc_assert_caller(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.check.assertCaller' + '(' + name_list[data[2]] + ')')

    @staticmethod
    def opc_assert_singer(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.check.assertSigner' + '(' + name_list[data[2]] + ')')

    @staticmethod
    def opc_load_env_caller(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print(name_list[data[2]] + ' = ' + 'operation.env.getCaller' + '()')

    @staticmethod
    def opc_load_env_signer(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print(name_list[data[2]] + ' = ' + 'operation.env.getSigner' + '()')

    @staticmethod
    def opc_cdbv_set(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        state_var = copy.deepcopy(arg[2])
        print('operation.db.setVariable(' + 'db.' + state_var[data[2]][1] + ', ' + name_list[data[3]] + ')')

    @staticmethod
    def opc_cdbvr_get(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        state_var = copy.deepcopy(arg[2])
        print(name_list[data[3]] + ' = ' + 'operation.db.getVariable' + '(db.' + state_var[data[2]][1] + ')')

    @staticmethod
    def opc_tdb_new(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.token.new', end='')
        print('(' + name_list[data[2]] + ', ' + name_list[data[3]] + ', ' + name_list[data[4]] + ')')

    @staticmethod
    def opc_tdb_split(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.token.split', end='')
        print('(' + name_list[data[2]] + ')')

    @staticmethod
    def opc_tdbr_max(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print(name_list[data[2]] + ' = ' + 'operation.token.getMaxSupply' + '()')

    @staticmethod
    def opc_tdbr_total(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print(name_list[data[2]] + ' = ' + 'operation.token.getTotalSupply' + '()')

    @staticmethod
    def opc_tdba_deposit(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.token.deposit', end='')
        print('(' + name_list[data[2]] + ', ' + name_list[data[3]] + ')')

    @staticmethod
    def opc_tdba_withdraw(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.token.withdraw', end='')
        print('(' + name_list[data[2]] + ', ' + name_list[data[3]] + ')')

    @staticmethod
    def opc_tdba_transfer(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print('operation.token.transfer', end='')
        print('(' + name_list[data[2]] + ', ' + name_list[data[3]] + ', '
              + name_list[data[4]] + ')')

    @staticmethod
    def opc_tdbar_balance(arg):
        data = copy.deepcopy(arg[0])
        name_list = copy.deepcopy(arg[1])
        print(name_list[data[3]] + ' = ' + 'operation.token.getBalance', end='')
        print('(' + name_list[data[2]] + ')')

    @staticmethod
    def opc_value_return(arg):
        name_list = copy.deepcopy(arg[1])
        print('operation.control.return', end='')
        print('(' + name_list[-1] + ')')

    def get_opc(self, arg, arg_outside):
        return getattr(self, arg)(arg_outside)
