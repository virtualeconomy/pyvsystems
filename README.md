# pyvee
A python wrapper for vee api

## install
For now, 
1. just clone the repo under you workspace 
2. install packages in pyvee/requirement.txt by 
```pip install -r ./pyvee/requirements.txt```
3. Then you can ```import pyvee```

## usage

### chain
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

### chain api
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


### address
