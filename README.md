# pyvee
A python wrapper for vee api

## Install
For now, 
1. clone the repo under you workspace
2. install packages in pyvee/requirement.txt by 
```pip install -r ./pyvee/requirements.txt```
3. Then you can ```import pyvee``` in your workspace

## Usage

### chain object
1. For testnet:
    ```python
    import pyvee as pv
    ts_chain = pv.testnet_chain()
    ```
2. For default chain:
    ```python
    import pyvee as pv
    main_chain = pv.default_chain()
    ```

3. For custom api node:
    ```python
    import pyvee as pv
    custom_wrapper = pv.create_api_wrapper('http://0.0.0.0/', api_key='')
    ts_chain = pv.testnet_chain(custom_wrapper)
    ```

4. For completely custom chain:
    ```python
    import pyvee as pv
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
    from pyvee import Address
    my_address = Address(chain=ts_chain, seed='<your seed>', nonce=0)
    ```
2. constructed by private key
    ```python
    from pyvee import Address
    my_address = Address(chain=ts_chain, private_key='<your base58 private key>')
    ```
3. constructed by public key
    ```python
    from pyvee import Address
    recipient = Address(chain=ts_chain, public_key='<base58 public key>')
    ```
4. constructed by wallet address
    ```python
    from pyvee import Address
    recipient = Address(chain=ts_chain, address='<base58 wallet address>')
    ```
 
### address api list
1. Get balance
    ```python
    # get VEE balance
    balance = my_address.balance()
    print("The balance is {}".format(balance))
    # get VEE balance after 5 confirmations 
    balance = my_address.balance(confirmations = 5)
    print("The balance is {}".format(balance))
    ```
2. Send payment transaction
    ```python
    # send payment (100000000 = 1 VEE)
    my_address.send_payment(recipient, amount=100000000)
    ```
3. Send and cancel lease transaction
    ```python
    # send lease (100000000 = 1 VEE)
    response = my_address.lease(recipient, amount=100000000)
    tx_id = response["id"]
    # cancel lease
    my_address.lease_cancel(tx_id)
    ```
