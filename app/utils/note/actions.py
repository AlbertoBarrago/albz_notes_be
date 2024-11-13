"""
Note Action DB
"""
from datetime import datetime
from fastapi import HTTPException
from app.db.models.notes import Note


def note_to_dict(note):
    """Convert Note object to dictionary"""
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "user_id": note.user_id
    }


def perform_note_action(db, action: str, note=None, note_id=None, current_user=None):
    """
    Perform database actions for notes
    :param db: Database connection
    :param action: Action to perform
    :param note: Note object
    :param note_id: ID of note
    :param current_user: Current authenticated user
    :return: Note or response object
    """
    match action:
        case "add_note":
            new_note = Note(
                title=note.title,
                content=note.content,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=current_user.user_id
            )
            db.add(new_note)
            db.commit()
            db.refresh(new_note)
            return {"notes": note_to_dict(new_note)}

        case "update_note":
            note_obj = db.query(Note).filter(Note.id == note_id).first()
            if not note_obj:
                raise HTTPException(status_code=404,
                                    detail="Note not found")

            if note_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to update this note")

            if note.title:
                note_obj.title = note.title
            if note.content:
                note_obj.content = note.content
            note_obj.updated_at = datetime.now()

            db.commit()
            db.refresh(note_obj)
            return note_to_dict(note_obj)

        case "get_note_by_id":
            note_obj = db.query(Note).filter(Note.id == note_id).first()
            if not note_obj:
                raise HTTPException(status_code=404,
                                    detail="Note not found")

            if note_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to view this note")

            return note_to_dict(note_obj)

        case "get_notes":
            notes = db.query(Note).filter(Note.user_id == current_user.user_id).all()
            return [note_to_dict(note) for note in notes]

        case "delete_note":
            note_obj = db.query(Note).filter(Note.id == note_id).first()
            if not note_obj:
                raise HTTPException(status_code=404,
                                    detail="Note not found")

            if note_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to delete this note")

            db.delete(note_obj)
            db.commit()

            return {
                "result": f"Note {note_id} has been deleted",
                "id_note": note_id
            }
