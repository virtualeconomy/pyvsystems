from .setting import *
from .crypto import *
from .error import *
from .words import WORDS
from . import is_offline
from . import default_chain
from .contract_methods import register_contract, execute_contract
import time
import struct
import json
import base58


class Account(object):
    def __init__(self, chain=default_chain(), address='', public_key='', private_key='', seed='', alias='', nonce=0):
        self.chain = chain
        self.wrapper = chain.api_wrapper
        if nonce < 0 or nonce > MAX_NONCE:
            raise InvalidParameterException('Nonce must be between 0 and %d' % MAX_NONCE)
        if seed:
            self._generate(seed=seed, nonce=nonce)
        elif private_key:
            self._generate(private_key=private_key)
        elif public_key:
            self._generate(public_key=public_key)
        elif address:
            if not self.chain.validate_address(address):
                raise InvalidAddressException("Invalid address")
            else:
                self.address = address
                self.publicKey = public_key
                self.privateKey = private_key
                self.seed = seed
                self.nonce = nonce
        elif alias:
            raise InvalidParameterException("The alias is not support in V systems")
        else:
            self._generate(nonce=nonce)

    def __str__(self):
        if not self.address:
            raise InvalidAddressException("No address")
        result = 'address = %s\npublicKey = %s\nprivateKey = %s\nseed = %s\nnonce = %d' % \
               (self.address, self.publicKey, self.privateKey, self.seed, self.nonce)
        if not is_offline():
            try:
                balance = self.balance()
                result += "\nbalance: {}".format(balance)
            except NetworkException:
                # Failed to get balance
                pass
        return result

    __repr__ = __str__

    def balance(self, confirmations=0):
        if is_offline():
            throw_error("Cannot check balance in offline mode.", NetworkException)
            return 0
        try:
            confirmations_str = '' if confirmations == 0 else '/%d' % confirmations
            resp = self.wrapper.request('/addresses/balance/%s%s' % (self.address, confirmations_str))
            return resp['balance']
        except Exception as ex:
            msg = "Failed to get balance. ({})".format(ex)
            throw_error(msg, NetworkException)
            return 0

    def balance_detail(self):
        try:
            resp = self.wrapper.request('/addresses/balance/details/%s' % self.address)
            return resp
        except Exception as ex:
            msg = "Failed to get balance detail. ({})".format(ex)
            throw_error(msg, NetworkException)
            return None

    def _generate(self, public_key='', private_key='', seed='', nonce=0):
        self.seed = seed
        self.nonce = nonce
        if not public_key and not private_key and not seed:
            wordCount = 2048
            words = []
            for i in range(5):
                r = bytes2str(os.urandom(4))
                x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
                w1 = x % wordCount
                w2 = ((int(x / wordCount) >> 0) + w1) % wordCount
                w3 = ((int((int(x / wordCount) >> 0) / wordCount) >> 0) + w2) % wordCount
                words.append(WORDS[w1])
                words.append(WORDS[w2])
                words.append(WORDS[w3])
            self.seed = ' '.join(words)
        if public_key:
            pubKey = base58.b58decode(public_key)
            privKey = ""
        else:
            seedHash = hashChain(str2bytes(str(nonce)+self.seed))
            accountSeedHash = sha256(seedHash)
            if not private_key:
                privKey = curve.generatePrivateKey(accountSeedHash)
            else:
                privKey = base58.b58decode(private_key)
            pubKey = curve.generatePublicKey(privKey)
        self.address = self.chain.public_key_to_address(pubKey)
        self.publicKey = bytes2str(base58.b58encode(pubKey))
        if privKey != "":
            self.privateKey = bytes2str(base58.b58encode(privKey))

    def send_payment(self, recipient, amount, attachment='', tx_fee=DEFAULT_PAYMENT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if not self.privateKey:
            msg = 'Private key required'
            throw_error(msg, MissingPrivateKeyException)
        if not self.chain.validate_address(recipient.address):
            msg = 'Invalid recipient address'
            throw_error(msg, InvalidAddressException)
        elif amount <= 0:
            msg = 'Amount must be > 0'
            throw_error(msg, InvalidParameterException)
        elif tx_fee < DEFAULT_PAYMENT_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_PAYMENT_FEE
            throw_error(msg, InvalidParameterException)
        elif len(attachment) > MAX_ATTACHMENT_SIZE:
            msg = 'Attachment length must be <= %d' % MAX_ATTACHMENT_SIZE
            throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            throw_error(msg, InvalidParameterException)
        elif not is_offline() and self.balance() < amount + tx_fee:
            msg = 'Insufficient VSYS balance'
            throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", PAYMENT_TX_TYPE) + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">H", len(attachment)) + \
                    str2bytes(attachment)
            signature = bytes2str(sign(self.privateKey, sData))
            attachment_str = bytes2str(base58.b58encode(str2bytes(attachment)))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "attachment": attachment_str,
                "signature": signature
            })

            return self.wrapper.request('/vsys/broadcast/payment', data)

    def lease(self, recipient, amount, tx_fee=DEFAULT_LEASE_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if not self.privateKey:
            msg = 'Private key required'
            throw_error(msg, MissingPrivateKeyException)
        if not self.chain.validate_address(recipient.address):
            msg = 'Invalid recipient address'
            throw_error(msg, InvalidAddressException)
        elif amount <= 0:
            msg = 'Amount must be > 0'
            throw_error(msg, InvalidParameterException)
        elif tx_fee < DEFAULT_LEASE_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_LEASE_FEE
            throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            throw_error(msg, InvalidParameterException)
        elif not is_offline() and self.balance() < amount + tx_fee:
            msg = 'Insufficient VSYS balance'
            throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", LEASE_TX_TYPE) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(self.privateKey, sData))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "signature": signature
            })
            req = self.wrapper.request('/leasing/broadcast/lease', data)
            return req

    def lease_cancel(self, lease_id, tx_fee=DEFAULT_CANCEL_LEASE_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        decode_lease_id = base58.b58decode(lease_id)
        if not self.privateKey:
            msg = 'Private key required'
            throw_error(msg, MissingPrivateKeyException)
        elif tx_fee < DEFAULT_CANCEL_LEASE_FEE:
            msg = 'Transaction fee must be > %d' % DEFAULT_CANCEL_LEASE_FEE
            throw_error(msg, InvalidParameterException)
        elif len(decode_lease_id) != LEASE_TX_ID_BYTES:
            msg = 'Invalid lease transaction id'
            throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            throw_error(msg, InvalidParameterException)
        elif not is_offline() and self.balance() < tx_fee:
            msg = 'Insufficient VSYS balance'
            throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", LEASE_CANCEL_TX_TYPE) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp) + \
                    decode_lease_id
            signature = bytes2str(sign(self.privateKey, sData))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "txId": lease_id,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "signature": signature
            })
            req = self.wrapper.request('/leasing/broadcast/cancel', data)
            return req

    def contend(self, slot_id, tx_fee=DEFAULT_CONTEND_SLOT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if not self.privateKey:
            msg = 'Private key required'
            throw_error(msg, MissingPrivateKeyException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            throw_error(msg, InvalidParameterException)
        elif self.check_contend(slot_id, tx_fee):
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", CONTEND_SLOT_TX_TYPE) + \
                    struct.pack(">I", slot_id) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(self.privateKey, sData))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "slotId": slot_id,
                "timestamp": timestamp,
                "signature": signature
            })
            return self.wrapper.request('/spos/broadcast/contend', data)

    def check_contend(self, slot_id, tx_fee):
        if tx_fee < DEFAULT_CONTEND_SLOT_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_CONTEND_SLOT_FEE
            throw_error(msg, InvalidParameterException)
            return False
        if slot_id >= 60 or slot_id < 0:
            msg = 'Slot id must be in 0 to 59'
            throw_error(msg, InvalidParameterException)
            return False
        if is_offline():  # if offline, skip other check
            return True
        balance_detail = self.get_info()
        min_effective_balance = MIN_CONTEND_SLOT_BALANCE + tx_fee
        if balance_detail["effective"] < min_effective_balance:
            msg = 'Insufficient VSYS balance. (The effective balance must be >= %d)' % min_effective_balance
            throw_error(msg, InvalidParameterException)
            return False
        slot_info = self.chain.slot_info(slot_id)
        if not slot_info or slot_info.get("mintingAverageBalance") is None:
            msg = 'Failed to get slot minting average balance'
            throw_error(msg, NetworkException)
            return False
        elif slot_info["mintingAverageBalance"] >= balance_detail["mintingAverage"]:
            msg = 'The minting average balance of slot %d is greater than or equals to yours. ' \
                  'You will contend this slot failed.' % slot_id
            throw_error(msg, InsufficientBalanceException)
            return False
        return True

    def release(self, slot_id, tx_fee=DEFAULT_RELEASE_SLOT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if not self.privateKey:
            msg = 'Private key required'
            throw_error(msg, MissingPrivateKeyException)
        elif tx_fee < DEFAULT_RELEASE_SLOT_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_RELEASE_SLOT_FEE
            throw_error(msg, InvalidParameterException)
        elif slot_id >= 60 or slot_id < 0:
            msg = 'Slot id must be in 0 to 59'
            throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            throw_error(msg, InvalidParameterException)
        elif not is_offline() and self.balance() < tx_fee:
            msg = 'Insufficient VSYS balance'
            throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", RELEASE_SLOT_TX_TYPE) + \
                    struct.pack(">I", slot_id) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(self.privateKey, sData))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "slotId": slot_id,
                "timestamp": timestamp,
                "signature": signature
            })
            return self.wrapper.request('/spos/broadcast/release', data)

    def dbput(self, db_key, db_data, db_data_type="ByteArray", tx_fee=DEFAULT_DBPUT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if not self.privateKey:
            msg = 'Private key required'
            throw_error(msg, MissingPrivateKeyException)
        elif tx_fee < DEFAULT_DBPUT_FEE:
            msg = 'Transaction fee must be >= %d' % DEFAULT_DBPUT_FEE
            throw_error(msg, InvalidParameterException)
        elif len(db_key) > MAX_DB_KEY_SIZE or len(db_key) < MIN_DB_KEY_SIZE:
            msg = 'DB key length must be greater than %d and smaller than %d' % (MIN_DB_KEY_SIZE, MAX_ATTACHMENT_SIZE)
            throw_error(msg, InvalidParameterException)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            msg = 'Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE
            throw_error(msg, InvalidParameterException)
        elif not is_offline() and self.balance() < tx_fee:
            msg = 'Insufficient VSYS balance'
            throw_error(msg, InsufficientBalanceException)
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            # "ByteArray" is the only supported type in first version
            if db_data_type == "ByteArray":
                data_type_id = b'\x01'
            # TODO: add more DB data type here
            else:
                msg = 'Unsupported data type: {}'.format(db_data_type)
                throw_error(msg, InvalidParameterException)
                return
            sData = struct.pack(">B", DBPUT_TX_TYPE) + \
                    struct.pack(">H", len(db_key)) + \
                    str2bytes(db_key) + \
                    struct.pack(">H", len(db_data)+1) + \
                    data_type_id + \
                    str2bytes(db_data) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(self.privateKey, sData))
            data = json.dumps({
                  "senderPublicKey": self.publicKey,
                  "dbKey": db_key,
                  "dataType": db_data_type,
                  "data": db_data,
                  "fee": tx_fee,
                  "feeScale": fee_scale,
                  "timestamp": timestamp,
                  "signature": signature
            })

            return self.wrapper.request('/database/broadcast/put', data)

    def register_contract(self, contract, data_stack, description='', tx_fee=DEFAULT_REGISTER_CONTRACT_FEE,
                      fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        return register_contract(self, contract, data_stack, description, tx_fee, fee_scale, timestamp)

    def execute_contract(self, contract_id, func_id, data_stack, attachment='', tx_fee=DEFAULT_EXECUTE_CONTRACT_FEE,
                     fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        return execute_contract(self, contract_id, func_id, data_stack, attachment, tx_fee, fee_scale, timestamp)

    def get_info(self):
        if not (self.address and self.publicKey):
            msg = 'Address required'
            throw_error(msg, MissingAddressException)
            return None
        if not self.publicKey:
            msg = 'Public key and address required'
            throw_error(msg, MissingPublicKeyException)
            return None
        if is_offline():
            info = {
                "publicKey": self.publicKey,
                "address": self.address
            }
            return info
        info = self.balance_detail()
        if not info:
            msg = 'Failed to get balance detail'
            throw_error(msg, NetworkException)
        else:
            info["publicKey"] = self.publicKey
            return info

    def get_tx_history(self, limit=100, type_filter=PAYMENT_TX_TYPE):
        if is_offline():
            throw_error("Cannot check history in offline mode.", NetworkException)
            return []
        if not self.address:
            msg = 'Address required'
            throw_error(msg, MissingAddressException)
        elif limit > MAX_TX_HISTORY_LIMIT:
            msg = 'Too big sequences requested (Max limitation is %d).' % MAX_TX_HISTORY_LIMIT
            throw_error(msg, InvalidParameterException)
        else:
            url = '/transactions/address/{}/limit/{}'.format(self.address, limit)
            resp = self.wrapper.request(url)
            if isinstance(resp, list) and type_filter:
                resp = [tx for tx in resp[0] if tx['type'] == type_filter]
            return resp

    def check_tx(self, tx_id, confirmations=0):
        """Confirm tx on chain.
        Return True if Transaction is fully confirmed.
        Return False if Transaction is sent but not confirmed or failed.
        Return None if Transaction does not exist!
        """
        if is_offline():
            throw_error("Cannot check transaction in offline mode.", NetworkException)
            return None
        utx_res = self.chain.unconfirmed_tx(tx_id)
        if "id" in utx_res:
            # Transaction is pending in UTX pool.
            return False
        else:
            tx_res = self.chain.tx(tx_id)
            if tx_res.get("status") == "Success":
                tx_height = tx_res["height"]
                cur_height = self.chain.height()
                if cur_height >= tx_height + confirmations:
                    # Transaction is fully confirmed.
                    return True
                else:
                    # Transaction is sent but not fully confirmed.
                    return False
            elif "id" not in tx_res:
                # Transaction does not exist!
                return None
            else:
                # Transaction failed to process!
                return False

    def check_node(self, other_node_host=None):
        if is_offline():
            throw_error("Cannot check node in offline mode.", NetworkException)
            return False
        if other_node_host:
            res = self.chain.check_with_other_node(other_node_host)
        else:
            res = self.chain.self_check()
        # add more check if need
        return res

    def get_tx_status(self, tx_id):
        self.check_is_offline()
        if not self.check_tx_is_unconfirmed(tx_id):
            return self.get_tx_attribute(tx_id, 'status')

    def get_tx_height(self, tx_id):
        self.check_is_offline()
        if not self.check_tx_is_unconfirmed(tx_id):
            return self.get_tx_attribute(tx_id, 'height')

    def get_tx_attribute(self, tx_id, attribute):
        tx_res = self.chain.tx(tx_id)
        if 'id' not in tx_res:
            return None
        else:
            return tx_res[attribute]

    def check_tx_is_unconfirmed(self, tx_id):
        utx_res = self.chain.unconfirmed_tx(tx_id)
        if "id" in utx_res:
            throw_error("Transaction {} is pending in UTX pool.".format(tx_id), InvalidStatus)
        else:
            return False

    @staticmethod
    def check_is_offline():
        if is_offline():
            throw_error("Cannot check transaction in offline mode.", NetworkException)
