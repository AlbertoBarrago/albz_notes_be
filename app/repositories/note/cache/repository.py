from functools import lru_cache
from typing import Any

from app.core import settings
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService

logger = LoggerService().logger


class CacheRepository:
    def __init__(self, db):
        self.db = db

    def _log_action(self, user_id, action, description):
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    @lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
    def get_public_notes(self, current_user, page: int, page_size: int,
                         search_query: str, sort_by: str, sort_order: str = 'desc') -> Any:
        """Cache layer for public notes"""
        from app.repositories.note.repository import NoteManager
        self._log_action(current_user.user_id, 'fetch data from cache', 'Get Public Notes from Cache')
        return NoteManager(self.db).get_explore_notes(
            current_user, page, page_size, search_query, sort_by, sort_order
        )

    @lru_cache(maxsize=settings.CACHE_CONFIG["MAXSIZE"])
    def get_note_paginated(self, current_user, page: int, page_size: int,
                           search_query: str, sort_by: str, sort_order: str = 'desc') -> Any:
        """Cache layer for paginated notes"""
        from app.repositories.note.repository import NoteManager
        self._log_action(current_user.user_id, 'fetch data from cache', 'Get Notes from Cache')
        return NoteManager(self.db).get_note_paginated(
            current_user, page, page_size, search_query, sort_by, sort_order
        )
