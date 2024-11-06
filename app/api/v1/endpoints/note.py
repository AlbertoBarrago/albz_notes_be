from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import DbConnection
from app.models.note import Note
from app.schemas.note import NoteOut, NoteCreate, NoteUpdate
from app.utils.dependency import get_db

router = APIRouter()


@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    try:
        db_note = Note(
            title=note.title,
            content=note.content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    except Exception as e:
        db.rollback()
        print(f"Error creating note: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the note: {str(e)}",
        )


@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.title:
        db_note.title = note.title
    if note.content:
        db_note.content = note.content
    db_note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.get("/", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db)):
    db_notes = db.query(Note).all()
    return db_notes
