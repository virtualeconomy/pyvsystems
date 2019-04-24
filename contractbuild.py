import itertools
import os
import struct

from pyvsystems import deser
from pyvsystems.dataentry import DataEntry
from pyvsystems.deser import serializeString


class ContractBuild:
    # texture
    initPara = ["max", "unity", "tokenDescription"]
    supersedePara = ["newIssuer"]
    issuePara = ["amount", "tokenIndex"]
    destroyPara = ["amount", "tokenIndex"]
    splitPara = ["newUnity", "tokenIndex"]
    sendPara = ["receipt", "amount", "tokenIndex"]
    transferPara = ["sender", "receipt", "amount", "tokenIndex"]
    depositPara = ["sender", "smart", "amount", "tokenIndex"]
    withdrawPara = ["smart", "receipt", "amount", "tokenIndex"]
    totalSupplyPara = ["tokenIndex"]
    maxSupplyPara = ["tokenIndex"]
    balanceOfPara = ["address", "tokenIndex"]
    getIssuerPara = []

    # statevar
    statevar_issuer = bytes([0])
    statevar_maker = bytes([1])
    statevar_max = bytes([2])
    statevar_total = bytes([3])
    statevar_unity = bytes([4])
    statevar_shortText = bytes([5])

    # datatype
    PublicKey = bytes([1])
    Address = bytes([2])
    Amount = bytes([3])
    Int32 = bytes([4])
    ShortText = bytes([5])
    ContractAccount = bytes([6])
    Account = bytes([7])

    # assertype
    GteqZeroAssert = bytes([1])
    LteqAssert = bytes([2])
    LtInt64Assert = bytes([3])
    GtZeroAssert = bytes([4])
    EqAssert =bytes([5])
    IsCallerOriginAssert = bytes([6])
    IsSignerOriginAssert = bytes([7])

    # cdbvtype
    SetCDBV = bytes([1])

    # cdbvrtype
    GetCDBVR = bytes([1])

    # loadtype
    SignerLoad = bytes([1])
    CallerLoad =bytes([2])

    # opctype
    AssertOpc = bytes([1])
    LoadOpc = bytes([2])
    CDBVOpc = bytes([3])
    CDBVROpc = bytes([4])
    TDBOpc = bytes([5])
    TDBROpc = bytes([6])
    TDBAOpc = bytes([7])
    TDBAROpc = bytes([8])
    ReturnOpc = bytes([9])

    # tdbatype
    DepositTDBA = bytes([1])
    WithdrawTDBA = bytes([2])
    TransferTDBA = bytes([3])

    # tdbartype
    BalanceTBDAR = bytes([1])

    # tdbtype
    NewTokenTDB = bytes([1])
    SplitTDB = bytes([2])

    # tdbrtype
    GetTDBR = bytes([1])
    TotalTDBR = bytes([2])

    # funid
    init = 0
    supersede = 1
    issue = 2
    destroy = 3
    split = 4
    send = 5
    transfer = 6
    deposit = 7
    withdraw = 8
    totalSupply = 9
    maxSupply = 10
    balanceOf = 11
    getIssuer = 12

    supersedeIndex = bytes([0])
    issueIndex = bytes([1])
    destroyIndex = bytes([2])
    splitIndex = bytes([3])
    sendIndex = bytes([4])
    transferIndex = bytes([5])
    depositIndex = bytes([6])
    withdrawIndex = bytes([7])
    totalSupplyIndex = bytes([8])
    maxSupplyIndex = bytes([9])
    balanceOfIndex = bytes([10])
    getIssuerIndex = bytes([11])

    # datastack
    initInput_maxIndex = bytes([0])
    initInput_unityIndex = bytes([1])
    initInput_shortTextIndex = bytes([2])
    initInput_issuerLoadIndex = bytes([3])

    supersedeInput_newIssuerIndex = bytes([0])
    supersedeInput_maker = bytes([1])

    splitInput_newUnityIndex = bytes([0])
    splitInput_tokenIndex = bytes([1])
    splitInput_issuerGetIndex = bytes([2])

    destroyInput_destroyAmountIndex = bytes([0])
    destroyInput_tokenIndex = bytes([1])
    destroyInput_issuerGetIndex = bytes([2])

    issueInput_amountIndex = bytes([0])
    issueInput_tokenIndex = bytes([1])
    issueInput_issuerGetIndex = bytes([2])

    sendInput_recipientIndex = bytes([0])
    sendInput_amountIndex = bytes([1])
    sendInput_tokenIndex = bytes([2])
    sendInput_senderIndex = bytes([3])

    transferInput_senderIndex = bytes([0])
    transferInput_recipientIndex = bytes([1])
    transferInput_amountIndex = bytes([2])
    transferInput_tokenIndex = bytes([3])

    depositInput_senderIndex = bytes([0])
    depositInput_smartContractIndex = bytes([1])
    depositInput_amountIndex = bytes([2])
    depositInput_tokenIndex = bytes([3])

    withdrawInput_smartContractIndex = bytes([0])
    withdrawInput_recipientIndex = bytes([1])
    withdrawInput_amountIndex = bytes([2])
    withdrawInput_tokenIndex = bytes([3])

    totalSupplyInput_tokenIndex = bytes([0])

    maxSupplyInput_tokenIndex = bytes([0])

    balanceOfInput_accountIndex = bytes([0])
    balanceOfInput_tokenIndex = bytes([1])

    def contractBuilder(self, languageCode, languageVersion, split=False):
        langCode = self.languageCodeBuilder(languageCode)
        langVer = self.languageVersionBuilder(languageVersion)
        initializer = self.initializerBuilder()
        descriptor = self.descriptorBuilder(split)
        stateVar = self.stateVarBuilder()
        texture = self.textureBuilder(split)
        # print(texture, len(texture))
        return langCode + langVer + initializer + descriptor + stateVar + texture

    # OpcId
    def assertGteqZeroGen(self):
        return self.opcAssertGteqZero()
    def assertLteqGen(self):
        return self.opcAssertLteq()
    def assertLtInt64Gen(self):
        return self.opcAssertLtInt64()
    def assertGtZeroGen(self):
        return self.opcAssertGtZero()
    def assertEqGen(self):
        return self.opcAssertEq()
    def assertIsCallerOriginGen(self):
        return self.opcAssertIsCallerOrigin()
    def assertIsSignerOriginGen(self):
        return self.opcAssertIsSignerOrigin()
    def loadSingerGen(self):
        return self.opcLoadSigner()
    def loadCallerGen(self):
        return self.opcLoadCaller()
    def CDBVSetGen(self):
        return self.opcCDBVSet()
    def CDBVRGetGen(self):
        return self.opcCDBVRGet()
    def TDBNewTokenGen(self):
        return self.opcTDBNewToken()
    def TDBSplitGen(self):
        return self.opcTDBSplit()
    def TDBROpcGet(self):
        return self.opcTDBROpcGet()
    def TDBROpcTotalGen(self):
        return self.opcTDBROpcTotal()
    def TDBADepositGen(self):
        return self.opcTDBADeposit()
    def TDBAWithdrawGen(self):
        return self.opcTDBAWithdraw()
    def TDBATransferGen(self):
        return self.opcTDBATransfer()
    def TDBARBalanceGen(self):
        return self.opcTDBARBalance()

    def opcAssertGteqZero(self):
        return self.AssertOpc + self.GteqZeroAssert

    def opcAssertLteq(self):
        return self.AssertOpc + self.LteqAssert

    def opcAssertLtInt64(self):
        return self.AssertOpc + self.LtInt64Assert

    def opcAssertGtZero(self):
        return self.AssertOpc + self.GtZeroAssert

    def opcAssertEq(self):
        return self.AssertOpc + self.EqAssert

    def opcAssertIsCallerOrigin(self):
        return self.AssertOpc + self.IsCallerOriginAssert

    def opcAssertIsSignerOrigin(self):
        return self.AssertOpc + self.IsSignerOriginAssert

    def opcLoadSigner(self):
        return self.LoadOpc + self.SignerLoad

    def opcLoadCaller(self):
        return self.LoadOpc + self.CallerLoad

    def opcCDBVSet(self):
        return self.CDBVOpc + self.SetCDBV

    def opcCDBVRGet(self):
        return self.CDBVROpc + self.GetCDBVR

    def opcTDBNewToken(self):
        return self.TDBOpc + self.NewTokenTDB

    def opcTDBSplit(self):
        return self.TDBOpc + self.SplitTDB

    def opcTDBROpcGet(self):
        return self.TDBROpc + self.GetTDBR

    def opcTDBROpcTotal(self):
        return self.TDBROpc + self.TotalTDBR

    def opcTDBADeposit(self):
        return self.TDBAOpc + self.DepositTDBA

    def opcTDBAWithdraw(self):
        return self.TDBAOpc + self.WithdrawTDBA

    def opcTDBATransfer(self):
        return self.TDBAOpc + self.TransferTDBA

    def opcTDBARBalance(self):
        return self.TDBAROpc + self.BalanceTBDAR

    def opcReturnValue(self):
        return self.ReturnOpc + bytes([0])

    # languageCode
    def languageCodeBuilder(self, code):
        languageCode = serializeString(code)
        return languageCode

    # languageVersion
    def languageVersionBuilder(self, version):
        return struct.pack(">I", version)

    # initializer
    def initializerBuilder(self):
        return deser.serializeArray(self.initFunGen())

    # descriptor
    def descriptorBuilder(self, split):
        if(split is False):
            descriptor = deser.serializeArrays(
                [self.supersedeFunGen(), self.issueFunGen(), self.destroyFunGen(),
                 self.sendFunGen(), self.transferFunGen(), self.depositFunGen(), self.withdrawFunGen(), self.totalSupplyFunGen(),
                 self.maxSupplyFunGen(), self.balanceOfFunGen(), self.getIssuerFunGen()])
        else:
            descriptor = deser.serializeArrays([self.supersedeFunGen(), self.issueFunGen(), self.destroyFunGen(), self.splitFunGen(), self.sendFunGen(),
                                                self.transferFunGen(), self.depositFunGen(), self.withdrawFunGen(), self.totalSupplyFunGen(),
                                                self.maxSupplyFunGen(), self.balanceOfFunGen(), self.getIssuerFunGen()])
        # print(descriptor)
        return deser.serializeArray(descriptor)


    # stateVar
    def stateVarBuilder(self):
        stateVar = self.stateVarGen([self.statevar_issuer + self.Address, self.statevar_maker + self.Address,
                                self.statevar_max + self.Amount, self.statevar_total + self.Amount,
                                self.statevar_unity + self.Amount, self.statevar_shortText + self.ShortText])
        return deser.serializeArray(stateVar)

    # texture
    def textureBuilder(self, split):
        self._fixedSize = 4
        self.stateVarName = ["issuer", "maker", "max", "total", "unity", "description"]
        self.stateVarTexture = deser.serializeArrays([deser.serializeString(name) for name in self.stateVarName])
        self.initializerTexture = deser.serializeArrays([self.initFuncBytes()])
        if(split is False):
            self.descriptorTexture = deser.serializeArrays([self.supersedeFuncBytes(),
                                                            self.issueFuncBytes(),
                                                            self.destroyFuncBytes(),
                                                            self.sendFuncBytes(),
                                                            self.transferFuncBytes(),
                                                            self.depositFuncBytes(),
                                                            self.withdrawFuncBytes(),
                                                            self.totalSupplyFuncBytes(),
                                                            self.maxSupplyFuncBytes(),
                                                            self.balanceOfFuncBytes(),
                                                            self.getIssuerFuncBytes()])
        else:
            self.descriptorTexture = deser.serializeArrays([self.supersedeFuncBytes(),
                                                            self.issueFuncBytes(),
                                                            self.destroyFuncBytes(),
                                                            self.splitFuncBytes(),
                                                            self.sendFuncBytes(),
                                                            self.transferFuncBytes(),
                                                            self.depositFuncBytes(),
                                                            self.withdrawFuncBytes(),
                                                            self.totalSupplyFuncBytes(),
                                                            self.maxSupplyFuncBytes(),
                                                            self.balanceOfFuncBytes(),
                                                            self.getIssuerFuncBytes()])

        self.textureRightGen = self.textureGen(self.initializerTexture, self.descriptorTexture, self.stateVarTexture)
        return self.textureRightGen

    def textureRandomGen(self):
        texture = bytearray(os.urandom(self._fixedSize))
        return texture

    def textureGen(self, initialization, description, stateVar):
        return deser.serializeArrays([initialization, description, stateVar])

    def textureFunGen(self, name, ret, para):
        funcByte = deser.serializeArray(deser.serializeString(name))
        retByte = deser.serializeArray(deser.serializeString(ret))
        paraByte = deser.serializeArrays([deser.serializeString(p) for p in para])
        texture = funcByte + retByte + paraByte
        return texture


    def initFuncBytes(self):
        return self.textureFunGen("init", "void", self.initPara)

    def supersedeFuncBytes(self):
        return self.textureFunGen("supersede", "void", self.supersedePara)

    def issueFuncBytes(self):
        return self.textureFunGen("issue", "void", self.issuePara)

    def destroyFuncBytes(self):
        return self.textureFunGen("destroy", "void", self.destroyPara)

    def splitFuncBytes(self):
        return self.textureFunGen("split", "void", self.splitPara)

    def sendFuncBytes(self):
        return self.textureFunGen("send", "void", self.sendPara)

    def transferFuncBytes(self):
        return self.textureFunGen("transfer", "void", self.transferPara)

    def depositFuncBytes(self):
        return self.textureFunGen("deposit", "void", self.depositPara)

    def withdrawFuncBytes(self):
        return self.textureFunGen("withdraw", "void", self.withdrawPara)

    def totalSupplyFuncBytes(self):
        return self.textureFunGen("totalSupply", "amount", self.totalSupplyPara)

    def maxSupplyFuncBytes(self):
        return self.textureFunGen("maxSupply", "amount", self.maxSupplyPara)

    def balanceOfFuncBytes(self):
        return self.textureFunGen("balanceOf", "amount", self.balanceOfPara)

    def getIssuerFuncBytes(self):
        return self.textureFunGen("getIssuer", "issuer", self.getIssuerPara)


    # statevar
    def statevar_builder(self):
        self.fixedSize = 2

    def stateVarRandomGen(self):
        statevar = bytearray(os.urandom(self.fixedSize))
        return statevar

    def stateVarGen(self, stateVars):
        stateVars = deser.serializeArrays(stateVars)
        return stateVars

    def aFunctionGen(self, funIdx, protoType, listOpc):
        fun = funIdx + protoType + listOpc
        return fun

    def initFunGen(self):
        fun = self.aFunctionGen(self.initFunIdGen(), self.protoTypeInitGen(), self.initOpcLineGen())
        return fun

    def supersedeFunGen(self):
        fun = self.aFunctionGen(self.supersedeFunIdGen(), self.protoTypeSupersedeGen(), self.supersedeOpcLineGen())
        return fun

    def issueFunGen(self):
        fun = self.aFunctionGen(self.issueFunIdGen(), self.protoTypeIssueGen(), self.issueOpcLineGen())
        return fun

    def destroyFunGen(self):
        fun = self.aFunctionGen(self.destroyFunIdGen(), self.protoTypeDestroyGen(), self.destroyOpcLineGen())
        return fun

    def splitFunGen(self):
        fun = self.aFunctionGen(self.splitFunIdGen(), self.protoTypeSplitGen(), self.splitOpcLineGen())
        return fun

    def sendFunGen(self):
        fun = self.aFunctionGen(self.sendFunIdGen(), self.protoTypeSendGen(), self.sendOpcLineGen())
        return fun

    def transferFunGen(self):
        fun = self.aFunctionGen(self.transferFunIdGen(), self.protoTypeTransferGen(), self.transferOpcLineGen())
        return fun

    def depositFunGen(self):
        fun = self.aFunctionGen(self.depositFunIdGen(), self.protoTypeDepositGen(), self.depositOpcLineGen())
        return fun

    def withdrawFunGen(self):
        fun = self.aFunctionGen(self.withdrawFunIdGen(), self.protoTypeWithdrawGen(), self.withdrawOpcLineGen())
        return fun

    def totalSupplyFunGen(self):
        fun = self.aFunctionGen(self.totalSupplyFunIdGen(), self.protoTypeTotalSupplyGen(), self.totalSupplyOpcLineGen())
        return fun

    def maxSupplyFunGen(self):
        fun = self.aFunctionGen(self.maxSupplyFunIdGen(), self.protoTypeMaxSupplyGen(), self.maxSupplyOpcLineGen())
        return fun

    def balanceOfFunGen(self):
        fun = self.aFunctionGen(self.balanceOfFunIdGen(), self.protoTypeBalanceOfGen(), self.balanceOfOpcLineGen())
        return fun

    def getIssuerFunGen(self):
        fun = self.aFunctionGen(self.getIssuerFunIdGen(), self.protoTypeGetIssuerGen(), self.getIssuerOpcLineGen())
        return fun

    # funid
    def initFunIdGen(self):
        return struct.pack(">H", self.init)
    def supersedeFunIdGen(self):
        return struct.pack(">H", self.supersede)
    def issueFunIdGen(self):
        return struct.pack(">H", self.issue)
    def destroyFunIdGen(self):
        return struct.pack(">H", self.destroy)
    def splitFunIdGen(self):
        return struct.pack(">H", self.split)
    def sendFunIdGen(self):
        return struct.pack(">H", self.send)
    def transferFunIdGen(self):
        return struct.pack(">H", self.transfer)
    def depositFunIdGen(self):
        return struct.pack(">H", self.deposit)
    def withdrawFunIdGen(self):
        return struct.pack(">H", self.withdraw)
    def totalSupplyFunIdGen(self):
        return struct.pack(">H", self.totalSupply)
    def maxSupplyFunIdGen(self):
        return struct.pack(">H", self.maxSupply)
    def balanceOfFunIdGen(self):
        return struct.pack(">H", self.balanceOf)
    def getIssuerFunIdGen(self):
        return struct.pack(">H", self.getIssuer)

    # prototype
    def protoTypeGen(self, returnType, listParaTypes):
        length = struct.pack(">H", len(listParaTypes) + 1)
        protoType = length + returnType + listParaTypes
        return protoType

    def returnType(self):
        return bytes([1])

    def initParaTypeWrong(self):
        return self.Amount + self.Amount

    def initParaType(self):
        return self.Amount + self.Amount + self.ShortText

    def supersedeParaType(self):
        return self.Account

    def issueParaType(self):
        return self.Amount + self.Int32

    def destroyParaType(self):
        return self.Amount + self.Int32

    def splitParaType(self):
        return self.Amount + self.Int32

    def sendParaType(self):
        return self.Account + self.Amount + self.Int32

    def transferParaType(self):
        return self.Account + self.Account + self.Amount + self.Int32

    def depositParaType(self):
        return self.Account + self.ContractAccount + self.Amount + self.Int32

    def withdrawParaType(self):
        return self.ContractAccount + self.Account + self.Amount + self.Int32

    def totalSupplyParaType(self):
        return self.Int32

    def maxSupplyParaType(self):
        return self.Int32

    def balanceOfParaType(self):
        return self.Account + self.Int32

    def getIssuerParaType(self):
        return bytes('',encoding ='utf-8')

    def protoTypeInitWrongGen(self):
        return self.protoTypeGen(self.returnType(), self.initParaTypeWrong())

    def protoTypeInitGen(self):
        return self.protoTypeGen(self.returnType(), self.initParaType())

    def protoTypeSupersedeGen(self):
        return self.protoTypeGen(self.returnType(), self.supersedeParaType())

    def protoTypeIssueGen(self):
        return self.protoTypeGen(self.returnType(), self.issueParaType())

    def protoTypeDestroyGen(self):
        return self.protoTypeGen(self.returnType(), self.destroyParaType())

    def protoTypeSplitGen(self):
        return self.protoTypeGen(self.returnType(), self.splitParaType())

    def protoTypeSendGen(self):
        return self.protoTypeGen(self.returnType(), self.sendParaType())

    def protoTypeTransferGen(self):
        return self.protoTypeGen(self.returnType(), self.transferParaType())

    def protoTypeDepositGen(self):
        return self.protoTypeGen(self.returnType(), self.depositParaType())

    def protoTypeWithdrawGen(self):
        return self.protoTypeGen(self.returnType(), self.withdrawParaType())

    def protoTypeTotalSupplyGen(self):
        return self.protoTypeGen(self.returnType(), self.totalSupplyParaType())

    def protoTypeMaxSupplyGen(self):
        return self.protoTypeGen(self.returnType(), self.maxSupplyParaType())

    def protoTypeBalanceOfGen(self):
        return self.protoTypeGen(self.returnType(), self.balanceOfParaType())

    def protoTypeGetIssuerGen(self):
        return self.protoTypeGen(self.returnType(), self.getIssuerParaType())


    # listopc
    def listOpcGen(self, ids, indexInput):
        length = struct.pack(">H", sum(list(map(lambda x: len(x[0]+x[1])+2, list(zip(ids, indexInput))))) + 2)
        numOpc = struct.pack(">H", len(ids))
        listOpc = bytes(itertools.chain.from_iterable(list(map(lambda x: struct.pack(">H",len(x[0]+x[1]))+x[0]+x[1], list(zip(ids, indexInput))))))
        lenListOpc = length + numOpc + listOpc
        return lenListOpc


    def initOpcLineWrongTDBGen(self):
        return self.listOpcGen(self.initWrongTDBOpc(), self.initOpcIndex())

    def initOpcLineGen(self):
        return self.listOpcGen(self.initOpc(), self.initOpcIndex())

    def supersedeOpcLineGen(self):
        return self.listOpcGen(self.supersedeOpc(), self.supersedeOpcIndex())

    def issueOpcLineGen(self):
        return self.listOpcGen(self.issueOpc(), self.issueOpcIndex())

    def destroyOpcLineGen(self):
        return self.listOpcGen(self.destroyOpc(), self.destroyOpcIndex())

    def splitOpcLineGen(self):
        return self.listOpcGen(self.splitOpc(), self.splitOpcIndex())

    def sendOpcLineGen(self):
        return self.listOpcGen(self.sendOpc(), self.sendOpcIndex())

    def transferOpcLineGen(self):
        return self.listOpcGen(self.transferOpc(), self.transferOpcIndex())

    def depositOpcLineGen(self):
        return self.listOpcGen(self.depositOpc(), self.depositOpcIndex())

    def withdrawOpcLineGen(self):
        return self.listOpcGen(self.withdrawOpc(), self.withdrawOpcIndex())

    def totalSupplyOpcLineGen(self):
        return self.listOpcGen(self.totalSupplyOpc(), self.totalSupplyOpcIndex())

    def maxSupplyOpcLineGen(self):
        return self.listOpcGen(self.maxSupplyOpc(), self.maxSupplyOpcIndex())

    def balanceOfOpcLineGen(self):
        return self.listOpcGen(self.balanceOfOpc(), self.balanceOfOpcIndex())

    def getIssuerOpcLineGen(self):
        return self.listOpcGen(self.getIssuerOpc(), self.getIssuerOpcIndex())

    def opcLoadSignerIndex(self):
        return bytes('',encoding ='utf-8')

    def opcLoadCallerIndex(self):
        return bytes('',encoding ='utf-8')

    def initOpcCDBVSetSignerIndex(self):
        return self.statevar_issuer + self.initInput_issuerLoadIndex

    def initOpcCDBVSetMakerIndex(self):
        return self.statevar_maker + self.initInput_issuerLoadIndex

    def initOpcTDBNewTokenIndex(self):
        return self.statevar_max + self.statevar_total + self.statevar_unity + \
               self.statevar_shortText + self.initInput_maxIndex + self.initInput_unityIndex +\
               self.initInput_shortTextIndex

    def initWrongTDBOpc(self):
        return [self.opcLoadSigner(), self.opcCDBVSet(), self.opcCDBVSet(), bytes([5]), bytes([3])]

    def initOpc(self):
        return [self.opcLoadSigner(), self.opcCDBVSet(), self.opcCDBVSet(), self.opcTDBNewToken()]

    def initOpcIndex(self):
        return [self.opcLoadSignerIndex(), self.initOpcCDBVSetSignerIndex(), self.initOpcCDBVSetMakerIndex(), self.initOpcTDBNewTokenIndex()]

    def supersedeOpcCDBVRGetIndex(self):
        return self.statevar_maker

    def superAssertIsSignerOriginIndex(self):
        return self.supersedeInput_maker

    def supersedeOpcCDBVSetIndex(self):
        return self.statevar_issuer + self.supersedeInput_newIssuerIndex

    def supersedeOpc(self):
        return [self.opcCDBVRGet(), self.opcAssertIsSignerOrigin(), self.opcCDBVSet()]

    def supersedeOpcIndex(self):
        return [self.supersedeOpcCDBVRGetIndex(), self.superAssertIsSignerOriginIndex(), self.supersedeOpcCDBVSetIndex()]

    def issueOpcCDBVRGetIndex(self):
        return self.statevar_issuer

    def issueOpcAssertIsCallerOriginIndex(self):
        return self.issueInput_issuerGetIndex

    def issueOpcTDBADepositIndex(self):
        return self.statevar_max + self.statevar_total + self.issueInput_issuerGetIndex + self.issueInput_amountIndex + self.issueInput_tokenIndex

    def issueOpc(self):
        return [self.opcCDBVRGet(), self.opcAssertIsCallerOrigin(), self.opcTDBADeposit()]

    def issueOpcIndex(self):
        return [self.issueOpcCDBVRGetIndex(), self.issueOpcAssertIsCallerOriginIndex(), self.issueOpcTDBADepositIndex()]

    def destroyOpcCDBVRGetIndex(self):
        return self.statevar_issuer

    def destroyOpcAssertIsCallerOriginIndex(self):
        return self.destroyInput_issuerGetIndex

    def destroyOpcTDBAWithdrawIndex(self):
        return self.statevar_total + self.destroyInput_issuerGetIndex + self.destroyInput_destroyAmountIndex + self.destroyInput_tokenIndex

    def destroyOpc(self):
        return [self.opcCDBVRGet(), self.opcAssertIsCallerOrigin(), self.opcTDBAWithdraw()]

    def destroyOpcIndex(self):
        return [self.destroyOpcCDBVRGetIndex(), self.destroyOpcAssertIsCallerOriginIndex(), self.destroyOpcTDBAWithdrawIndex()]

    def splitOpcCDBVRGetIndex(self):
        return self.statevar_issuer

    def splitOpcAssertIsCallerOriginIndex(self):
        return self.splitInput_issuerGetIndex

    def splitOpcTDBSplitIndex(self):
        return self.statevar_unity + self.splitInput_newUnityIndex + self.splitInput_tokenIndex

    def splitOpc(self):
        return [self.opcCDBVRGet(), self.opcAssertIsCallerOrigin(), self.opcTDBSplit()]

    def splitOpcIndex(self):
        return [self.splitOpcCDBVRGetIndex(), self.splitOpcAssertIsCallerOriginIndex(), self.splitOpcTDBSplitIndex()]

    def sendOpcTDBATransferIndex(self):
        return self.sendInput_senderIndex + self.sendInput_recipientIndex + self.sendInput_amountIndex + self.sendInput_tokenIndex

    def sendOpc(self):
        return [self.opcLoadCaller(), self.opcTDBATransfer()]

    def sendOpcIndex(self):
        return [self.opcLoadCallerIndex(), self.sendOpcTDBATransferIndex()]

    def transferOpcAssertIsCallerOriginIndex(self):
        return self.transferInput_senderIndex

    def transferOpcTDBATransferIndex(self):
        return self.transferInput_senderIndex + self.transferInput_recipientIndex + self.transferInput_amountIndex + self.transferInput_tokenIndex

    def transferOpc(self):
        return [self.opcAssertIsCallerOrigin(), self.opcTDBATransfer()]

    def transferOpcIndex(self):
        return [self.transferOpcAssertIsCallerOriginIndex(), self.transferOpcTDBATransferIndex()]

    def depositOpcAssertIsCallerOriginIndex(self):
        return self.depositInput_senderIndex

    def depositOpcTDBATransferIndex(self):
        return self.depositInput_senderIndex + self.depositInput_smartContractIndex + self.depositInput_amountIndex + self.depositInput_tokenIndex

    def depositOpc(self):
        return [self.opcAssertIsCallerOrigin(), self.opcTDBATransfer()]

    def depositOpcIndex(self):
        return [self.depositOpcAssertIsCallerOriginIndex(), self.depositOpcTDBATransferIndex()]

    def withdrawOpcAssertIsCallerOriginIndex(self):
        return self.withdrawInput_recipientIndex

    def withdrawOpcTDBATransferIndex(self):
        return self.withdrawInput_smartContractIndex + self.withdrawInput_recipientIndex + self.withdrawInput_amountIndex + self.withdrawInput_tokenIndex

    def withdrawOpc(self):
        return [self.opcAssertIsCallerOrigin(), self.opcTDBATransfer()]

    def withdrawOpcIndex(self):
        return [self.withdrawOpcAssertIsCallerOriginIndex(), self.withdrawOpcTDBATransferIndex()]

    def totalSupplyOpcTDBRTotalIndex(self):
        return self.statevar_total + self.totalSupplyInput_tokenIndex

    def totalSupplyOpc(self):
        return [self.opcTDBROpcTotal(), self.opcReturnValue()]

    def totalSupplyOpcIndex(self):
        return [self.totalSupplyOpcTDBRTotalIndex(), bytes('',encoding ='utf-8')]

    def maxSupplyOpcTDBRMaxIndex(self):
        return self.statevar_max + self.maxSupplyInput_tokenIndex

    def maxSupplyOpc(self):
        return [self.opcTDBROpcGet(), self.opcReturnValue()]

    def maxSupplyOpcIndex(self):
        return [self.maxSupplyOpcTDBRMaxIndex(), bytes('',encoding ='utf-8')]

    def balanceOfOpcTDBARBalanceIndex(self):
        return self.balanceOfInput_accountIndex + self.balanceOfInput_tokenIndex

    def balanceOfOpc(self):
        return [self.opcTDBARBalance(), self.opcReturnValue()]

    def balanceOfOpcIndex(self):
        return [self.balanceOfOpcTDBARBalanceIndex(), bytes('',encoding ='utf-8')]

    def getIssuerOpcCDBVRGetIndex(self):
        return self.statevar_issuer

    def getIssuerOpc(self):
        return [self.opcCDBVRGet(), self.opcReturnValue()]

    def getIssuerOpcIndex(self):
        return [self.getIssuerOpcCDBVRGetIndex(), bytes('',encoding ='utf-8')]

    # datastack
    def initDataStackGen(self, amount, unity, desc):

        max = DataEntry(bytes([amount]), self.Amount)
        unit = DataEntry(bytes([unity]), self.Amount)
        shortText = DataEntry.create(desc.getBytes(), self.ShortText)
        return [max, unit, shortText]

    def supersedeDataStackGen(self, newIssuer):
        iss = DataEntry(newIssuer.bytes.arr, self.Address)
        return iss

    def splitDataStackGen(self, newUnity, tokenIndex):
        unit = DataEntry(bytes([newUnity]), self.Amount)
        index =   DataEntry(bytes([tokenIndex]), self.Int32)
        return [unit, index]

    def destroyDataStackGen(self, amount, tokenIndex):
        am = DataEntry(bytes([amount]), self.Amount)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [am, index]

    def issueDataStackGen(self, amount, tokenIndex):
        max = DataEntry(bytes([amount]), self.Amount)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [max, index]

    def sendDataStackGen(self, recipient, amount, tokenIndex):
        reci = DataEntry(recipient.bytes.arr, self.Address)
        am = DataEntry(bytes([amount]), self.Amount)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [reci, am, index]

    def transferDataStackGen(self, sender, recipient, amount, tokenIndex):
        se = DataEntry(sender.bytes.arr, self.Address)
        reci = DataEntry(recipient.bytes.arr, self.Address)
        am = DataEntry(bytes([amount]), self.Amount)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [se, reci, am, index]

    def depositDataStackGen(self, sender, smartContract, amount, tokenIndex):
        se = DataEntry(sender.bytes.arr, self.Address)
        sc = DataEntry(smartContract.bytes.arr, self.Address)
        am = DataEntry(bytes([amount]), self.Amount)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [se, sc, am, index]

    def withdrawDataStackGen(self, smartContract, recipient, amount, tokenIndex):
        sc = DataEntry(smartContract.bytes.arr, self.Address)
        reci = DataEntry(recipient.bytes.arr, self.Address)
        am = DataEntry(bytes([amount]), self.Amount)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [sc, reci, am, index]

    def totalSupplyDataStackGen(self, tokenIndex):
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [index]

    def maxSupplyDataStackGen(self, tokenIndex):
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [index]

    def balanceOfDataStackGen(self, account, tokenIndex):
        acc =  DataEntry(account.bytes.arr, self.Address)
        index = DataEntry(bytes([tokenIndex]), self.Int32)
        return [acc, index]
