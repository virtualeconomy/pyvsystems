from requests.exceptions import RequestException
from .errors import NetworkException
import os
import logging
import requests


class Wrapper(object):
    def __init__(self, node_host, api_key=''):
        self.node_host = node_host
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def request(self, api, post_data=''):
        headers = {}
        url = os.path.join(self.node_host, api)
        if self.api_key:
            headers['api_key'] = self.api_key
        header_str = ' '.join(['--header \'{}: {}\''.format(k, v) for k, v in headers.items()])
        try:
            if post_data:
                headers['Content-Type'] = 'application/json'
                data_str = '-d {}'.format(post_data)
                self.logger.info("curl -X POST %s %s %s" % (header_str, data_str, url))
                return requests.post(url, data=post_data, headers=headers).json()
            else:
                self.logger.info("curl -X GET %s %s" % (header_str, url))
                return requests.get(url, headers=headers).json()
        except RequestException as ex:
            msg = 'Failed to get response: {}'.format(ex)
            raise NetworkException(msg)