"""
Note Schemas
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class NoteBase(BaseModel):
    """
    NoteBase Model
    """
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"env_file": ".env"}


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

    model_config = {"env_file": ".env"}


class NoteDelete(BaseModel):
    """
    NoteDelete Model
    """
    id_note: int
    result: str

    model_config = {"env_file": ".env"}
