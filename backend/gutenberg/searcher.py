import pandas as pd
from typing import TypedDict


class QueryResult(TypedDict):
    book_id: int
    title: str


class Searcher:
    def __init__(self):
        self.df = pd.read_csv("pg_catalog.csv")[["Text#", "Title"]].rename(
            columns={"Text#": "book_id", "Title": "title"}
        )

    def search(self, query) -> list[QueryResult]:
        results = []
        mask = self.df["title"].str.contains(query, case=False)
        results = self.df[mask].to_dict(orient="records")
        return results  # type: ignore
