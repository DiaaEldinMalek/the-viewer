from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import pydantic
import logging
from threading import Thread

from backend.gutenberg.controller import GutenController
from backend.utils.exceptions import APIException
from backend.ai_tools.book_agent import AgentsManager

gutenberg_api = GutenController()
agents_manager = AgentsManager()
logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_origin_regex="https://*.ngrok-free.app",
)


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
async def get_book_content(id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(agents_manager.get_agent, id)

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

    def attach_response(self, response: str):
        return ChatResponse(
            book_id=self.book_id, message=self.message, response=response
        )


class ChatResponse(ChatRequest):
    response: str


@app.post("/chat", response_model=ResponseModel)
def chat(request: ChatRequest):

    agent = agents_manager.get_agent(request.book_id)

    try:
        response = agent.chat(request.message)
        data = request.attach_response(response)
        logging.info(data)
    except Exception as e:
        logging.exception(e)
        return ErrorModel(detail="Error during chat", status_code=500)
    return ResponseModel(detail="Chat response", data=data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
