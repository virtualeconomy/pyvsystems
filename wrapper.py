import logging
import requests
from requests.exceptions import RequestException
from .error import NetworkException


class Wrapper(object):

    def __init__(self, node_host, api_key=''):
        self.node_host = node_host
        self.api_key = api_key

    def request(self, api, post_data=''):
        global OFFLINE
        if OFFLINE:
            offlineTx = {}
            offlineTx['api-type'] = 'POST' if post_data else 'GET'
            offlineTx['api-endpoint'] = api
            offlineTx['api-data'] = post_data
            return offlineTx
        headers = {}
        url = self.node_host + api
        if self.api_key:
            headers['api_key'] = self.api_key
        header_str = ' '.join(['--header \'{}: {}\''.format(k, v) for k, v in headers.items()])
        try:
            if post_data:
                headers['Content-Type'] = 'application/json'
                data_str = '-d {}'.format(post_data)
                logging.info("curl -X POST %s %s %s" % (header_str, data_str, url))
                return requests.post(url, data=post_data, headers=headers).json()
            else:
                logging.info("curl -X GET %s %s" % (header_str, url))
                return requests.get(url, headers=headers).json()
        except RequestException as ex:
            msg = 'Failed to get response: {}'.format(ex)
            raise NetworkException(msg)
