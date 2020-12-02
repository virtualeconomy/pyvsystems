import logging
import requests
from requests.exceptions import RequestException
from .error import NetworkException
from . import is_offline


class Wrapper(object):

    def __init__(self, node_host, api_key='', timeout=None):
        self.node_host = node_host
        self.api_key = api_key
        self.timeout = timeout

    def request(self, api, post_data=''):
        if is_offline():
            offline_tx = {}
            offline_tx['api-type'] = 'POST' if post_data else 'GET'
            offline_tx['api-endpoint'] = api
            offline_tx['api-data'] = post_data
            return offline_tx
        headers = {}
        url = self.node_host + api
        if self.api_key:
            headers['api_key'] = self.api_key
        header_str = ' '.join(['--header \'{}: {}\''.format(k, v) for k, v in headers.items()])
        try:
            if post_data:
                headers['Content-Type'] = 'application/json'
                if self.timeout:
                    return requests.post(url, data=post_data, headers=headers, timeout=self.timeout).json()
                else:
                    return requests.post(url, data=post_data, headers=headers).json()
            else:
                if self.timeout:
                    return requests.get(url, headers=headers, timeout=self.timeout).json()
                else:
                    return requests.get(url, headers=headers).json()
        except RequestException as ex:
            msg = 'Failed to get response: {}'.format(ex)
            raise NetworkException(msg)
