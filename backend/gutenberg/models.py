from typing import Any
from pydantic import BaseModel


class BookContent(BaseModel):
    title: str
    author: str
    content: str

    @classmethod
    def load_with_metadata(cls, content: str, metadata: "BookMetadata"):
        return cls(
            title=metadata.metadata["title"],
            author=metadata.metadata.get("author", "Unknown"),
            content=content,
        )


class BookMetadata(BaseModel):
    metadata: dict[str, str]

    def model_post_init(self, __context: Any) -> None:
        self.metadata = {key.lower(): val for key, val in self.metadata.items()}
        return super().model_post_init(__context)
