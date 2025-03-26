from pydantic import BaseModel

from backend.utils.exceptions import NotFoundError
from .dao import GutenbergDAO
from .models import GutenbergBookContent, BookMetadata
from .cache_manager import GutenbergCacheManager
from .utils.parse_metadata_from_landing_page import parse_metada_from_html
from .utils.clean_book_content import clean_gutenberg_file


class FetchOptions(BaseModel):
    from_cache: bool = True


class ContentOptions(FetchOptions):
    cleaned: bool = True


class MetadataOptions(FetchOptions):
    pass


class GutenController:
    """Controller is the public API for this module. It handles validation & serialization (data conversion),
    error handling, retrying, business requirements, etc.
    It does so by coordinating the DAO and CacheManager to fetch and store data."""

    def __init__(self):
        self.dao = GutenbergDAO()
        self.cache_manager = GutenbergCacheManager()

    def fetch_book_content(
        self, book_id: int, options: ContentOptions = ContentOptions()
    ):
        """Fetches the textual content of a book from the Gutenberg project.
        Args:
            book_id (int): The ID of the book to fetch.
            from_cache (bool): If True, will first check the cache for the content.
            cache (bool): If True, will cache the content after fetching it (from the website).
        """

        if options.from_cache and (
            content := self.cache_manager.get_book_content(
                book_id, cleaned=options.cleaned
            )
        ):
            return GutenbergBookContent(content=content)

        response = self.dao.fetch_book_content(book_id)

        if response.status_code == 404:
            raise NotFoundError(
                f"Textual content for book with id {book_id} not found. Might be unavailable or an audiobook."
            )

        # Store raw data in cache. the cache manager
        # automatically creates a cleaned copy on disk
        self.cache_manager.save_book_content(book_id, response.text)

        # If the cleaned data is request, fetch it from the cache manager
        if options.cleaned:
            content = self.cache_manager.get_book_content(
                book_id, cleaned=options.cleaned
            )

            if not content:
                raise NotFoundError(
                    f"Cleaned content for book with id {book_id} not found."
                )
        else:  # Otherwise, return the data as is
            content = response.text

        return GutenbergBookContent(content=content)

    def fetch_book_metadata(
        self,
        book_id: int,
        *,
        from_cache=True,
        cache=True,
    ):
        """Fetches the metadata of a book from the Gutenberg project.
        Args:
            book_id (int): The ID of the book to fetch.
            from_cache (bool): If True, will first check the cache for the metadata.
            cache (bool): If True, will cache the metadata after fetching it (from the website).
        """

        if from_cache and (metadata := self.cache_manager.get_book_metadata(book_id)):
            return BookMetadata(metadata=metadata)

        response = self.dao.fetch_book_metadata(book_id)

        try:
            metadata = parse_metada_from_html(response.content)
        except:
            raise NotFoundError(f"Metadata for book with id {book_id} not found.")

        if cache:
            self.cache_manager.save_book_metadata(book_id, metadata)
        return BookMetadata(metadata=metadata)
