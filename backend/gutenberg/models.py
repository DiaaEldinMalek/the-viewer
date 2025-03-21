from pydantic import BaseModel


class BookContent(BaseModel):
    content: str


class BookMetadata(BaseModel):
    metadata: dict
