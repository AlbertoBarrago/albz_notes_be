"""
 Cache Repository
"""
from functools import lru_cache
from typing import Any

from app.core import settings
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService
from app.repositories.note.repository import NoteManager

logger = LoggerService().logger


class CacheRepository:
    """
    Manages cache repositories and integrates caching with database-backed storage solutions.

    The CacheRepository class serves as a bridge between the application's caching layer and
    the database layer. It provides methods for accessing public and paginated notes with caching
    enabled, to enhance performance by reducing the need for repeated database queries. The class
    uses the least recently used (LRU) caching strategy to manage cache size and maintains an
    audit trail of actions performed by users interacting with the cached data.
    """
    def __init__(self, db):
        self.db = db

    def _log_action(self, user_id, action, description):
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    @lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
    def get_public_notes(self, current_user, page: int, page_size: int,
                         search_query: str, sort_by: str, sort_order: str = 'desc') -> Any:
        """Cache layer for public notes"""
        self._log_action(current_user.user_id,
                         'fetch data from cache',
                         'Get Public Notes from Cache')
        return NoteManager(self.db).get_explore_notes(
            current_user, page, page_size, search_query, sort_by, sort_order
        )

    @lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
    def get_note_paginated(self, current_user, page: int, page_size: int,
                           search_query: str, sort_by: str, sort_order: str = 'desc') -> Any:
        """Cache layer for paginated notes"""
        self._log_action(current_user.user_id, 'fetch data from cache', 'Get Notes from Cache')
        return NoteManager(self.db).get_note_paginated(
            current_user, page, page_size, search_query, sort_by, sort_order
        )
