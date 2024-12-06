"""
Note Action DB
"""
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import or_

from app.core.exceptions.auth import AuthErrorHandler
from app.core.exceptions.note import NoteErrorHandler
from app.db.models import Note, User
from app.dto.note.noteDTO import NoteDTO
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService

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
        try:
            logger.info("User %s %s %s", user_id, action, description)
            log_audit_event(self.db, user_id=user_id, action=action, description=description)
        except Exception as e:
            logger.error(f"Error logging action: {str(e)}")
            raise HTTPException(status_code=500, detail="Error logging action")

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
        try:
            if search_query := search_query.strip():
                search = f"%{search_query}%"
                query = query.filter(
                    or_(
                        Note.title.ilike(search),
                        Note.content.ilike(search),
                        Note.tags.contains(search),
                        User.username.ilike(search),
                        User.email.ilike(search)
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

            return NoteDTO.paginated_response(
                notes,
                page,
                page_size,
                search_query,
                total,
                sort_by,
                sort_order
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error handling paginated request: {str(e)}")
            NoteErrorHandler.raise_pagination_error(e)

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
        try:
            skip = (page - 1) * page_size
            query = self.db.query(Note).join(User, Note.user_id == User.user_id, isouter=True).filter(
                Note.is_public == True)

            return self.handling_paginated_request(current_user,
                                                   page,
                                                   page_size,
                                                   query,
                                                   search_query,
                                                   skip, sort_by,
                                                   sort_order)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error getting explore notes: {str(e)}")
            NoteErrorHandler.raise_pagination_error(e)

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
        try:
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
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error getting paginated notes: {str(e)}")
            NoteErrorHandler.raise_pagination_error(e)

    def get_note(self, note_id, current_user):
        """Get note by ID"""
        try:
            note_obj = (self.db.query(Note)
                        .filter(Note.id == note_id).first())
            if not note_obj:
                NoteErrorHandler.raise_note_not_found()
            if not note_obj.is_public and note_obj.user_id != current_user.user_id:
                AuthErrorHandler.raise_unauthorized()
            return NoteDTO.from_model(note_obj)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error getting note: {str(e)}")
            NoteErrorHandler.raise_pagination_error(e)

    def search_notes(self, current_user, query):
        """Search notes by query"""
        try:
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
            notes = base_query.all()
            return [NoteDTO.from_model(note) for note in notes]
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error searching notes: {str(e)}")
            raise HTTPException(status_code=500, detail="Error searching notes")

    def add_note(self, note, current_user):
        """Add new note"""
        try:
            new_note = Note(
                title=note.title,
                content=note.content,
                is_public=note.is_public,
                tags=note.tags,
                image_url=note.image_url,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=current_user.user_id
            )

            self._log_action(current_user.user_id, "create_note", "User create note successfully")
            self.db.add(new_note)
            self.db.commit()
            self.db.refresh(new_note)

            return NoteDTO.from_model(new_note)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding note: {str(e)}")
            NoteErrorHandler.raise_note_creation_error(str(e))

    def update_note(self, note_id, note, current_user):
        """Update existing note"""
        try:
            note_obj = (self.db.query(Note)
                        .filter(Note.id == note_id).first())
            if not note_obj:
                NoteErrorHandler.raise_note_not_found()
            if note_obj.user_id != current_user.user_id:
                AuthErrorHandler.raise_unauthorized()

            update_fields = {
                'title': note.title,
                'content': note.content,
                'is_public': note.is_public,
                'image_url': note.image_url,
                'tags': note.tags
            }

            for field, value in update_fields.items():
                if value is not None:
                    setattr(note_obj, field, value)

            note_obj.updated_at = datetime.now()

            self._log_action(current_user.user_id, "update_note", "User update note successfully")
            self.db.commit()
            self.db.refresh(note_obj)
            return NoteDTO.from_model(note_obj)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating note: {str(e)}")
            raise HTTPException(status_code=500, detail="Error updating note")

    def delete_note(self, note_id, current_user):
        """Delete note"""
        try:
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
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting note: {str(e)}")
            raise HTTPException(status_code=500, detail="Error deleting note")

    def perform_note_action(self, action: str,
                            note=None,
                            note_id=None,
                            current_user=None,
                            **kwargs):
        """
        Perform database actions for note
        :param action: Action to perform
        :param note: Note object
        :param note_id: ID of note
        :param current_user: Current authenticated user
        :param kwargs: Additional arguments
        :return: Note or response object
        """
        try:
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
                "get_note_by_id": lambda: self.get_note(note_id, current_user),
                "update_note": lambda: self.update_note(note_id, note, current_user),
                "delete_note": lambda: self.delete_note(note_id, current_user)
            }
            return actions[action]()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error performing note action: {str(e)}")
            raise HTTPException(status_code=500, detail="Error performing note action")
