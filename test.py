from backend.book_ai_assistant import BookAIAssistant

import asyncio
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Set datetime format
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("groq").setLevel(logging.WARNING)

assistant = BookAIAssistant()


async def main():
    # logging.info(start := datetime.now())
    summary = await assistant.get_book_summary(1342)
    # logging.info(end := datetime.now())
    print(summary)


asyncio.run(main())
