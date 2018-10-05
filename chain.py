import base58
import logging
from .crypto import hashChain, bytes2str, str2bytes
from .setting import ADDRESS_LENGTH, ADDRESS_CHECKSUM_LENGTH

class Chain(object):

    def __init__(self, chain_name, chain_id, address_version, api_wrapper):
        self.chain_name = chain_name
        self.chain_id = chain_id
        self.address_version = address_version
        self.api_wrapper = api_wrapper

    def height(self):
        return self.api_wrapper.request('/blocks/height')['height']

    def lastblock(self):
        return self.api_wrapper.request('/blocks/last')

    def block(self, n):
        return self.api_wrapper.request('/blocks/at/%d' % n)

    def tx(self, id):
        return self.api_wrapper.request('/transactions/info/%s' % id)

    def slot_info(self, slot_id):
        return self.api_wrapper.request('/consensus/slotInfo/%s' % slot_id)

    def validate_address(self, address):
        addr = bytes2str(base58.b58decode(address))
        if addr[0] != chr(self.address_version):
            logging.error("Wrong address version")
        elif addr[1] != self.chain_id:
            logging.error("Wrong chain id")
        elif len(addr) != ADDRESS_LENGTH:
            logging.error("Wrong address length")
        elif addr[-ADDRESS_CHECKSUM_LENGTH:] != hashChain(str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
            logging.error("Wrong address checksum")
        else:
            return True
        return False
