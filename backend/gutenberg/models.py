from pydantic import BaseModel


class GutenbergBookContent(BaseModel):
    content: str


class BookMetadata(BaseModel):
    metadata: dict
