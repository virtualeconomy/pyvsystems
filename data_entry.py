# from .crypto import *
from .error import *
from .contract_build import *
import base58
import pyvsystems


class DataEntry:
    def __init__(self, data, dataType):
        if not type(dataType) is bytes:
            msg = 'Data Type must be bytes'
            pyvsystems.throw_error(msg, InvalidParameterException)
        if dataType == Type.PublicKey:
            self.bytes = dataType + base58.b58decode(data)
        elif dataType == Type.Address:
            self.bytes = dataType + base58.b58decode(data)
        elif dataType == Type.Amount:
            self.bytes = dataType + struct.pack(">Q", data)
        elif dataType == Type.Int32:
            self.bytes = dataType + struct.pack(">I", data)
        elif dataType == Type.ShortText:
            self.bytes = dataType + deser.serializeDataString(data)
        elif dataType == Type.ContractAccount:
            self.bytes = dataType + base58.b58decode(data)
        elif dataType == Type.Account:
            self.bytes = dataType + base58.b58decode(data)
        else:
            msg = 'Invalid Data Entry'
            pyvsystems.throw_error(msg, InvalidParameterException)


class DataStackGen:
   # datastack
    @staticmethod
    def initDataStackGen(max, unity, desc):
        max = DataEntry(max, Type.Amount)
        unit = DataEntry(unity, Type.Amount)
        shortText = DataEntry(desc, Type.ShortText)
        init_data_stack = [max.bytes, unit.bytes, shortText.bytes]
        return deser.serializeDataStack(init_data_stack)

    @staticmethod
    def supersedeDataStackGen(newIssuer):
        iss = DataEntry(newIssuer, Type.Address)
        supersede_data_stack = [iss.bytes]
        return deser.serializeDataStack(supersede_data_stack)

    @staticmethod
    def splitDataStackGen(newUnity, tokenIndex):
        unit = DataEntry(newUnity, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        split_data_stack = [unit.bytes, index.bytes]
        return deser.serializeDataStack(split_data_stack)

    @staticmethod
    def destroyDataStackGen(amount, tokenIndex):
        am = DataEntry(amount, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        destroy_data_stack = [am.bytes, index.bytes]
        return deser.serializeDataStack(destroy_data_stack)

    @staticmethod
    def issueDataStackGen(amount, tokenIndex):
        max = DataEntry(amount, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        issue_data_stack = [max.bytes, index.bytes]
        return deser.serializeDataStack(issue_data_stack)

    @staticmethod
    def sendDataStackGen(recipient, amount, tokenIndex):
        reci = DataEntry(recipient, Type.Address)
        am = DataEntry(amount, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        send_data_stack = [reci.bytes, am.bytes, index.bytes]
        return deser.serializeDataStack(send_data_stack)

    @staticmethod
    def transferDataStackGen(sender, recipient, amount, tokenIndex):
        se = DataEntry(sender, Type.Address)
        reci = DataEntry(recipient, Type.Address)
        am = DataEntry(amount, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        transfer_data_stack = [se.bytes, reci.bytes, am.bytes, index.bytes]
        return deser.serializeDataStack(transfer_data_stack)

    @staticmethod
    def depositDataStackGen(sender, smartContract, amount, tokenIndex):
        se = DataEntry(sender, Type.Address)
        sc = DataEntry(smartContract, Type.Address)
        am = DataEntry(amount, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        deposit_data_stack = [se.bytes, sc.bytes, am.bytes, index.bytes]
        return deser.serializeDataStack(deposit_data_stack)

    @staticmethod
    def withdrawDataStackGen(smartContract, recipient, amount, tokenIndex):
        sc = DataEntry(smartContract.bytes.arr, Type.Address)
        reci = DataEntry(recipient.bytes.arr, Type.Address)
        am = DataEntry(amount, Type.Amount)
        index = DataEntry(tokenIndex, Type.Int32)
        withdraw_data_stack = [sc.bytes, reci.bytes, am.bytes, index.bytes]
        return deser.serializeDataStack(withdraw_data_stack)

    @staticmethod
    def totalSupplyDataStackGen(tokenIndex):
        index = DataEntry(tokenIndex, Type.Int32)
        total_supply_data_stack = [index.bytes]
        return deser.serializeDataStack(total_supply_data_stack)

    @staticmethod
    def maxSupplyDataStackGen(tokenIndex):
        index = DataEntry(tokenIndex, Type.Int32)
        max_supply_data_stack = [index.bytes]
        return deser.serializeDataStack(max_supply_data_stack)

    @staticmethod
    def balanceOfDataStackGen(account, tokenIndex):
        acc =  DataEntry(account.bytes.arr, Type.Address)
        index = DataEntry(tokenIndex, Type.Int32)
        balance_of_data_stack = [acc.bytes, index.bytes]
        return deser.serializeDataStack(balance_of_data_stack)


class Type:
    PublicKey = bytes([1])
    Address = bytes([2])
    Amount = bytes([3])
    Int32 = bytes([4])
    ShortText = bytes([5])
    ContractAccount = bytes([6])
    Account = bytes([7])


