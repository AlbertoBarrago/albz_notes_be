from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class NoteDTO:
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    is_public: bool
    tags: List[str]
    image_url: Optional[str]

    @staticmethod
    def from_model(note) -> dict:
        return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "is_public": note.is_public,
            "tags": note.tags if note.tags else [],
            "image_url": note.image_url,
            "user": {
                "username": note.user.username,
                "email": note.user.email,
                "role": note.user.role,
                "picture_url": note.user.picture_url
            }
        }

    @staticmethod
    def paginated_response(notes, page: int, page_size: int, search_query: str, total: int, sort_by: str,
                           sort_order: str) -> dict:
        return {
            "items": [NoteDTO.from_model(note) for note in notes],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page < ((total + page_size - 1) // page_size),
            "has_prev": page > 1,
            "search_query": search_query,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
