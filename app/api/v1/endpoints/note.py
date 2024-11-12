"""
Note Endpoint
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from app.db.models.users import User
from app.schemas.note import NoteOut, NoteCreate, NoteUpdate, NoteDelete
from app.utils.audit.actions import log_action
from app.db.mysql import get_db, get_current_user
from app.utils.note.actions import perform_note_action

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

router = APIRouter()


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

    notes_out = perform_note_action(db, 'get_note_by_id',
                                    note_id=note_id,
                                    current_user=current_user)


    log_action(db,
               user_id=current_user.user_id,
               action="get_note_by_id",
               description="User get note successfully")

    return notes_out


@router.get("/", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    """
    Get Notes
    :param db:
    :param current_user:
    :return: NoteOut
    """
    notes_out = perform_note_action(db, 'get_notes', current_user=current_user)

    log_action(db,
               user_id=current_user.user_id,
               action="get_notes", description="User get notes successfully")

    return notes_out


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
    try:
        notes_out = perform_note_action(db,
                                       'add_note',
                                       note,
                                       current_user=current_user)

        log_action(db,
                   user_id=current_user.user_id,
                   action="create_note",
                   description="User create note successfully")

        return notes_out
    except Exception as e:
        db.rollback()
        print(f"Error creating note: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the note: {str(e)}",
        ) from e


@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Update a note
    :param note_id:
    :param note:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    notes_out = perform_note_action(db,
                                   'update_note',
                                   note,
                                   note_id=note_id,
                                   current_user=current_user,
                                   )


    log_action(db,
               user_id=current_user.user_id,
               action="update_note",
               description="User update note successfully")

    return notes_out


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

    notes_out = perform_note_action(db,
                                   "delete_note",
                                   note_id=note_id,
                                   current_user=current_user)


    log_action(db,
               user_id=current_user.user_id,
               action="delete_note",
               description="User delete note successfully")

    return notes_out
