from requests.exceptions import RequestException
from .error import NetworkException
import requests


class Wrapper(object):
    def __init__(self, node_host, api_key="", timeout=None):
        self.node_host = node_host
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if self.api_key:
            self.session.headers.update({"api_key": self.api_key})
        if timeout:
            self.session.timeout = timeout

    def request(self, api, post_data=""):
        url = self.node_host + "/" + api
        try:
            if post_data:
                return self.session.post(url, data=post_data).json()
            else:
                return self.session.get(url).json()

        except RequestException as ex:
            msg = "Failed to get response: {}".format(ex)
            raise NetworkException(msg)
