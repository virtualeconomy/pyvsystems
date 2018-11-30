# pyvsys
A python wrapper for vsys api

## Install
For now, 
1. clone the repo under you workspace
2. install packages in pyvsys/requirement.txt by 
```pip install -r ./pyvsys/requirements.txt```
3. Then you can ```import pyvsys``` in your workspace

## Usage

### chain object
1. For testnet:
    ```python
    import pyvsys as pv
    ts_chain = pv.testnet_chain()
    ```
2. For default chain:
    ```python
    import pyvsys as pv
    main_chain = pv.default_chain()
    ```

3. For custom api node:
    ```python
    import pyvsys as pv
    custom_wrapper = pv.create_api_wrapper('http://0.0.0.0/', api_key='')
    ts_chain = pv.testnet_chain(custom_wrapper)
    ```

4. For completely custom chain:
    ```python
    import pyvsys as pv
    custom_wrapper = pv.create_api_wrapper('http://0.0.0.0/', api_key='')
    ts_chain = pv.Chain(chain_name='aaa', chain_id='aaa', address_version=1, api_wrapper=custom_wrapper)
    ```

### chain api list
1. look up current block height of the chain:
    ```python
    ts_chain.height()
    ```

2. look up the last block info of the chain:
    ```python
    ts_chain.lastblock()
    ```


3. look up a block info at n in the chain:
    ```python
    ts_chain.block(n)
    ```

4. Get a transaction info by transacion id in the chain:
    ```python
    ts_chain.tx(tx_id)
    ```
    
5. Validate an address of the chain:
    ```python
    ts_chain.validate_address(addr)
    ```

### address object
1. constructed by seed
    ```python
    from pyvsys import Account
    my_address = Account(chain=ts_chain, seed='<your seed>', nonce=0)
    ```
2. constructed by private key
    ```python
    from pyvsys import Account
    my_address = Account(chain=ts_chain, private_key='<your base58 private key>')
    ```
3. constructed by public key
    ```python
    from pyvsys import Account
    recipient = Account(chain=ts_chain, public_key='<base58 public key>')
    ```
4. constructed by wallet address
    ```python
    from pyvsys import Account
    recipient = Account(chain=ts_chain, address='<base58 wallet address>')
    ```
 
### address api list
1. Get balance
    ```python
    # get VSYS balance
    balance = my_address.balance()
    print("The balance is {}".format(balance))
    # get VSYS balance after 5 confirmations 
    balance = my_address.balance(confirmations = 5)
    print("The balance is {}".format(balance))
    ```
2. Send payment transaction
    ```python
    # send payment (100000000 = 1 VSYS)
    my_address.send_payment(recipient, amount=100000000)
    ```
3. Send and cancel lease transaction
    ```python
    # send lease (100000000 = 1 VSYS)
    response = my_address.lease(recipient, amount=100000000)
    tx_id = response["id"]
    # cancel lease
    my_address.lease_cancel(tx_id)
    ```
    
### Sample Code

```python
import datetime
import pyvsys as pv
from pyvsys import Account
from pyvsys.error import *


def test_payment():
    # set chain
    ts_chain = pv.testnet_chain()

    # get block height
    try:
        height = ts_chain.height()
        print("The current block height of the chain: {}".format(height))
    except NetworkException as ex:
        # Handle Network issue here
        print("Failed to get block height: {}".format(ex))
        return False

    # create / restore account
    try:
        # retrieve account by private key
        private_key = "XXXXXXXXXX"
        my_account = Account(chain=ts_chain, private_key=private_key)
        # create recipient with address
        recipient_address = "XXXXXXXXXXXXXXXXX"
        recipient = Account(chain=ts_chain, address=recipient_address)
    except InvalidParameterException as ex:
        # Handle Invalid Parameter issue here
        print("Invalid Parameter: {}".format(ex))
        return False
    except InvalidAddressException as ex:
        # Handle Invalid Address issue here
        print("Invalid Address: {}".format(ex))
        return False

    # send payment (100000000 = 1 VSYS)
    try:
        print("========Do payment transaction===========")
        resp = my_account.send_payment(recipient, amount=100000000)
        print("Payment TX result: {}".format(resp))
        print("Transaction ID: {}".format(resp['id']))
        display_time = datetime.datetime.fromtimestamp(resp['timestamp'] // 1000000000)
        print("Time: {}".format(display_time))
        sender_public_key = resp['proofs'][0]['publicKey']
        sender_address = ts_chain.public_key_to_address(sender_public_key)
        print("From: {}".format(sender_address))
        print("To: {}".format(resp['recipient']))
        print("Amount: {}".format(resp['amount']))
        print("Transaction fee: {}".format(resp['fee']))
    except InvalidParameterException as ex:
        # Handle Invalid Parameter issue here
        print("Invalid Parameter: {}".format(ex))
        return False
    except MissingPrivateKeyException:
        # Handle Missing Private Key issue here
        print("No private key for `my_account`")
        return False
    except InvalidAddressException as ex:
        # Handle Invalid Address issue here
        print("Invalid Address: {}".format(ex))
        return False
    except InsufficientBalanceException:
        # Handle Insufficient Balance issue here
        print("Insufficient Balance.")
        return False
    except NetworkException as ex:
        # Handle Network issue here
        print("Failed to get HTTP response: {}".format(ex))
        return False

    # check payment history
    try:
        print("========Check payment history===========")
        history = my_account.get_tx_history(10)
        print("Payment history: {}".format(history))
        for record in history:
            sender_public_key = resp['proofs'][0]['publicKey']
            sender_address = ts_chain.public_key_to_address(sender_public_key)
            if sender_address == my_account.address:
                print("####### Send #######")
            else:
                print("####### Received #######")
            print("From: {}".format(sender_address))
            print("To: {}".format(record['recipient']))
            print("Transaction ID: {}".format(record['id']))
            display_time = datetime.datetime.fromtimestamp(resp['timestamp'] // 1000000000)
            print("Time: {}".format(display_time))
            print("Amount: {}".format(record['amount']))
            print("Transaction fee: {}".format(record['fee']))
    except InvalidParameterException as ex:
        # Handle Invalid Parameter issue here
        print("Invalid Parameter: {}".format(ex))
        return False
    except MissingAddressException:
        # Handle Address issue here
        print("No address for `my_account`")
        return False
    except NetworkException as ex:
        # Handle Network issue here
        print("Failed to get HTTP response: {}".format(ex))
        return False
    return True


if __name__ == "__main__":
    test_payment()
```
