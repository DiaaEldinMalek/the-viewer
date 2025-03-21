from fastapi import FastAPI, Response
from backend.gutenberg.controller import GutenController, BookContent

gutenberg_api = GutenController()

app = FastAPI()


@app.get("/get_book_content/{id}", response_model=BookContent)
def get_book_content(id: str | int):
    book_content = gutenberg_api.fetch_book_content(id)
    return book_content


@app.get("/get_book_metadata/{id}")
def get_book_metadata(id: str | int):
    metadata = gutenberg_api.fetch_book_metadata(id)
    return metadata


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
