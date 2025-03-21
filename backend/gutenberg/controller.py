from backend.utils.exceptions import APIException

from .dao import GutenbergDAO
from .models import BookContent, BookMetadata
import bs4


class GutenController:
    """Controller is the public API for this module. It handles validation & serialization (data conversion),
    error handling, retrying, business requirements, etc."""

    def __init__(self):
        self.dao = GutenbergDAO()

    def fetch_book_content(self, book_id: str | int):
        try:
            response = self.dao.fetch_book_content(book_id)
            return BookContent(content=response.content)
        except Exception as e:
            raise APIException(e)

    def fetch_book_metadata(self, book_id: str | int, *fields: str):
        response = self.dao.fetch_book_metadata(book_id)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        metadata = soup.find("table", {"class": "bibrec"}).find_all("tr")
        metadata_dict = {}
        for row in metadata:
            try:
                key = row.find("th").text.strip()
                value = row.find("td").text.strip()
                metadata_dict[key] = value
            except:
                print(row)
        return BookMetadata(metadata=metadata_dict)
