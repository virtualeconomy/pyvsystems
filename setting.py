DEFAULT_TX_FEE = 10000000
DEFAULT_LEASE_FEE = 10000000
DEFAULT_CANCEL_LEASE_FEE = 10000000
DEFAULT_ALIAS_FEE = 10000000
DEFAULT_CONTEND_SLOT_FEE = 5000000000000
DEFAULT_RELEASE_SLOT_FEE = 10000000
DEFAULT_MINTING_FEE = 10000000
DEFAULT_FEE_SCALE = 100

THROW_EXCEPTION_ON_ERROR = False

CHAIN = 'mainnet'
CHAIN_ID = 'M'

NODE = 'http://127.0.0.1'
API_KEY = ''


def set_throw_on_error(throw=True):
    global THROW_EXCEPTION_ON_ERROR
    THROW_EXCEPTION_ON_ERROR = throw


def set_chain(chain_name=CHAIN, chain_id=None):
    global CHAIN, CHAIN_ID

    if chain_id is not None:
        CHAIN = chain_name
        CHAIN_ID = chain_id
    else:
        if chain_name.lower() == 'mainnet' or chain_name.lower() == 'm':
            CHAIN = 'mainnet'
            CHAIN_ID = 'M'
        else:
            CHAIN = 'testnet'
            CHAIN_ID = 'T'


def get_chain():
    return CHAIN


def get_chain_id():
    return CHAIN_ID


def set_node(node=NODE, chain=CHAIN, chain_id=None, api_key=''):
    global NODE, CHAIN, CHAIN_ID, API_KEY
    NODE = node
    API_KEY = api_key
    set_chain(chain, chain_id)


def get_node():
    return NODE


def get_api_key():
    return API_KEY

