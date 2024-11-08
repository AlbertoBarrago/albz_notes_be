"""
Note Endpoint
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from app.db.models.notes import Note
from app.db.models.users import User
from app.schemas.note import NoteOut, NoteCreate, NoteUpdate, NoteDelete
from app.utils.audit_utils import log_action
from app.utils.dependency import get_db, get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

router = APIRouter()


@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate,
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
        db_note = Note(
            title=note.title,
            content=note.content,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=current_user.user_id,
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        log_action(db,
                   user_id=current_user.user_id,
                   action="create_note",
                   description="User create note successfully")

        return db_note
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

    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this note")

    if note.title:
        db_note.title = note.title
    if note.content:
        db_note.content = note.content
    db_note.updated_at = datetime.now()

    db.commit()
    db.refresh(db_note)

    log_action(db,
               user_id=current_user.user_id,
               action="update_note",
               description="User update note successfully")

    return db_note


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

    db_note = db.query(Note).filter(Note.id == note_id).first()

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.user_id != current_user.user_id:  # Ensure the user owns the note
        raise HTTPException(status_code=403, detail="You do not have permission to view this note")

    db.delete(db_note)
    db.commit()
    resp = {
        "result": f"Note {note_id} has been deleted",
        "id_note": note_id,
    }

    log_action(db,
               user_id=current_user.user_id,
               action="delete_note",
               description="User delete note successfully")

    return resp


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

    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    if db_note.user_id != current_user.user_id:  # Ensure the user owns the note
        raise HTTPException(status_code=403, detail="You do not have permission to view this note")

    log_action(db,
               user_id=current_user.user_id,
               action="get_note",
               description="User get note successfully")

    return db_note


@router.get("/", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    """
    Get Notes
    :param db:
    :param current_user:
    :return: NoteOut
    """
    db_notes = db.query(Note).filter(Note.user_id == current_user.user_id).all()

    log_action(db,
               user_id=current_user.user_id,
               action="get_notes", description="User get notes successfully")

    return db_notes
