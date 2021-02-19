from .setting import *
from .crypto import *
from .error import *
from .words import WORDS
from .contract import serialize_data
from . import is_offline
from . import default_chain
import time
import struct
import json
import base58


class Account(object):
    def __init__(self, chain=default_chain(), address='', public_key='', private_key='', seed='', nonce=0):
        """Constructor.
        """
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
        else:
            self._generate(nonce=nonce)

    def __str__(self):
        """Returns readable representation.
        """
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
            raise NetworkException("Cannot check height in offline mode.")
        else:
            confirmations_str = '' if confirmations == 0 else '/%d' % confirmations
            resp = self.wrapper.request('addresses/balance/%s%s' % (self.address, confirmations_str))
            return resp['balance']

    def balance_detail(self):
        try:
            resp = self.wrapper.request('addresses/balance/details/%s' % self.address)
            return resp
        except Exception as ex:
            msg = "Failed to get balance detail. ({})".format(ex)
            raise NetworkException(msg)

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
            seedHash = hashChain(str2bytes(str(nonce) + self.seed))
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

    def _check(self, tx_fee, fee_scale, address=None, amount=None, attachment=None, lease_id=None, slot_id=None,
               db_key=None, default_fee=DEFAULT_PAYMENT_FEE):
        if not self.privateKey:
            raise MissingPrivateKeyException('Private key required')
        elif address and not self.chain.validate_address(address):
            raise InvalidAddressException('Invalid recipient address')
        elif amount and amount < 0:
            raise InvalidParameterException('Amount must be >= 0')
        elif attachment and len(attachment) > MAX_ATTACHMENT_SIZE:
            raise InvalidParameterException('Attachment length must be <= %d' % MAX_ATTACHMENT_SIZE)
        elif lease_id and len(base58.b58decode(lease_id)) != LEASE_TX_ID_BYTES:
            raise InvalidParameterException('Invalid lease transaction id')
        elif slot_id and (slot_id >= 60 or slot_id < 0):
            raise InvalidParameterException('Slot id must be in 0 to 59')
        elif db_key and (len(db_key) > MAX_DB_KEY_SIZE or len(db_key) < MIN_DB_KEY_SIZE):
            raise InvalidParameterException('DB key length must be greater than %d and smaller than %d'
                                            % (MIN_DB_KEY_SIZE, MAX_ATTACHMENT_SIZE))
        elif tx_fee < default_fee:
            raise InvalidParameterException('Transaction fee must be >= %d' % default_fee)
        elif CHECK_FEE_SCALE and fee_scale != DEFAULT_FEE_SCALE:
            raise InvalidParameterException('Wrong fee scale (currently, fee scale must be %d).' % DEFAULT_FEE_SCALE)
        elif not is_offline() and amount and self.balance() < amount + tx_fee:
            raise InsufficientBalanceException('Insufficient VSYS balance')
        else:
            return True

    def sign(self, sData):
        if not self.privateKey:
            raise MissingPrivateKeyException('Private key required')
        return bytes2str(sign(self.privateKey, base58.b58decode(sData)))

    def send_payment(self, recipient, amount, attachment='', tx_fee=DEFAULT_PAYMENT_FEE, fee_scale=DEFAULT_FEE_SCALE,
                     timestamp=0):
        if self._check(tx_fee, fee_scale, address=recipient.address, amount=amount, attachment=attachment):
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
            return self.wrapper.request('vsys/broadcast/payment', data)

    def lease(self, recipient, amount, tx_fee=DEFAULT_LEASE_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if self._check(tx_fee, fee_scale, address=recipient.address, amount=amount):
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
            return self.wrapper.request('leasing/broadcast/lease', data)

    def cancel_lease(self, lease_id, tx_fee=DEFAULT_CANCEL_LEASE_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if self._check(tx_fee, fee_scale, amount=0, lease_id=lease_id):
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", LEASE_CANCEL_TX_TYPE) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp) + \
                    base58.b58decode(lease_id)
            signature = bytes2str(sign(self.privateKey, sData))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "txId": lease_id,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "signature": signature
            })
            req = self.wrapper.request('leasing/broadcast/cancel', data)
            return req

    def contend(self, slot_id, tx_fee=DEFAULT_CONTEND_SLOT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if self._check(tx_fee, fee_scale, slot_id=slot_id, default_fee=DEFAULT_CONTEND_SLOT_FEE):
            if not is_offline():
                balance_detail = self.get_info()
                min_effective_balance = MIN_CONTEND_SLOT_BALANCE + tx_fee
                if balance_detail["effective"] < min_effective_balance:
                    raise InvalidParameterException('Insufficient VSYS balance. (The effective balance must be >= %d)'
                                                    % min_effective_balance)
                slot_info = self.chain.slot_info(slot_id)
                if not slot_info or slot_info.get("mintingAverageBalance") is None:
                    raise NetworkException('Failed to get slot minting average balance')
                elif slot_info["mintingAverageBalance"] >= balance_detail["mintingAverage"]:
                    raise InsufficientBalanceException(
                        'The minting average balance of slot %d is greater than or equals '
                        'to yours. You will fail in contending this slot.' % slot_id)
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
            return self.wrapper.request('spos/broadcast/contend', data)

    def release(self, slot_id, tx_fee=DEFAULT_RELEASE_SLOT_FEE, fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if self._check(tx_fee, fee_scale, amount=0, slot_id=slot_id):
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
            return self.wrapper.request('spos/broadcast/release', data)

    def dbput(self, db_key, db_data, db_data_type="ByteArray", tx_fee=DEFAULT_DBPUT_FEE, fee_scale=DEFAULT_FEE_SCALE,
              timestamp=0):
        if self._check(tx_fee, fee_scale, amount=0, db_key=db_key, default_fee=DEFAULT_DBPUT_FEE):
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            # "ByteArray" is the only supported type in first version
            if db_data_type == "ByteArray":
                data_type_id = b'\x01'
            # TODO: add more DB data type here
            else:
                raise InvalidParameterException('Unsupported data type: {}'.format(db_data_type))
            sData = struct.pack(">B", DBPUT_TX_TYPE) + \
                    struct.pack(">H", len(db_key)) + \
                    str2bytes(db_key) + \
                    struct.pack(">H", len(db_data) + 1) + \
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
            return self.wrapper.request('database/broadcast/put', data)

    def register_contract(self, contract, data_stack, description='', tx_fee=DEFAULT_REGISTER_CONTRACT_FEE,
                          fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if self._check(tx_fee, fee_scale, amount=0, default_fee=DEFAULT_REGISTER_CONTRACT_FEE):
            data_stack_bytes = serialize_data(data_stack)
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", REGISTER_CONTRACT_TX_TYPE) + \
                    struct.pack(">H", len(contract.bytes)) + \
                    contract.bytes + \
                    struct.pack(">H", len(data_stack_bytes)) + \
                    data_stack_bytes + \
                    struct.pack(">H", len(description)) + \
                    str2bytes(description) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(self.privateKey, sData))
            description_str = description
            data_stack_str = bytes2str(base58.b58encode(data_stack_bytes))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "contract": bytes2str(base58.b58encode(contract.bytes)),
                "initData": data_stack_str,
                "description": description_str,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "signature": signature
            })
            return self.wrapper.request('contract/broadcast/register', data)

    def execute_contract(self, contract_id, func_id, data_stack, attachment='', tx_fee=DEFAULT_EXECUTE_CONTRACT_FEE,
                         fee_scale=DEFAULT_FEE_SCALE, timestamp=0):
        if self._check(tx_fee, fee_scale, amount=0, default_fee=DEFAULT_EXECUTE_CONTRACT_FEE):
            data_stack_bytes = serialize_data(data_stack)
            if timestamp == 0:
                timestamp = int(time.time() * 1000000000)
            sData = struct.pack(">B", EXECUTE_CONTRACT_FUNCTION_TX_TYPE) + \
                    base58.b58decode(contract_id) + \
                    struct.pack(">H", func_id) + \
                    struct.pack(">H", len(data_stack_bytes)) + \
                    data_stack_bytes + \
                    struct.pack(">H", len(attachment)) + \
                    str2bytes(attachment) + \
                    struct.pack(">Q", tx_fee) + \
                    struct.pack(">H", fee_scale) + \
                    struct.pack(">Q", timestamp)
            signature = bytes2str(sign(self.privateKey, sData))
            description_str = bytes2str(base58.b58encode(str2bytes(attachment)))
            data_stack_str = bytes2str(base58.b58encode(data_stack_bytes))
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "contractId": contract_id,
                "functionIndex": func_id,
                "functionData": data_stack_str,
                "attachment": description_str,
                "fee": tx_fee,
                "feeScale": fee_scale,
                "timestamp": timestamp,
                "signature": signature
            })
            return self.wrapper.request('contract/broadcast/execute', data)

    def get_info(self):
        if not (self.address and self.publicKey):
            raise MissingAddressException('Address and Public key required')
        if is_offline():
            info = {
                "publicKey": self.publicKey,
                "address": self.address
            }
            return info
        info = self.balance_detail()
        if not info:
            raise NetworkException('Failed to get balance detail')
        else:
            info["publicKey"] = self.publicKey
            return info

    def get_tx_history(self, limit=100, type_filter=PAYMENT_TX_TYPE):
        if is_offline():
            raise NetworkException("Cannot check history in offline mode.")
        if not self.address:
            raise MissingAddressException('Address required')
        elif limit > MAX_TX_HISTORY_LIMIT:
            raise InvalidParameterException('Too big sequences requested (Max limitation is %d).' % MAX_TX_HISTORY_LIMIT)
        else:
            url = 'transactions/address/{}/limit/{}'.format(self.address, limit)
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
            raise NetworkException("Cannot check transaction in offline mode.")
        utx_res = self.chain.unconfirmed_tx(tx_id)
        if "id" in utx_res:
            # The transaction is pending in UTX pool.
            return False
        else:
            tx_res = self.chain.tx(tx_id)
            if tx_res.get("status") == "Success":
                tx_height = tx_res["height"]
                cur_height = self.chain.height()
                if cur_height >= tx_height + confirmations:
                    # The transaction is fully confirmed.
                    return True
                else:
                    # The transaction is sent but not fully confirmed.
                    return False
            elif "id" not in tx_res:
                # Transaction does not exist!
                return None
            else:
                # Transaction failed to process!
                return False

    def check_node(self, other_node_host=None):
        if is_offline():
            raise NetworkException("Cannot check transaction in offline mode.")
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
            raise InvalidStatus("Transaction {} is pending in UTX pool.".format(tx_id))
        else:
            return False

    @staticmethod
    def check_is_offline():
        if is_offline():
            raise NetworkException("Cannot check transaction in offline mode.")