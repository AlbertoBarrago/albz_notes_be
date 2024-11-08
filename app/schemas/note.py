from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"env_file": ".env"}


class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteOut(NoteBase):
    id: int

    model_config = {"env_file": ".env"}


class NoteDelete(BaseModel):
    id_note: int
    result: str

    model_config = {"env_file": ".env"}
