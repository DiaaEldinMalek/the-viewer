import os
import pathlib
import enum
import logging
from langchain_core.documents import Document

from .gutenberg.controller import GutenController
from .gutenberg.cache_manager import GutenbergCacheManager
from .ai_interface.core import AISummarizer, AIChatAgent
from functools import lru_cache

api_key = os.environ.get("GROQ_API_KEY")

logger = logging.getLogger(__name__)


class AIModels(enum.Enum):
    GEMMA2_9B_IT = "gemma2-9b-it"
    QWEN_QWQ_32B = "qwen-qwq-32b"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class BookAIAssistant:
    def __init__(self):
        self.summarizer = AISummarizer(AIModels.GEMMA2_9B_IT.value)
        self.agent = AIChatAgent(AIModels.QWEN_QWQ_32B.value)
        self.gutenberg_manager = GutenController()
        self.book_cache_manager = GutenbergCacheManager()

    async def get_book_summary(self, book_id: int, from_cache=True):
        logger.info(f"Getting book summary for book: {book_id}")

        if from_cache and (
            summary := self.book_cache_manager.get_book_summary(book_id)
        ):
            logger.info(f"Book summary for book: {book_id} found in cache")
            return summary

        book_content = self.gutenberg_manager.fetch_book_content(book_id)
        summary = await self.summarizer.generate_summary(
            [Document(book_content.content)]
        )
        logger.info("Summary generated successfully")
        self.book_cache_manager.save_book_summary(book_id, summary)
        return summary

    async def chat_about_book(self, book_id: int, message: str):
        logger.info(
            f"Chatting about book: {book_id}. Message: {message}. Fetching book summary"
        )
        book_summary = await self.get_book_summary(book_id)
        book_metadata = self.gutenberg_manager.fetch_book_metadata(book_id)
        prompt_data = {
            "metadata": book_metadata.metadata,
            "summary": book_summary,
            "human_input": message,
        }
        return await self.agent.chat(prompt_data)
