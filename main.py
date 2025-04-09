from typing import Any
import pydantic
import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks
from fastapi.exceptions import HTTPException

from backend.gutenberg.controller import GutenController
from backend.gutenberg.models import BookContent
from backend.utils.exceptions import APIException
from backend.ai_tools.book_agent import AgentsManager, BookAgent
from backend.gutenberg.searcher import Searcher

gutenberg_api = GutenController()
agents_manager = AgentsManager()
s = Searcher()

logging.basicConfig(level=logging.INFO)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_origin_regex="https://*",
)


class ChatRequest(pydantic.BaseModel):
    book_id: int
    message: str

    def attach_response(self, response: str):
        return ChatResponse(
            book_id=self.book_id, message=self.message, response=response
        )


class ChatResponse(ChatRequest):
    response: str


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


class SearchQuery(pydantic.BaseModel):
    query: str


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/search", response_model=ResponseModel)
def search(query: SearchQuery):
    try:
        results = s.search(query.query)[:5]
        return ResponseModel(detail="Search results", data=results)
    except Exception:
        raise HTTPException(status_code=500, detail="Couldn't find results")


@app.get("/get_book_content/{id}", response_model=ResponseModel)
async def get_book_content(id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(agents_manager.get_agent, id)

    try:
        book_content: BookContent = gutenberg_api.fetch_book_content(id)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return ResponseModel(detail=f"Fetched book {id}", data=book_content)


@app.get("/get_book_metadata/{id}", response_model=ResponseModel)
def get_book_metadata(id: int):
    try:
        metadata = gutenberg_api.fetch_book_metadata(id)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    return ResponseModel(detail=f"Fetched metadata for book {id}", data=metadata)


@app.post("/chat", response_model=ResponseModel)
def chat(request: ChatRequest):

    def respond(agent: BookAgent, request: ChatRequest):
        response = agent.chat(request.message)
        data = request.attach_response(response)
        logging.info(data)
        return data

    trial = 0
    max_trials = 3
    while trial < max_trials:
        trial += 1
        agent = agents_manager.get_agent(request.book_id)
        try:
            data = respond(agent, request)
            return ResponseModel(detail="Chat response", data=data)

        except Exception as e:
            # Log the exception
            logging.exception(f"Error during chat: {e}")
            agents_manager.remove_agent(request.book_id)
            # Attempt to reinitialize the agent

    raise HTTPException(
        status_code=500, detail="Agent failed to respond after multiple attempts"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
