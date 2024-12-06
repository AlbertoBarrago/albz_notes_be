"""
    Cache decorator for caching data
"""
from functools import lru_cache
from typing import Any

from app.core import settings


@lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
def cache_data(key: str) -> Any:
    """
    LRU Cache decorator caches up to 128 items in memory
    When the cache is full, Least Recently Used items are removed first
    """
    return key
