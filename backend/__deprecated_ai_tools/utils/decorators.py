import asyncio
from groq import RateLimitError, APIConnectionError
import re
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@staticmethod
def _extract_retry_time(error_message):
    match = re.search(r"Please try again in (\d+m)?([\d.]+)s", error_message)
    if match:
        minutes = int(match.group(1)[:-1]) if match.group(1) else 0
        seconds = float(match.group(2))
        return timedelta(minutes=minutes, seconds=seconds)
    return None


def durable_ainvoke_decorator(func):
    async def wrapper(*args, **kwargs):
        while True:
            try:
                return await func(*args, **kwargs)
            except RateLimitError as e:
                wait_time = _extract_retry_time(str(e))
                if wait_time:
                    logger.info(f"Rate limit error, waiting for {wait_time}...")
                    await asyncio.sleep(wait_time.total_seconds())
                else:
                    await asyncio.sleep(60)
            except APIConnectionError as e:
                logger.info("API connection error, retrying in 5s...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.exception("Error", e)
                raise

    return wrapper
