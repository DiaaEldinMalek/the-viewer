import requests
import os


class SimpleHTTPResponse:
    def __init__(self, response: requests.Response):
        self.status_code = response.status_code
        self.content = response.content
        self.__json = None
        self.__raw_response = response

    @property
    def json(self):
        if self.__json is None:
            self.__json = self.__raw_response.json()
        return self.__json


class GutenbergDAO:
    """The data access object communicates directly with the source data (API/Database, etc.) and returns a predictable schema.
    Essentially, it's just a wrapper over the `requests` library but designed for this specific data source (in this case, Gutenberg)
    """

    def __init__(self):
        self.base_url = f"https://www.gutenberg.org"

    # TODO: implement retry mechanism decorator in case of network failures
    def fetch_book_content(self, book_id: int):
        url = self.base_url + f"/cache/epub/{book_id}/pg{book_id}.txt"
        response = requests.get(url)
        return SimpleHTTPResponse(response)

    def fetch_book_metadata(self, book_id: int):
        url = self.base_url + f"/ebooks/{book_id}"
        response = requests.get(url)
        return SimpleHTTPResponse(response)
