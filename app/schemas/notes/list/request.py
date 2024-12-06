"""
Note listing request schema
"""
from pydantic import BaseModel, Field


class NoteQueryParams(BaseModel):
    """Query parameters for note listing endpoints"""
    page: int = Field(default=1)
    page_size: int = Field(default=10)
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$")
    sort_by: str = Field(default="created_at", pattern="^(created_at|updated_at)$")
    query: str = Field(default="", max_length=100)
    title: str | None = Field(default=None, max_length=100)
    content: str | None = Field(default=None, max_length=1000)
    created_at: str | None = Field(default=None, pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    updated_at: str | None = Field(default=None, pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
