from fastapi import FastAPI, Response
from typing import Any
import pydantic

from backend.gutenberg.controller import GutenController
from backend.utils.exceptions import APIException
from backend.ai_tools.book_agent import AgentsManager

gutenberg_api = GutenController()
agents_manager = AgentsManager()

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


class ChatRequest(pydantic.BaseModel):
    book_id: int
    message: str


class ChatResponse(pydantic.BaseModel):
    response: str


@app.post("/chat", response_model=ResponseModel)
def chat(request: ChatRequest):

    agent = agents_manager.get_agent(request.book_id)

    try:
        response = agent.chat(request.message)
    except Exception as e:
        print(e)
        return ErrorModel(detail="Error during chat", status_code=500)
    return ResponseModel(detail="Chat response", data=ChatResponse(response=response))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
