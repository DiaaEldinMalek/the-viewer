import requests


class SimpleHTTPResponse:
    def __init__(self, response: requests.Response):
        self.status_code = response.status_code
        self.content = response.content
        self.raw_response = response
        self.__json = None

    @property
    def json(self):
        if self.__json is None:
            self.__json = self.raw_response.json()
        return self.__json

    @property
    def text(self):
        return self.raw_response.text
