"""
Note Endpoint
"""
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.models.users import User
from app.schemas.note import NoteOut, NoteCreate, NoteDelete
from app.db.mysql import get_db, get_current_user
from app.schemas.pagination import PaginatedResponse
from app.utils.note.actions import perform_note_action

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

router = APIRouter()


@router.get("/", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    """
    Get Notes
    :param db:
    :param current_user:
    :return: NoteOut
    """
    return perform_note_action(db, 'get_notes', current_user=current_user)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """
    Get Note
    :param note_id:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return perform_note_action(db, 'get_note_by_id',
                               note_id=note_id,
                               current_user=current_user)


@router.get("/list/paginated", response_model=PaginatedResponse[NoteOut])
def get_paginated_notes(
        page: int = Query(default=1, gt=0),
        page_size: int = Query(default=10, gt=0, le=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get paginated notes
    :param page:
    :param page_size:
    :param current_user:
    :param db:
    :return:
    """
    return perform_note_action(db, "get_note_paginated",
                               current_user=current_user,
                               page=page,
                               page_size=page_size)


@router.get("/list/search", response_model=List[NoteOut])
def search_notes(
        query: str = Query(None, description="Search term for title, content or author"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Search notes
    :param query:
    :param current_user:
    :param db:
    :return:
    """
    return perform_note_action(db, "search_notes", query=query, current_user=current_user)


@router.post("/", response_model=NoteOut)
def add_note(note: NoteCreate,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """
    Create a new note
    :param note:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return perform_note_action(db,
                               'add_note',
                               note,
                               current_user=current_user)


@router.delete("/{note_id}", response_model=NoteDelete)
def delete_note(note_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Delete a note
    :param note_id:
    :param db:
    :param current_user:
    :return: NoteDelete
    """

    return perform_note_action(db,
                               "delete_note",
                               note_id=note_id,
                               current_user=current_user)
