"""
Note Action DB
"""
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import or_
from starlette import status

from app.db.models import Note, User
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
        case "search_notes":
            search_query = kwargs.get("query")
            base_query = db.query(Note).join(User).filter(Note.user_id == current_user.user_id)

            if search_query:
                search = f"%{search_query}%"
                base_query = base_query.filter(
                    or_(
                        Note.title.ilike(search),
                        Note.content.ilike(search),
                        User.username.ilike(search)
                    )
                )

            log_action(db,
                       user_id=current_user.user_id,
                       action="search_notes",
                       description="User searched notes successfully")

            result = base_query.all()
        case "get_note_paginated":
            page = kwargs.get("page", 1)
            page_size = kwargs.get("page_size", 10)
            search_query = kwargs.get("query", "").strip()
            sort_by = kwargs.get("sort_by", "created_at")
            sort_order = kwargs.get("sort_order", "desc")

            skip = (page - 1) * page_size

            query = db.query(Note).join(User).options(joinedload(Note.user)) \
                .filter(Note.user_id == current_user.user_id)

            if search_query:
                search = f"%{search_query}%"
                query = query.filter(
                    or_(
                        Note.title.ilike(search),
                        Note.content.ilike(search),
                        User.username.ilike(search)
                    )
                )

            sort_column = getattr(Note, sort_by)

            if sort_order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

            total = query.count()

            notes = query.offset(skip).limit(page_size).all()

            log_action(db,
                       user_id=current_user.user_id,
                       action="get_paginated_notes",
                       description=f"User get paginated "
                                   f"notes with search: "
                                   f"{search_query}" if search_query else "User get "
                                                                          "paginated notes")

            result = {
                "items": [note_to_dict(note) for note in notes],
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size,
                "has_next": page < ((total + page_size - 1) // page_size),
                "has_prev": page > 1,
                "search_query": search_query if search_query else ""
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
