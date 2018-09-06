from __future__ import absolute_import, division, print_function, unicode_literals

ogging.getLogger("requests").setLevel(logging.WARNING)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


from .address import *
from .chain import *

def testnet_chain(api_node_url='', api_key=''):
    if api_node_url:
        return Chain('testnet', 'T', api_node_url, api_key)
    else: 
        return Chain( ,api_node_url, api_key)