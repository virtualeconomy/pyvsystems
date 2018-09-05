from .address import *
from .chain import *


ADDRESS_VERSION = 1
ADDRESS_CHECKSUM_LENGTH = 4
ADDRESS_HASH_LENGTH = 20
ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

CHAIN = 'mainnet'
CHAIN_ID = 'M'

NODE = 'http://127.0.0.1'
API_KEY = ''


def setChain(chain_name=CHAIN, chain_id=None):
    global CHAIN, CHAIN_ID

    if chain_id is not None:
        CHAIN = chain
        CHAIN_ID = chain_id
    else:
        if chain_name.lower() == 'mainnet' or chain_name.lower() == 'm':
            CHAIN = 'mainnet'
            CHAIN_ID = 'M'
        else:
            CHAIN = 'testnet'
            CHAIN_ID = 'T'


def getChain():
    return CHAIN


def setNode(node=NODE, chain=CHAIN, chain_id=None, api_key=''):
    global NODE, CHAIN, CHAIN_ID, API_KEY
    NODE = node
    API_KEY = api_key
    setChain(chain, chain_id)


def getNode():
    return NODE


def validateAddress(address):
    addr = crypto.bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        logging.error("Wrong address version")
    elif addr[1] != CHAIN_ID:
        logging.error("Wrong chain id")
    elif len(addr) != ADDRESS_LENGTH:
        logging.error("Wrong address length")
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        logging.error("Wrong address checksum")
    else:
        return True
    return False