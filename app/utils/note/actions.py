"""
Note Action DB
"""
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from starlette import status

from app.db.models import Note
from app.utils.audit.actions import log_action


def note_to_dict(note):
    """Convert Note object to dictionary"""
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "user": note.user
    }


def perform_note_action(db,
                        action: str,
                        note=None,
                        note_id=None,
                        current_user=None,
                        **kwargs):
    """
    Perform database actions for notes
    :param db: Database connection
    :param action: Action to perform
    :param note: Note object
    :param note_id: ID of note
    :param current_user: Current authenticated user
    :param kwargs: Additional arguments
    :return: Note or response object
    """
    result = None
    match action:
        case "get_notes":
            notes = (db.query(Note)
                     .filter(Note.user_id == current_user.user_id)
                     .options(joinedload(Note.user)).all())
            log_action(db,
                       user_id=current_user.user_id,
                       action="get_notes",
                       description="User get notes successfully")
            result = [note_to_dict(note) for note in notes]
        case "get_note_by_id":
            note_obj = db.query(Note).filter(Note.id == note_id).first()
            if not note_obj:
                raise HTTPException(status_code=404,
                                    detail="Note not found")

            if note_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to view this note")

            log_action(db,
                       user_id=current_user.user_id,
                       action="get_note_by_id",
                       description="User get note successfully")

            result = note_to_dict(note_obj)
        case "get_note_paginated":
            page = kwargs.get("page", 1)
            page_size = kwargs.get("page_size", 10)

            skip = (page - 1) * page_size

            total = db.query(Note) \
                .filter(Note.user_id == current_user.user_id) \
                .count()

            notes = db.query(Note) \
                .filter(Note.user_id == current_user.user_id) \
                .offset(skip) \
                .limit(page_size) \
                .all()

            log_action(db,
                       user_id=current_user.user_id,
                       action="get_paginated_notes",
                       description="User get paginated notes successfully")

            result = {
                "items": notes,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }
        case "add_note":
            try:
                new_note = Note(
                    title=note.title,
                    content=note.content,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    user_id=current_user.user_id
                )

                log_action(db,
                           user_id=current_user.user_id,
                           action="create_note",
                           description="User create note successfully")

                db.add(new_note)
                db.commit()
                db.refresh(new_note)

                result = note_to_dict(new_note)

            except Exception as e:
                db.rollback()
                print(f"Error creating note: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while creating the note: {str(e)}",
                ) from e
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

            log_action(db,
                       user_id=current_user.user_id,
                       action="update_note",
                       description="User update note successfully")

            db.commit()
            db.refresh(note_obj)
            result = note_to_dict(note_obj)
        case "delete_note":
            note_obj = db.query(Note).filter(Note.id == note_id).first()
            if not note_obj:
                raise HTTPException(status_code=404,
                                    detail="Note not found")

            if note_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403,
                                    detail="You do not have permission to delete this note")

            log_action(db,
                       user_id=current_user.user_id,
                       action="delete_note",
                       description="User delete note successfully")

            db.delete(note_obj)
            db.commit()

            result = {
                "result": f"Note {note_id} has been deleted",
                "id_note": note_id
            }

    return result
