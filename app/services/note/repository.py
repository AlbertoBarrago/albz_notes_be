"""
Note Action DB
"""
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import or_

from app.core.exeptions.auth import AuthErrorHandler
from app.core.exeptions.note import NoteErrorHandler
from app.db.models import Note, User
from app.services.audit.repository import log_audit_event
from app.services.logger.repository import LoggerService

logger = LoggerService().logger

class NoteManager:
    """
    Note manager class
    """

    def __init__(self, db):
        self.db = db

    def _log_action(self, user_id: str, action: str, description: str):
        """
        Log audit event and log to file
        :param user_id:
        :param action:
        :param description:
        :return: None
        """
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    @staticmethod
    def _note_to_dict(note):
        """Convert Note object to dictionary"""
        return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "user": note.user
        }

    def paginated_response(self, notes, page, page_size, search_query, total):
        """
        Paginated response
        :param notes:
        :param page:
        :param page_size:
        :param search_query:
        :param total:
        :return: Paginated response
        """
        return {
            "items": [self._note_to_dict(note) for note in notes],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page < ((total + page_size - 1) // page_size),
            "has_prev": page > 1,
            "search_query": search_query
        }

    def handling_paginated_request(self,
                                   current_user,
                                   page,
                                   page_size,
                                   query,
                                   search_query,
                                   skip, sort_by,
                                   sort_order):
        """
        Handling pagination request
        """
        if search_query := search_query.strip():
            search = f"%{search_query}%"
            query = query.filter(
                or_(
                    Note.title.ilike(search),
                    Note.content.ilike(search),
                    User.username.ilike(search)
                )
            )
        sort_column = getattr(Note, sort_by)
        query = query.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())

        total = query.count()
        notes = query.offset(skip).limit(page_size).all()

        log_description = (f"User get pagination notes with search: "
                           f"{search_query}") if search_query \
            else "User get pagination notes"
        self._log_action(current_user.user_id, "get_paginated_notes", log_description)
        return self.paginated_response(notes, page, page_size, search_query, total)

    def get_explore_notes(self,
                         current_user,
                         page=1,
                         page_size=10,
                         search_query="",
                         sort_by="created_at",
                         sort_order="desc"
                         ):
        """
         Get public notes for logged user
        """
        skip = (page - 1) * page_size
        query = self.db.query(Note).join(User, Note.user_id == User.user_id, isouter=True)

        return self.handling_paginated_request(current_user,
                                               page,
                                               page_size,
                                               query,
                                               search_query,
                                               skip, sort_by,
                                               sort_order)

    def get_note_paginated(self, current_user,
                           page=1,
                           page_size=10,
                           search_query="",
                           sort_by="created_at",
                           sort_order="desc"
                           ):
        """
         Get pagination notes for specific user
        """
        skip = (page - 1) * page_size
        query = (self.db.query(Note)
                 .join(User)
                 .options(joinedload(Note.user))
                 .filter(Note.user_id == current_user.user_id))

        return self.handling_paginated_request(current_user,
                                               page,
                                               page_size,
                                               query,
                                               search_query,
                                               skip,
                                               sort_by,
                                               sort_order)

    def search_notes(self, current_user, query):
        """Search notes by query"""
        base_query = self.db.query(Note).join(User).filter(Note.user_id == current_user.user_id)

        if query:
            search = f"%{query}%"
            base_query = base_query.filter(
                or_(
                    Note.title.ilike(search),
                    Note.content.ilike(search),
                    User.username.ilike(search)
                )
            )

        self._log_action(current_user.user_id, "search_notes", "User searched notes successfully")
        return base_query.all()

    def add_note(self, note, current_user):
        """Add new note"""
        try:
            new_note = Note(
                title=note.title,
                content=note.content,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=current_user.user_id
            )

            self._log_action(current_user.user_id, "create_note", "User create note successfully")
            self.db.add(new_note)
            self.db.commit()
            self.db.refresh(new_note)

            return self._note_to_dict(new_note)
        except HTTPException as e:
            self.db.rollback()
            NoteErrorHandler.raise_note_creation_error(e)
            return None

    def update_note(self, note_id, note, current_user):
        """Update existing note"""
        note_obj = (self.db.query(Note)
                    .filter(Note.id == note_id).first())
        if not note_obj:
            NoteErrorHandler.raise_note_not_found()
        if note_obj.user_id != current_user.user_id:
            AuthErrorHandler.raise_unauthorized()

        if note.title:
            note_obj.title = note.title
        if note.content:
            note_obj.content = note.content
        note_obj.updated_at = datetime.now()

        self._log_action(current_user.user_id, "update_note", "User update note successfully")
        self.db.commit()
        self.db.refresh(note_obj)
        return self._note_to_dict(note_obj)

    def delete_note(self, note_id, current_user):
        """Delete note"""
        note_obj = (self.db.query(Note)
                    .filter(Note.id == note_id).first())
        if not note_obj:
            NoteErrorHandler.raise_note_not_found()
        if note_obj.user_id != current_user.user_id:
            AuthErrorHandler.raise_unauthorized()

        self._log_action(current_user.user_id,
                         "delete_note",
                         "User delete note successfully")
        self.db.delete(note_obj)
        self.db.commit()
        return {"result": f"Note {note_id} has been deleted",
                "id_note": note_id}

    def perform_note_action(self, action: str,
                            note=None,
                            note_id=None,
                            current_user=None,
                            **kwargs):
        """
        Perform database actions for notes
        :param action: Action to perform
        :param note: Note object
        :param note_id: ID of note
        :param current_user: Current authenticated user
        :param kwargs: Additional arguments
        :return: Note or response object
        """
        actions = {
            "search_notes": lambda: self.search_notes(current_user, kwargs.get("query")),
            "get_note_paginated": lambda: self.get_note_paginated(
                current_user,
                kwargs.get("page", 1),
                kwargs.get("page_size", 10),
                kwargs.get("query", ""),
                kwargs.get("sort_by", "created_at"),
                kwargs.get("sort_order", "desc"),
            ),
            "get_explore_notes": lambda: self.get_explore_notes(
                current_user,
                kwargs.get("page", 1),
                kwargs.get("page_size", 10),
                kwargs.get("query", ""),
                kwargs.get("sort_by", "created_at"),
                kwargs.get("sort_order", "desc"),
            ),
            "add_note": lambda: self.add_note(note, current_user),
            "update_note": lambda: self.update_note(note_id, note, current_user),
            "delete_note": lambda: self.delete_note(note_id, current_user)
        }
        return actions[action]()
