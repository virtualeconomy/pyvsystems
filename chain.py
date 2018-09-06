from wrapper import Wrapper

class Chain(object):

	def __init__(self, chain_name, chain_id, api_node_url, api_key):
		self.chain_name = chain_name
		self.chain_id = chain_id
		self.api_node_url = api_node_url
		self.api_key = api_key

	def api_get(self, api_path):
		return Wrapper(self.api_node_url, self.api_key).request(api_path)

	def height(self):
	    return self.api_get('/blocks/height')['height']

	def lastblock(self):
	    return self.api_get('/blocks/last')

	def block(self, n):
	    return self.api_get('/blocks/at/%d' % n)

	def tx(self, id):
	    return self.api_get('/transactions/info/%s' % id)