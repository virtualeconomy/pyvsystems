import logging
import requests

class Wrapper(object):

    def __init__(self, node_host, api_key=''):
        self.node_host = node_host
        self.api_key = api_key

    def request(self, api, post_data=''):
        headers = {}
        url = self.node_host + api
        if self.api_key:
            headers['api_key'] = self.api_key 
        if post_data:
            headers['Content-Type'] = 'application/json'
            header_str = ' '.join(['--header \'{}: {}\''.format(k, v) for k, v in headers.items()])
            data_str = '-d {}'.format(post_data)
            logging.info("curl -X POST %s %s" % (header_str, data_str))
            return requests.post(url, data=post_data, headers=headers).json()
        else:
            logging.info("curl -X GET %s" % (' '.join(['--header \'{}\': \'{}\''.format(k, v) for k, v in headers.items()])))
            return requests.get(url, headers=headers).json()