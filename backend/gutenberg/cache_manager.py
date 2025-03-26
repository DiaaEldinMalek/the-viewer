import pathlib
import json
from typing import Optional
from .utils.clean_book_content import clean_gutenberg_file


class _BaseManager:
    def __init__(self):
        self.cache_dir = pathlib.Path("cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def create_book_folder(self, book_id: int):
        book_path = self.cache_dir.joinpath(str(book_id))
        book_path.mkdir(parents=True, exist_ok=True)


class CachedContentManager(_BaseManager):

    def _get_content_path(self, book_id: int, *, cleaned: bool) -> pathlib.Path:
        filename = "cleaned_content.txt" if cleaned else "content.txt"
        return self.cache_dir.joinpath(str(book_id)).joinpath(filename)

    def get_book_content(
        self,
        book_id: int,
        *,
        cleaned: bool,
    ) -> Optional[str]:

        # If the cleaned copy is requested, create it if it doesn't exist

        # Reads and returns the copy
        content_path = self._get_content_path(book_id, cleaned=cleaned)
        try:
            if cleaned:
                self._create_cleaned_copy(book_id)

            with open(content_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def save_book_content(
        self,
        book_id: int,
        content: str,
        *,
        folder_checked: bool = False,
    ):
        if not folder_checked:
            self.create_book_folder(book_id)

        content_path = self._get_content_path(book_id, cleaned=False)

        with open(content_path, "w") as f:
            f.write(content)

        self._create_cleaned_copy(book_id)

    def _create_cleaned_copy(self, book_id: int):
        content_path = self._get_content_path(book_id, cleaned=False)
        cleaned_content_path = self._get_content_path(book_id, cleaned=True)
        clean_gutenberg_file(content_path, cleaned_content_path)
        return cleaned_content_path


class CachedMetadataManager(_BaseManager):

    def _get_metadata_path(self, book_id: int) -> pathlib.Path:
        return self.cache_dir.joinpath(str(book_id)).joinpath("metadata.json")

    def get_book_metadata(self, book_id: int) -> Optional[dict]:
        metadata_path = self._get_metadata_path(book_id)

        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def save_book_metadata(
        self, book_id: int, metadata: dict, *, folder_checked: bool = False
    ):
        if not folder_checked:
            self.create_book_folder(book_id)

        metadata_path = self._get_metadata_path(book_id)

        with open(metadata_path, "w") as f:
            json.dump(metadata, f)


class CachedSummaryManager(_BaseManager):
    def _get_summary_path(self, book_id: int) -> pathlib.Path:
        return self.cache_dir.joinpath(str(book_id)).joinpath("summary.txt")

    def get_book_summary(self, book_id: int) -> Optional[str]:
        summary_path = self._get_summary_path(book_id)

        try:
            with open(summary_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def save_book_summary(
        self, book_id: int, summary: str, *, folder_checked: bool = False
    ):
        if not folder_checked:
            self.create_book_folder(book_id)

        summary_path = self._get_summary_path(book_id)

        with open(summary_path, "w") as f:
            f.write(summary)


class GutenbergCacheManager(
    CachedContentManager,
    CachedMetadataManager,
    CachedSummaryManager,
):
    pass
