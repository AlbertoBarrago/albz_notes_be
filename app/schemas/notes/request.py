"""
Note Schemas
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.schemas.user.request import UserBase


class NoteBase(BaseModel):
    """
    NoteBase Model
    """
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_public: bool = Field(default=False)
    tags: List[str] = Field(default_factory=list)
    image_url: Optional[str] = Field(default=None)


class NoteOut(NoteBase):
    """
    NoteOut Model
    """
    id: int
    user: UserBase


class NoteCreate(NoteBase):
    """
    NoteCreate Model
    """
    pass


class NoteUpdate(BaseModel):
    """
    NoteUpdate Model
    """
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    image_url: Optional[str] = Field(default=None)


class NoteDelete(BaseModel):
    """
    NoteDelete Model
    """
    id_note: int
    result: str
