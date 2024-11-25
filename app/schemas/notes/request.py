"""
Note Schemas
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user.request import UserBase


class NoteBase(BaseModel):
    """
    NoteBase Model
    """
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class NoteCreate(NoteBase):
    """
    NoteCreate Model
    """


class NoteUpdate(NoteBase):
    """
    NoteUpdate Model
    """
    title: Optional[str] = None
    content: Optional[str] = None


class NoteOut(NoteBase):
    """
    NoteOut Model
    """
    id: int
    user: UserBase


class NoteDelete(BaseModel):
    """
    NoteDelete Model
    """
    id_note: int
    result: str
