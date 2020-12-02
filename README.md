# pyvsystems
A python wrapper for vsys api.

For more detail, please refer:

[PYVSYSTEMS User Guide Specification (English)](https://github.com/virtualeconomy/pyvsystems/wiki/PYVSYSTEMS-User-Guide-Specification-%28English%29)

[PYVSYSTEMS 使用详细指南(中文)](https://github.com/virtualeconomy/pyvsystems/wiki/PYVSYSTEMS-使用详细指南%28中文%29)

## Install

Library can be pulled via pip directly:

```git+https://github.com/virtualeconomy/pyvsystems.git```

Or:

1. clone the repo under you workspace
```git clone https://github.com/virtualeconomy/pyvsystems.git```
2. install the package 
```pip3 install pyvsystems/.```
3. Then you can  ```import pyvsystems```  in your workspace

## Usage

### chain object
1. For testnet:
    ```python
    import pyvsystems as pv
    ts_chain = pv.testnet_chain()
    ```
2. For default chain:
    ```python
    import pyvsystems as pv
    main_chain = pv.default_chain()
    ```

3. For custom api node:
    ```python
    import pyvsystems as pv
    # you can set the request timeout
    custom_wrapper = pv.create_api_wrapper('http://<full node ip>:9922', api_key='', timeout=None)
    ts_chain = pv.testnet_chain(custom_wrapper)
    ```

4. For completely custom chain:
    ```python
    import pyvsystems as pv
    custom_wrapper = pv.create_api_wrapper('http://<full node ip>:9922', api_key='',  timeout=None))
    t_chain = pv.Chain(chain_name='testnet', chain_id='T', address_version=5, api_wrapper=custom_wrapper)
    custom_wrapper2 = pv.create_api_wrapper('http://<full node ip>:9922', api_key='',  timeout=None))
    m_chain = pv.Chain(chain_name='mainnet', chain_id='M', address_version=5, api_wrapper=custom_wrapper2)
    custom_wrapper3 = pv.create_api_wrapper('http://<full node ip>:9922', api_key='',  timeout=None))
    c_chain = pv.Chain(chain_name='mychain', chain_id='C', address_version=1, api_wrapper=custom_wrapper3)
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
    from pyvsystems import Account
    my_address = Account(chain=ts_chain, seed='<your seed>', nonce=0)
    ```
2. constructed by private key
    ```python
    from pyvsystems import Account
    my_address = Account(chain=ts_chain, private_key='<your base58 private key>')
    ```
3. constructed by public key
    ```python
    from pyvsystems import Account
    recipient = Account(chain=ts_chain, public_key='<base58 public key>')
    ```
4. constructed by wallet address
    ```python
    from pyvsystems import Account
    recipient = Account(chain=ts_chain, address='<base58 wallet address>')
    ```
 
### address api list
1. Get balance
    ```python
    # get balance
    balance = my_address.balance()
    print("The balance is {}".format(balance))
    # get balance after 16 confirmations 
    balance = my_address.balance(confirmations = 16)
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
    
[Sample code for Send Transaction](https://github.com/virtualeconomy/pyvsystems/wiki/PYVSYSTEMS-User-Guide-Specification-%28English%29#sample-code) for reference

[Sample Code for Smart Contract](https://github.com/virtualeconomy/pyvsystems/wiki/Sample-Code-for-Smart-Contract) for reference

[Sample Code for Exchange](https://github.com/virtualeconomy/pyvsystems/wiki/Sample-Code-for-Exchange) for reference
