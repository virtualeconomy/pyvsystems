from requests.exceptions import RequestException
from .error import NetworkException
import os
import requests


class Wrapper(object):
    def __init__(self, node_host, api_key='', timeout=None):
        self.node_host = node_host
        self.api_key = api_key
        self.timeout = timeout

    def request(self, api, post_data=''):
        headers = {}
        url = os.path.join(self.node_host, api)
        if self.api_key:
            headers['api_key'] = self.api_key
        try:
            if post_data:
                headers['Content-Type'] = 'application/json'
                if self.timeout:
                    return requests.post(url, data=post_data, headers=headers, timeout=self.timeout).json()
                else:
                    return requests.post(url, data=post_data, headers=headers).json()
            else:
                if self.timeout:
                    resp = requests.get(url, headers=headers, timeout=self.timeout)
                    return resp.json()
                else:
                    resp = requests.get(url, headers=headers)
                    return resp.json()
        except RequestException as ex:
            msg = 'Failed to get response: {}'.format(ex)
            raise NetworkException(msg)