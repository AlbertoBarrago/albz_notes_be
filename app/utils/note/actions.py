"""
Note Action DB
"""
from datetime import datetime

from fastapi import HTTPException
from app.db.models.notes import Note


def perform_action(db, action, note=None, note_id=None, current_user=None):
    """
    Perform an action on the database
    :param db:
    :param action:
    :param note:
    :param note_id:
    :param current_user:
    :return: Note
    """
    object_data = None
    match action:
        case "add_note":
            object_data = Note(
                title=note.title,
                content=note.content,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=current_user.user_id,
            )
        case "update_note":
            object_data = db.query(Note).filter(Note.id == note_id).first()
            if not object_data:
                raise HTTPException(status_code=404, detail="Note not found")

            if object_data.user_id != current_user.user_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to update this note")

            if note.title:
                object_data.title = note.title
            if note.content:
                object_data.content = note.content
            object_data.updated_at = datetime.now()
        case "get_note_by_id":
            object_data = db.query(Note).filter(Note.id == note_id).first()
            if not object_data:
                raise HTTPException(status_code=404, detail="Note not found")

            if object_data.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to view this note")

            return object_data
        case "get_notes":
            object_data = db.query(Note).filter(Note.user_id == current_user.user_id).all()

            return object_data
        case "delete_note":
            object_data = db.query(Note).filter(Note.id == note_id).first()

            if not object_data:
                raise HTTPException(status_code=404, detail="Note not found")

            if object_data.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to view this note")

            db.delete(object_data)
            db.commit()
            resp = {
                "result": f"Note {note_id} has been deleted",
                "id_note": note_id,
            }
            return resp

    db.add(object_data)
    db.commit()
    db.refresh(object_data)
    return object_data
