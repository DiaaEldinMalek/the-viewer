from fastapi import FastAPI, Response
from backend.gutenberg.controller import GutenController, GutenbergBookContent
from backend.utils.exceptions import APIException
import pydantic
from typing import Any

gutenberg_api = GutenController()

app = FastAPI()


class ResponseModel(pydantic.BaseModel):
    detail: str
    data: Any = None
    status: bool = True
    status_code: int = 200


class ErrorModel(ResponseModel):
    status: bool = False
    status_code: int = 500

    @classmethod
    def from_exception(cls, e: APIException):
        return cls(detail=e.message, status_code=e.status_code)


@app.get("/get_book_content/{id}", response_model=ResponseModel)
def get_book_content(id: int):
    try:
        book_content = gutenberg_api.fetch_book_content(id)
    except APIException as e:
        return ErrorModel(detail=e.message, status_code=e.status_code)

    return ResponseModel(detail=f"Fetched book {id}", data=book_content)


@app.get("/get_book_metadata/{id}", response_model=ResponseModel)
def get_book_metadata(id: int):
    try:
        metadata = gutenberg_api.fetch_book_metadata(id)
    except APIException as e:
        return ErrorModel.from_exception(e)
    return ResponseModel(detail=f"Fetched metadata for book {id}", data=metadata)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
