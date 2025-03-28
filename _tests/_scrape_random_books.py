import random
from backend.gutenberg.controller import GutenController, BookContent
import pathlib
import json


ctrl = GutenController()
for i in range(10):
    idx = random.randint(1, 9999)
    book_path = pathlib.Path("cache/" + str(idx))
    book_path.mkdir(parents=True, exist_ok=True)

    content = ctrl.fetch_book_content(idx)
    metadata = ctrl.fetch_book_metadata(idx)

    with open(book_path.joinpath("content.txt"), "w") as f:
        f.write(content.content)
    with open(book_path.joinpath("metadata.json"), "w") as f:
        json.dump(metadata.model_dump(), f)
