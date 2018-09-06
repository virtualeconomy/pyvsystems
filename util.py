from setting import THROW_EXCEPTION_ON_ERROR
import setting
import base58
import logging
import crypto

ADDRESS_VERSION = 5
ADDRESS_CHECKSUM_LENGTH = 4
ADDRESS_HASH_LENGTH = 20
ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH


class PyVeeException(Exception):
    pass


def throw_error(msg):
    if THROW_EXCEPTION_ON_ERROR:
        raise PyVeeException(msg)


def validate_address(address):
    addr = crypto.bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        logging.error("Wrong address version")
    elif addr[1] != setting.get_chain_id():
        logging.error("Wrong chain id")
    elif len(addr) != ADDRESS_LENGTH:
        logging.error("Wrong address length")
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        logging.error("Wrong address checksum")
    else:
        return True
    return False