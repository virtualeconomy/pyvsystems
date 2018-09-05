from address import Address
import setting

if __name__ == "__main__" and __package__ is None:
    setting.set_node("http://wallet.testnet.vee.money/api","testnet")
    addr = 'ATt6P4vSpBvBTHdV5V9PJEHMFp4msJ1fkkX'
    pub_key = 'B2Khd89jtnpuzGdnyGRcnKycZMBCo6PsotFcWWi1wMDV'
    private_key = '2ePiTD4jGMmiVsRt74y768pxKtA6nmzmwftMyP4vSYsF'
    seed = 'drill endorse plunge prevent stool expect also tortoise unable distance local spoon wealth resource result sign chair hockey'
    # address = Address(addr, pub_key, private_key, seed, '', 1)
    address = Address(seed=seed, nonce=1)
    print("Balance: {}".format(address.balance()))
